from rest_framework import serializers
from core.models import department, University

class departmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = department
        fields = '__all__'
    
    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError('Dep. Name should be a string')
        return value

    def validate_hod(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError('HOD Name should be a string')
        return value