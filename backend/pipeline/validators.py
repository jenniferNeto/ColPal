from django.core.validators import EmailValidator

from constraints.models import Constraint

from constraints.models import (
    VarcharConstraint,
    IntegerConstraint,
    FloatConstraint,
    DateConstraint,
    BooleanConstraint,
    DatetimeConstraint,
)

from .models import PipelineFile

import csv
import codecs


class CSVFileValidator:
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

    def _validate_constraint(self, constraint: int, value: str) -> bool:
        # Map the constraint to its class type
        constraints = [
            None,
            VarcharConstraint,
            IntegerConstraint,
            FloatConstraint,
            DateConstraint,
            BooleanConstraint,
            DatetimeConstraint,
            None
        ]

        # Mapped instance
        obj = constraints[constraint]

        if obj is not None:
            try:
                obj.objects.create(value=value)
            except Exception:
                return False
        if constraint == Constraint.Attributes.EMAIL:
            # Email uses built in validator instead of custom instance
            try:
                validator = EmailValidator()
                validator.__call__(value=value)
            except Exception:
                return False

        # NONE constraint
        return True

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
        results.append([True] * len(headers))

        # Validate every cell within the csv file
        for row in reader:
            row_results = []

            for x_index, value in enumerate(row):
                constraint = headers[x_index]

                # Validate for null values
                if constraint.nullable:
                    if value == 'NULL':
                        row_results.append(True)
                        continue
                # Validate for empty vlaues
                if constraint.blank:
                    if value == '':
                        row_results.append(True)
                        continue

                # Validate value against constraint
                row_results.append(self._validate_constraint(constraint.attribute_type, value))

            # Add recorded row to list of values
            results.append(row_results)
        return results
