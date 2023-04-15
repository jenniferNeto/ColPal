from django.db import models

class Constraint(models.Model):
    class Attributes(models.IntegerChoices):
        NONE = 0,
        VARCHAR = 1,
        INTEGER = 2,
        FLOAT = 3
        BOOLEAN = 4,
        DATE = 5,
        ADDRESS = 6,
        EMAIL = 7

    # Need to use module.model name to avoid circular import
    pipeline = models.ForeignKey("pipeline.Pipeline", on_delete=models.CASCADE, null=False)
    column_title = models.TextField(blank=False, null=False)
    column_type = models.PositiveSmallIntegerField(choices=Attributes.choices, default=Attributes.NONE)

    # Maps attributes to string representations
    # Can't be done in the Attributes model itself because of the override
    VALUES = (
        (Attributes.NONE, 'None'),
        (Attributes.VARCHAR, 'Varchar'),
        (Attributes.INTEGER, 'Integer'),
        (Attributes.FLOAT, 'Float'),
        (Attributes.DATE, 'Date'),
        (Attributes.BOOLEAN, 'Boolean'),
        (Attributes.ADDRESS, 'Datetime'),
        (Attributes.EMAIL, 'Email')
    )

    def __str__(self):
        return f'{self.column_title}[{self.VALUES[self.column_type][1]}]'

class VarcharConstraint(models.Model):
    value = models.CharField(null=True, max_length=1000)

class IntegerConstraint(models.Model):
    value = models.IntegerField(null=True)

class FloatConstraint(models.Model):
    value = models.FloatField(null=True)

class BooleanConstraint(models.Model):
    value = models.BooleanField(null=True)
