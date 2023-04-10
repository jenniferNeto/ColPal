from rest_framework import serializers

from .models import Constraint

class ConstraintSerializer(serializers.ModelSerializer):
    pipeline_id = serializers.SerializerMethodField()
    constraint_id = serializers.SerializerMethodField()
    constraint_title = serializers.SerializerMethodField()
    constraint_type = serializers.SerializerMethodField()

    class Meta:
        model = Constraint

        fields = [
            'pipeline_id',
            'constraint_id',
            'constraint_title',
            'constraint_type',
            'nullable',
            'valid',
        ]

    def get_pipeline_id(self, obj):
        return obj.pipeline.pk

    def get_constraint_id(self, obj):
        return obj.pk

    def get_constraint_title(self, obj):
        return obj.column_title

    def get_constraint_type(self, obj):
        return obj.VALUES[obj.attribute_type][1]

class ConstraintUpdateSerializer(serializers.ModelSerializer):
    """Update a constraint's default state"""

    attribute_type = serializers.ChoiceField(choices=Constraint.VALUES)

    class Meta:
        model = Constraint

        fields = [
            'attribute_type'
        ]
