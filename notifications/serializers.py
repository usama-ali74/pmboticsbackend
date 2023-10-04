from core.models import notification, User, department
from rest_framework import serializers
from datetime import datetime


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(default = datetime.now().date())
    createtime = serializers.TimeField(default = datetime.now().time())
    createdby = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all())
    name = serializers.PrimaryKeyRelatedField(read_only = True, source='createdby.name')

    class Meta:
        model = notification
        fields = ['id','title', 'description', 'createdate', 'createtime', 'department','createdby','name']

    def create(self, validated_data):
        validated_data['createtime'] = datetime.now().strftime('%H:%M')
        return super().create(validated_data)
    def validate_title(self, value):
        if value.isnumeric():
            raise serializers.ValidationError("The value should not contain only numbers.")
        return value
    def validate_description(self, value):
        if value.isnumeric():
            raise serializers.ValidationError("The value should not contain only numbers.")
        return value  