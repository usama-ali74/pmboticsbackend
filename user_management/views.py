from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from fyp_management.permission import IsFYPPanel, IsStudent, IsSupervisor
from supervisor.serializers import AddSupervisorSerializer, updateSupervisorSerializer
from teamMember.serializers import teamMemberSerializer, updateStudentSerializer
from core.models import User, teamMember, supervisor, project
from project.serializers import projectSerializer
from django.core.mail import send_mail
from django.conf import settings
from google.auth import exceptions
from django.utils import timezone
from rest_framework import status
from django.db import transaction


# Create your views here.
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    
    @transaction.atomic
    def post(self, request):
        try:
            if request.data.get("role") == User.SUPERVISOR:
                serialize = AddSupervisorSerializer(data=request.data)
                if serialize.is_valid():
                    serialize.save()
                    subject = 'SUPERVISOR Registration'
                    email_from = request.user
                    message = f"You are registered in PMBOTICS By {request.user.uni.name}. You are welcome into the system PMBOTICS By {request.user.uni.name}.\nDepartment {request.user.department}\nPlease find your login credentials:\nEmail: {request.data.get('email')}\nPassword: {request.data.get('password')}\nDue to system security, please do not provide your credentials to anyone.\nFYP Co-ordinator Name: {request.user.name}\nEmail Id: {email_from}"
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
                else:
                    return Response(
                        {
                        "status": 422,
                        "message": serialize.errors,
                        "body": {},
                        "exception": "some exception" 
                        }
                    )
            elif request.data.get("role") == User.STUDENT:            
                serialize = teamMemberSerializer(data=request.data)                        
                if serialize.is_valid():
                    serialize.save()
                    subject = 'STUDENT Registration'
                    email_from = request.user
                    message = f"You are registered in PMBOTICS By {request.user.uni.name}. You are welcome into the system PMBOTICS By {request.user.uni.name}.\nDepartment {request.user.department}\nPlease find your login credentials:\nEmail: {request.data.get('email')}\nPassword: {request.data.get('password')}\nDue to system security, please do not provide your credentials to anyone.\nFYP Co-ordinator Name: {request.user.name}\nEmail Id: {email_from}"
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
                else:
                    return Response(
                        {
                        "status": 422,
                        "message": serialize.errors,
                        "body": {},
                        "exception": "some exception" 
                        }
                    )
            
        except Exception as e:
            return Response(
                {
                "status": 400,
                "message": "Bad Request",
                "body": {},
                "exception": str(e)
                }
            )
            

class allusersAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def get(self, request):
        try:
            if request.GET.get("role") == "supervisor":                    
                my_objects = supervisor.objects.filter(deleted_at=None)
                serialize = AddSupervisorSerializer(my_objects, many=True)
                return Response(       
                        {
                        "data": serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
            elif request.GET.get("role") == "student":
                my_objects = teamMember.objects.filter(deleted_at=None)
                serialize = teamMemberSerializer(my_objects, many=True)
                return Response(       
                        {
                        "data": serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
            else:
                return Response(
                    {
                    "status": 422,
                    "message": serialize.errors,
                    "body": {},
                    "exception": "some exception" 
                    }
                )
        except Exception as e:
            return Response(
                {
                "status": 400,
                "message": "Bad Request",
                "body": {},
                "exception": str(e)
                }
            )


class updatesupervisorAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def patch(self, request):
      try:
        instance = supervisor.objects.get(id=request.data.get("id"), deleted_at=None)
        serialize = updateSupervisorSerializer(instance,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(       
                    {
                    "data": serialize.data,
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None 
                    }
                )
        else:
            return Response(
                    {
                    "status": 422,
                    "message": serialize.errors,
                    "body": {},
                    "exception": "some exception" 
                    }
                )
            
      except Exception as e:
          return Response(       
                {
                "status": 404,
                "message": "Some exception",
                "body": {},
                "exception": str(e) 
                }
            )


class deletesupervisorAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def delete(self, request, pk):
        try:
            my_object = supervisor.objects.get(pk=pk, deleted_at=None)
            User_object = User.objects.get(id = my_object.user.id, deleted_at=None)
            pro = project.objects.filter(supervisor=pk, deleted_at=None, status='ongoing')
            serialize = projectSerializer(pro, many=True)
            data = serialize.data
            projects = [] 
            for item in data:
                projects.append(item["title"])
            if len(pro) == 0:
                User_object.deleted_at = timezone.now()
                User_object.save()
                my_object.deleted_at = timezone.now()
                my_object.save()
            else:
                return Response(
                {
                "status": 400,
                "message": f"Supervisor must be removed from projects {projects} before deletion",
                "body": {},
                "exception": None 
                }
            )
        except supervisor.DoesNotExist:
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


class updatestudentAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def patch(self, request):
      try:
        sup = teamMember.objects.get(id=request.data.get("id"), deleted_at=None)
        serialize = updateStudentSerializer(sup,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(       
                    {
                    "data": serialize.data,
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None 
                    }
                    )
        else:
            return Response(
                    {
                    "status": 422,
                    "message": serialize.errors,
                    "body": {},
                    "exception": "some exception" 
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

class deletestudentAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def delete(self, request, pk):
        try:
            my_object = teamMember.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except teamMember.DoesNotExist:
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


class studentlistAPI(APIView):
    permission_classes = [IsAuthenticated & (IsSupervisor | IsStudent)]
    def get(self, request):
        try:
            department_obj = request.user.department
            tm = teamMember.objects.filter(user__department=department_obj, deleted_at=None, project_id=None)
            serialize = updateStudentSerializer(tm, many=True)        
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
