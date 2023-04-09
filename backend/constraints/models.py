from django.db import models

class Constraint(models.Model):
    class Attributes(models.IntegerChoices):
        NONE = 0,
        VARCHAR = 1,
        INT = 2,
        DATE = 3,
        BOOLEAN = 4,
        DATETIME = 5,
        ENUM = 6

    # Need to use module.model name to avoid circular import
    pipeline = models.ForeignKey("pipeline.Pipeline", on_delete=models.CASCADE, null=False)
    column_title = models.TextField(blank=False, null=False)
    attribute_type = models.PositiveSmallIntegerField(choices=Attributes.choices, default=Attributes.NONE)
    nullable = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)

    # Maps attributes to string representations
    # Can't be done in the Attributes model itself because of the override
    VALUES = (
        (Attributes.NONE, 'None'),
        (Attributes.VARCHAR, 'Varchar'),
        (Attributes.INT, 'Integer'),
        (Attributes.DATE, 'Date'),
        (Attributes.BOOLEAN, 'Boolean'),
        (Attributes.DATETIME, 'Datetime'),
        (Attributes.ENUM, 'Enum')
    )

    def __str__(self):
        return f'{self.column_title}[{self.VALUES[self.attribute_type][1]}]'
