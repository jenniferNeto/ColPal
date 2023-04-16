from rest_framework import serializers

from .models import Constraint

class ConstraintSerializer(serializers.ModelSerializer):
    constraint_id = serializers.SerializerMethodField()
    column_title = serializers.SerializerMethodField()
    column_type = serializers.SerializerMethodField()

    class Meta:
        model = Constraint

        fields = [
            'constraint_id',
            'column_title',
            'column_type',
        ]

    def get_constraint_id(self, obj):
        return obj.pk

    def get_column_title(self, obj):
        return obj.column_title

    def get_column_type(self, obj):
        return obj.VALUES[obj.column_type][1]

class ConstraintUpdateSerializer(serializers.ModelSerializer):
    """Update a constraint's default state"""

    column_type = serializers.ChoiceField(choices=Constraint.VALUES)

    class Meta:
        model = Constraint

        fields = [
            'column_type'
        ]
