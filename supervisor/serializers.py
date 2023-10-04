from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import supervisor, User, teamMember, department, University
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class AddSupervisorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', required=True)
    phoneno = serializers.CharField(source='user.phoneno', required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    uni = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), source='user.uni')
    faculty_no = serializers.CharField(required=True)
    designation = serializers.CharField(required=True)
    field_of_interest = serializers.CharField(required=True)
    
    class Meta:
        model = supervisor
        fields = ['id','email', 'password', 'name','faculty_no', 'field_of_interest', 'phoneno', 'department', 'designation', 'uni']
    
    
    def create(self, validated_data):
        sp = User.objects.create(
        email=validated_data['user']['email'],
        name=validated_data['user']['name'],
        password=make_password(validated_data['password']),
        department = validated_data['user']['department'],
        uni = validated_data['user']['uni'],
        phoneno = validated_data['user']['phoneno'],
        is_active = False,
        role=User.SUPERVISOR
        )
        # department_id = validated_data.pop('department')
        # department_instance = department.objects.get(id=department_id)
        # project_id = validated_data.pop('project')
        # project_instance = project.objects.get(id=project_id)
        sup = supervisor.objects.create(
        user=sp, 
        faculty_no=validated_data['faculty_no'],
        field_of_interest=validated_data['field_of_interest'],
        designation=validated_data['designation'],
        # phone_no=validated_data['phone_no'],
        # project =project_instance,        
        # department=department_instance,
        )
        return sup


class updateSupervisorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    name = serializers.CharField(source='user.name', required=True)
    faculty_no = serializers.CharField(required=True)
    field_of_interest = serializers.CharField(required=True)
    designation = serializers.CharField(required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    phoneno = serializers.CharField(source='user.phoneno', required=True)

    class Meta:
        model = supervisor
        fields = ['id', 'faculty_no', 'field_of_interest', 'designation', 'department', 'email', 'name', 'phoneno']

    def update(self, instance, validated_data):
        # Update supervisor fields
        instance.faculty_no = validated_data.get('faculty_no', instance.faculty_no)
        instance.field_of_interest = validated_data.get('field_of_interest', instance.field_of_interest)
        instance.designation = validated_data.get('designation', instance.designation)

        
        # Update related user department field
        user = instance.user
        email=validated_data['user']['email']
        name=validated_data['user']['name']
        phoneno=validated_data['user']['phoneno']
        dep = validated_data['user']['department']
        user.email = email
        user.name = name
        user.phoneno = phoneno
        user.department = dep
        user.save()
        # Save and return updated supervisor instance

        instance.save()
        return instance
