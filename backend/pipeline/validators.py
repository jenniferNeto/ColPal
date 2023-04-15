from django.core.validators import EmailValidator
from django.db import transaction
from constraints.models import Constraint
from django.db import IntegrityError

from dateutil.parser import parse, ParserError

from constraints.models import (
    VarcharConstraint,
    IntegerConstraint,
    FloatConstraint,
    BooleanConstraint,
)

from .models import PipelineFile

import csv

import io
import pandas as pd

import googlemaps
import os

maps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))


class CSVFileValidator:
    """Validate cells within a csv file against generated constraints"""
    def __init__(self, file: PipelineFile):
        self.file = file

    def _is_csv(self):
        """Validate the file is a csv file"""
        try:
            self.dialect = csv.Sniffer().sniff(self.file.file.read(1024).decode("UTF-8"))
            self.file.file.seek(0, 0)
        except csv.Error:
            return False
        return True

    def _validate_constraint(self, constraint: int, value: str, null=False, blank=False,) -> str:  # type: ignore
        # Map the constraint to its class type
        # This is in the order of the Constraint.VALUES list
        # None represents the constrained values that don't require custom models to validate
        constraints = [
            None,  # NONE
            VarcharConstraint,
            IntegerConstraint,
            FloatConstraint,
            None,  # DATE
            BooleanConstraint,
            None,  # DATETIME
            None   # EMAIL
        ]

        # Mapped instance
        obj = constraints[constraint]

        # Need to use atomic transactions for test cases to work properly
        with transaction.atomic():
            try:
                if obj is not None:
                    # Convert value to use for model creation
                    if constraint == Constraint.Attributes.BOOLEAN:
                        try:
                            value: bool = bool(value)  # type: ignore
                        except Exception as e:
                            return str(e)
                    if constraint == Constraint.Attributes.INTEGER:
                        try:
                            value: int = int(value)  # type: ignore
                        except Exception as e:
                            return str(e)
                    if constraint == Constraint.Attributes.FLOAT:
                        try:
                            value: float = float(value)  # type: ignore
                        except Exception as e:
                            return str(e)
                    try:
                        obj.objects.create(value=value)
                    except Exception as e:
                        return str(e)

                if constraint == Constraint.Attributes.DATE or constraint == Constraint.Attributes.DATETIME:
                    # Date and Datetime use dateutil parser instead of custom instance
                    try:
                        value: str = str(parse(value))  # type: ignore
                    except ParserError as pe:
                        return str(pe)
                    return "OK"

                if constraint == Constraint.Attributes.EMAIL:
                    # Email uses built in validator instead of custom instance
                    try:
                        validator = EmailValidator()
                        validator.__call__(value=value)  # type: ignore
                    except Exception as e:
                        return str(e)
            except IntegrityError as ie:
                return str(ie)
        # NONE constraint
        return 'OK'

    def validate_date(self, x) -> bool:
        """Validate a date"""
        try:
            parse(x)
        except Exception:
            return False
        return True

    def validate_email(self, x) -> bool:
        """Validate an email address"""
        try:
            EmailValidator().__call__(value=x)
        except Exception:
            return False
        return True

    def validate_address(self, x) -> bool:
        """Validate an address using google maps api"""
        return bool(maps.geocode(address=x, components={}))  # type: ignore

    def infer_type(self, x, dtype) -> bool:
        """Alter inference to more accurately describe data by validating"""
        inference = isinstance(x, dtype)

        # isinstance does not consider '1' an int, override functionality
        if not inference and dtype is int or dtype is float:
            try:
                dtype(x)
            except ValueError:
                return inference

            # Differentiate int vs float
            if dtype == float:
                return dtype(x) % 1 != 0
            return float(x) % 1 == 0
        return inference

    def generate_base_types(self):
        """Generate inferred types about a csv file"""
        # Create a dataframe from the csv file
        dataframe = pd.read_csv(io.BytesIO(self.file.file.read()))

        # Record attempts to infer data type
        type_counts = {}
        for col in dataframe.columns:
            for dtype in [bool, int, float, str]:
                # Test every value in a column against the data types and sum the results
                count = dataframe[col].apply(lambda x: self.infer_type(x, dtype)).sum()
                type_counts.setdefault(col, {})[dtype] = count

        # Get the most common type for each column
        most_common_types = {}
        for col, counts in type_counts.items():
            # Pursuade columns that seem to be numbers
            if counts[float] != 0 and counts[str] > counts[float]:
                counts[str] -= counts[float]
            elif counts[int] != 0 and counts[str] > counts[int]:
                counts[str] -= counts[int]
            most_common_types[col] = max(counts, key=counts.get)

        return dataframe, [n.__name__ for n in most_common_types.values()]

    def validate(self):
        # Get dataframe and base inferred types
        dataframe, types = self.generate_base_types()
        names = ["email", "date", "address"]

        # Type conversion minimum threshold
        threshold = 0.4

        # Store types and index of type needed to be checked
        # Only string values need to be checked
        type_counts = {}
        types_index = 0
        for index, col in enumerate(dataframe.columns):
            if types[index] != 'str':
                continue
            for i, dtype in enumerate([self.validate_email, self.validate_date, self.validate_address]):
                # Test every value in a column against the data types and sum the results
                count = dataframe[col].apply(lambda x: dtype(x)).sum()
                type_counts.setdefault(col, {})[names[i]] = count

            # Dictionary of successful email / date validates on a column
            current_types = list(type_counts.values())[types_index]
            types_index += 1

            print("Values:", current_types.values())
            # If no validation was successful, the column really is a plain string
            if not sum(current_types.values()):
                continue

            # Column is actually an email or date
            types[index] = max(current_types, key=current_types.get)

            # Revert conversion if threshold is not satisified
            if current_types[types[index]] < threshold * len(dataframe.index):
                types[index] = 'str'
        print(types)
