from rest_framework import generics
from fyp_management.permission import IsFYPPanel, IsStudent, IsSupervisor
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from notifications.serializers import notificationSerializer
from core.models import notification, project, supervisor, User, teamMember
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
# # Create your views here.

class createnotificationAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def post(self, request):
        try:
            serialize = notificationSerializer(data=request.data)
            if request.data.get('id') != None:                
                if serialize.is_valid():
                    notification_obj = serialize.save()
                    projects = project.objects.get(id=request.data.get('id'))
                    projects.notification.add(notification_obj)
                    return Response(
                    {
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )            
            elif serialize.is_valid():
                notification_obj = serialize.save()
                projects = project.objects.filter(status="ongoing", deleted_at=None)
                for p in projects:
                    p.notification.add(notification_obj)
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
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class allnotificationsAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def get(self, request):
        try:
            my_objects = notification.objects.filter(deleted_at=None, department=request.user.department)
            sorted_objects = sorted(my_objects, key=lambda obj: datetime.combine(obj.createdate, obj.createtime), reverse=True)
            serializer = notificationSerializer(sorted_objects, many=True)
            return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })


class getallnotificationsAPI(APIView):
    permission_classes = [IsAuthenticated & (IsStudent | IsSupervisor)]
    def get(self, request):
        try:
            if request.user.role == User.SUPERVISOR:
                sup = supervisor.objects.get(user=request.user, deleted_at=None)
                projects = project.objects.filter(supervisor=sup)
                # print(projects)
                # if projects != None: #projects[0]
                notifications = []
                for p in projects:
                    n = notification.objects.filter(project=p, deleted_at=None)
                    notifications += list(n)
                serializer = notificationSerializer(notifications, many=True)
                return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
            elif request.user.role == User.STUDENT:
                tm = teamMember.objects.get(user=request.user, deleted_at=None)
                p = tm.project
                if p != None:
                    notifications = notification.objects.filter(project=p, deleted_at=None)
                    serializer = notificationSerializer(notifications, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                        })
                else:
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": [],
                        "exception": None
                        })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })

class deletenotificationAPI(APIView):    
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def delete(self, request, pk):
        try:
            my_object = notification.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except notification.DoesNotExist:
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

class updatenotificationAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def patch(self, request):
        try:
            sup = notification.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = notificationSerializer(sup,data=request.data)
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
