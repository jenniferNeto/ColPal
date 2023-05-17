from django.core.validators import EmailValidator
from django.db.models.fields.files import FieldFile

from dateutil.parser import parse

from constraints.models import Constraint
from pipeline.models import Pipeline

from .models import PipelineFile

import io
import pandas as pd

# import googlemaps
import os

# maps = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))


def validate_date(x: str) -> bool:
    """Validate a date"""
    try:
        parse(x)
    except Exception:
        return False
    return True


def validate_email(x: str) -> bool:
    """Validate an email address"""
    try:
        EmailValidator().__call__(value=x)
    except Exception:
        return False
    return True


# def validate_address(x: str) -> bool:
#     """Validate an address using google maps api"""
#     return bool(maps.geocode(address=x, components={}))  # type: ignore


def infer_type(x, dtype) -> bool:
    """Alter inference to more accurately describe data by validating"""
    inference = isinstance(x, dtype)

    # isinstance does not consider '1' an int, override functionality
    if not inference and dtype in [int, float]:
        try:
            dtype(x)
        except ValueError:
            return inference

        # Differentiate int vs float
        if dtype == float:
            return dtype(x) % 1 != 0
        return float(x) % 1 == 0
    return inference


def generate_base_types(file):
    """Generate inferred types about a csv file"""
    # Create a dataframe from the csv file
    dataframe = pd.read_csv(io.BytesIO(file.read()))

    # Record attempts to infer data type
    type_counts = {}
    for col in dataframe.columns:
        print("COL:", col)
        for dtype in [bool, int, float, str]:
            # Test every value in a column against the data types and sum the results
            count = dataframe[col].apply(lambda x: infer_type(x, dtype)).sum()
            type_counts.setdefault(col, {})[dtype] = count

    # Get the most common type for each column
    most_common_types = {}
    for col, counts in type_counts.items():
        # Pursuade columns that seem to be numbers
        if counts[float] != 0 and counts[str] > counts[float]:
            counts[str] -= counts[float]
        elif counts[int] != 0 and counts[str] > counts[int]:
            counts[str] -= counts[int]
        # Can cause a problem if the column is empty, TODO
        most_common_types[col] = max(counts, key=counts.get)

    return dataframe, [n.__name__ for n in most_common_types.values()]


def generate_types(file):
    # Get dataframe and base inferred types
    dataframe, types = generate_base_types(file)
    names = ["email", "date"]

    # Type conversion minimum threshold
    threshold = 0.4

    # Store types and index of type needed to be checked
    # Only string values need to be checked
    type_counts = {}
    types_index = 0
    for index, col in enumerate(dataframe.columns):
        if types[index] != 'str':
            continue
        for i, dtype in enumerate([validate_email, validate_date]):
            # Test every value in a column against the data types and sum the results
            count = dataframe[col].apply(lambda x: dtype(x)).sum()
            type_counts.setdefault(col, {})[names[i]] = count

        # Dictionary of successful email / date validates on a column
        current_types = list(type_counts.values())[types_index]
        types_index += 1

        # If no validation was successful, the column really is a plain string
        if not sum(current_types.values()):
            continue

        # Column is actually an email or date
        types[index] = max(current_types, key=current_types.get)

        # Revert conversion if threshold is not satisified
        if current_types[types[index]] < threshold * len(dataframe.index):
            types[index] = 'str'

    # Generate response for api
    response = []
    for i in range(len(dataframe.columns)):
        response.append({"column_name": dataframe.columns[i], "column_type": types[i]})
    return response


def validate(file: FieldFile, pipeline: Pipeline):
    """Validate a csv file based on provided types"""
    if not file:
        return {"detail": "File cannot be empty"}

    # Get file and constraint types as indexes
    types = [constraint.column_type for constraint in Constraint.objects.filter(
        pipeline=pipeline)]

    # Create a dataframe from the csv file
    dataframe = pd.read_csv(io.BytesIO(file.read()))
    errors = {}
    error_count = 1

    # Validator list
    validators = [None, str, int, float, bool, validate_email, validate_date]

    for c_index, col in enumerate(dataframe.columns):
        # If no constraints, can't validate
        if len(types) == 0:
            break

        # If files doesn't match generated constraints
        if c_index >= len(types):
            for r_index, row in enumerate(dataframe[col]):
                errors[error_count] = {"col": c_index, "row": r_index, "error": "Undefined column"}
                error_count += 1
            continue
        dtype = validators[types[c_index]]
        for r_index, row in enumerate(dataframe[col]):
            try:
                dtype(row)
            except Exception as e:
                errors[error_count] = {"col": c_index, "row": r_index, "error": str(e)}
                error_count += 1
    return errors
