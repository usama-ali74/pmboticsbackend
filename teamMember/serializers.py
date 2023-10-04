from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import teamMember, User, department, University
from django.contrib.auth.hashers import make_password


class teamMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', required=True)
    phoneno = serializers.CharField(source='user.phoneno', required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    rollno = serializers.CharField(required=True)
    seatno = serializers.CharField(required=True)
    enrollmentno = serializers.CharField(required=True)
    uni = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), source='user.uni')
    u_id = serializers.PrimaryKeyRelatedField(read_only = True, source='user.id')

    class Meta:
        model = teamMember
        fields = ['id','email','password','name','rollno', 'seatno', 'enrollmentno', 'phoneno', 'department', 'u_id', 'uni']
    
    def create(self, validated_data):
        tm = User.objects.create(
        email=validated_data['user']['email'],
        name=validated_data['user']['name'],
        password=make_password(validated_data['password']),
        phoneno = validated_data['user']['phoneno'],
        department = validated_data['user']['department'],
        uni=validated_data['user']['uni'],
        is_active = False,
        role=User.STUDENT
        )
        # department_id = validated_data.pop('department')
        # department_instance = department.objects.get(id=department_id)
        # project_id = validated_data.pop('project')
        # project_instance = project.objects.get(id=project_id)
        team = teamMember.objects.create(
        user=tm, 
        rollno=validated_data['rollno'],
        seatno=validated_data['seatno'],
        enrollmentno=validated_data['enrollmentno'],
        # phoneno=validated_data['phoneno'],
        # project =project_instance,        
        # department=department_instance,
        )
        return team

# class studentlistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = teamMember
#         fields = '__all__'

class updateStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    name = serializers.CharField(source='user.name', required=True)
    phoneno = serializers.CharField(source='user.phoneno', required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    rollno = serializers.CharField(required=True)
    seatno = serializers.CharField(required=True)
    enrollmentno = serializers.CharField(required=True)

    class Meta:
        model = teamMember
        fields = ['id','email','name','rollno', 'seatno', 'enrollmentno', 'phoneno', 'department']

    def update(self, instance, validated_data):
        # Update supervisor fields
        instance.rollno = validated_data.get('rollno', instance.rollno)
        instance.seatno = validated_data.get('seatno', instance.seatno)
        instance.enrollmentno = validated_data.get('enrollmentno', instance.enrollmentno)

        
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
