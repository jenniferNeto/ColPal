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
import codecs


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

    def validate(self):
        """Validate all cells within a csv file against header constraints"""
        if not self._is_csv():
            return

        # Create a csv file reader
        reader = csv.reader(codecs.iterdecode(self.file.file.open('r'), "UTF-8"), self.dialect)

        # Get constraint headers and skip header line in reader
        headers = Constraint.objects.filter(pipeline=self.file.pipeline)
        next(reader)

        # Header row is valid by default
        results = []
        results.append(['OK'] * len(headers))

        # Validate every cell within the csv file
        for row in reader:
            row_results = []

            for x_index, value in enumerate(row):
                constraint = headers[x_index]

                # Validate for null values
                if constraint.nullable:
                    if value == 'NULL':
                        row_results.append('OK')
                        continue
                # Validate for empty vlaues
                if constraint.blank:
                    if value == '':
                        row_results.append('OK')
                        continue

                # Validate value against constraint
                row_results.append(self._validate_constraint(constraint.attribute_type, value))

            # Add recorded row to list of values
            results.append(row_results)
        return results
