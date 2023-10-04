from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from fyp_management.permission import IsSuperAdmin
from core.models import department, University, User
from .serializers import departmentSerializer
from rest_framework.views import APIView
from django.utils import timezone
from django.core.mail import send_mail
from google.auth import exceptions
from fyp_management.permission import IsFYPPanel
from authentication_management.serializers import RegisterSerializer
# Create your views here.

class departmentAPI(APIView):
    permission_classes = [IsAuthenticated & IsSuperAdmin]

    def get(self, request):
        try:
            uni_id = request.user.uni_id
            sup = department.objects.filter(uni__id = uni_id, deleted_at=None)
            serialize = departmentSerializer(sup, many=True)
            return Response(
                {
                "data":serialize.data,
                "status": 200,
                "message": "Success",
                "body": {},
                "exception": None
                }
            )
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

    @transaction.atomic  
    def post(self, request):
        uni_id = request.user.uni_id
        try:
            data1 = {
                'name':request.data.get("dep_name"),
                'hod':request.data.get("hod_name"),
                'uni':uni_id
            }
            serialize = departmentSerializer(data=data1)
            if serialize.is_valid():
                dep = serialize.save()
                dep_id = dep.id
            data = {
                'email':request.data.get("email"),
                'name':request.data.get("hod_name"),
                'password':request.data.get("password"),
                'facultyid': request.data.get("facultyid"),
                'designation': request.data.get("designation"),
                "phoneno":request.data.get("phoneno"),
                "department":dep_id,
                "uni":uni_id            
                }
            user_serializer = RegisterSerializer(data=data)
            if user_serializer.is_valid():
                user_serializer.save()
                subject = 'PMO Registration'
                email_from = request.user
                message = f"You are registered in PMBOTICS By {request.user.uni.name}. You are welcome into the system PMBOTICS By {request.user.uni.name}. Please find your login credentials:\nEmail: {request.data.get('email')}\nPassword: {request.data.get('password')}\nDue to system security, please do not provide your credentials to anyone.\nAdmin Name: {request.user.name}\nEmail Id: {email_from}"
                recipient_list = [request.data.get('email'), email_from]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                except exceptions.GoogleAuthError:
                    return Response({'error': 'Failed to send email.'}, status=500)
                return Response(
                    {
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

    def patch(self, request):
        try:
            uni = request.user.uni_id
            dep = department.objects.get(id=request.data.get("dep_id"), deleted_at=None)
            fyp_panel = User.objects.get(id=request.data.get("hod_id"), deleted_at=None)
            hod = fyp_panel.name
            data = {
                'name':request.data.get("name"),
                'hod':hod,
                'uni':uni
            }
            serialize = departmentSerializer(dep,data=data)
            if serialize.is_valid():
                serialize.save()
                return Response(
                {
                "data":serialize.data,
                "status": 200,
                "message": "Success",
                "body": {},
                "exception": None
                }
            )
            else:
                return Response(
                {
                "data":[],
                "status": 400,
                "message": serialize.errors,
                "body": {},
                "exception": None
                }
            )
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

    def delete(self, request):
        try:
            pk = request.data.get("dep_id")
            my_object = department.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except department.DoesNotExist:
            return Response(
                        {
                        "status": 404,
                        "message": "Not Found",
                        "body": {},
                        "exception": None 
                        }
                    )
        return Response(
                        {
                        "status": 200,
                        "message": "Successfuly deleted",
                        "body": {},
                        "exception": None 
                        }
                    )