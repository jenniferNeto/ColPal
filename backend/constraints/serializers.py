from rest_framework import serializers

from .models import Constraint

class ConstraintSerializer(serializers.Serializer):
    pipeline_id = serializers.SerializerMethodField()
    constraint_id = serializers.SerializerMethodField()
    constraint_title = serializers.SerializerMethodField()
    constraint_type = serializers.SerializerMethodField()
    nullable = serializers.SerializerMethodField()
    valid = serializers.SerializerMethodField()

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
        return obj.pipeline_file.pipeline.pk

    def get_constraint_id(self, obj):
        return obj.pk

    def get_constraint_title(self, obj):
        return obj.column_title

    def get_constraint_type(self, obj):
        return obj.VALUES[obj.attribute_type][1]

    def get_nullable(self, obj):
        return obj.nullable

    def get_valid(self, obj):
        return obj.valid
