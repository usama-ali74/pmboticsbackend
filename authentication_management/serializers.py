from core.models import User, fyppanel, department, University
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

import re

class RegisterSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True, source='user.email')
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  name = serializers.CharField(required=True, source='user.name')
  facultyid = serializers.CharField(required=True)
  designation = serializers.CharField(required=True)
  phoneno = serializers.CharField(required=True, source='user.phoneno')
  department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
  uni = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), source='user.uni')
  
  def validate_name(self, value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError('Name cannot contain digits')
    return value
  
  def validate_phoneno(self, value):
    if not re.match(r'^\d{11}$', value):
      raise serializers.ValidationError("Invalid phone number format check your phone no again")
    return value

  def validate_designation(self, value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError('designation cannot contain digits')
    return value

  class Meta:
    model = User
    fields = ['email', 'password', 'name', 'phoneno', 'department']
    
  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['user']['email'],
      name=validated_data['user']['name'],
      password=make_password(validated_data['password']),
      phoneno=validated_data['user']['phoneno'],
      department=validated_data['user']['department'],
      uni=validated_data['user']['uni'],
      is_active = False,
      role=User.PMO
    )
    FYPPANEL = fyppanel.objects.create(
      user=user, 
      facultyid=validated_data['facultyid'],
      designation=validated_data['designation']
    )
    return FYPPANEL


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True)
  
  # class Meta:
  #   model = User
  #   fields = "__all__"

class fyppanelSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'name']
