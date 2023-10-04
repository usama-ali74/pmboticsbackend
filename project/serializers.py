from core.models import project, department, supervisor
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from datetime import datetime
import re

class projectSerializer(serializers.ModelSerializer):
  title = serializers.CharField(required=True)
  year = serializers.CharField(required=True)
  batch = serializers.CharField(required=True)
  description = serializers.CharField(required=True)
  domain = serializers.CharField(required=True)
  no_of_group_members = serializers.IntegerField(required=True)
  department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all())
  supervisor = serializers.PrimaryKeyRelatedField(queryset=supervisor.objects.all())

  def validate_title(self, value):
      if value.isnumeric():
          raise serializers.ValidationError("Title value should not contain only numbers.")
      return value

  def validate_description(self, value):
      if value.isnumeric():
          raise serializers.ValidationError("Description value should not contain only numbers.")
      return value

  def validate_batch(self, value):
      if value.isnumeric():
          raise serializers.ValidationError("Batch should contain alphanumeric value like 19B.")
      return value

  def validate_year(self, value):
    try:
      year = int(value)
      current_year = datetime.now().year
      if year > current_year:
        raise serializers.ValidationError("year should be valid, before "+ str(current_year))
    except ValueError:
        raise serializers.ValidationError("Year must be a valid integer")
    return value
  
  def validate_no_of_group_members(self, value):
    if value < 1 or value > 5:
        raise serializers.ValidationError("Number of group members should be greate than 1 or less than equal to 5")
    return value

  def validate_domain(self, value):
      # Check if the value contains only alphabets
      if not re.match(r'^[a-zA-Z ]+$', value):
          raise serializers.ValidationError("Domain value should contain only alphabets.")
      return value  
  
  class Meta:
    model = project
    fields = ['id','title', 'year', 'batch', 'description', 'status', 'domain', 'no_of_group_members', 'supervisor','department']    


class projectlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = '__all__'
        # fields = ['title']
