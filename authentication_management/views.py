from django.db import IntegrityError, connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from authentication_management.serializers import RegisterSerializer, LoginSerializer, fyppanelSerializer
from authentication_management.utils.contant import LoginMessages
from core.models import User, fyppanel
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from fyp_management.permission import IsFYPPanel
from fyp_management.permission import IsSuperAdmin
from rest_framework.decorators import api_view 
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from google.auth import exceptions
from django.utils import timezone 
import random


class RegisterUserAPIView(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]

    @transaction.atomic  
    def post(self, request):
        try:
            serialize = RegisterSerializer(data=request.data) 
            if serialize.is_valid():
                serialize.save()
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
                    "message": "PMO Registration successful.",
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

class allfyppanelApi(APIView):
    permission_classes = [IsAuthenticated & (IsSuperAdmin| IsFYPPanel)]
    def get(self, request):    
        try:
            uni_id = request.user.uni_id
            dep_id = request.GET.get("dep_id")
            fyppanel = User.objects.filter(uni__id=uni_id, department=dep_id, role="fyp_panel", deleted_at=None)
            serialize = fyppanelSerializer(fyppanel, many=True)
            # data = {
            #     'id':fyppanel.id,
            #     'name':fyppanel.name
            # }
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
                "status": 400,
                "message": "Bad Request",
                "body": {},
                "exception": str(e)
                }
            )

class LoginUserApi(APIView):
    def post(self, request):
        serialize = LoginSerializer(data=request.data)
        if serialize.is_valid():
            try:
                user = User.objects.get(**serialize.validated_data, deleted_at=None)
                email = request.data.get('email')

                # Generate an OTP
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

                # Save the OTP in the user's session or database for verification later
                user.otp = otp
                user.is_active = True
                user.save()

                # Send the OTP to the user's email
                subject = 'Login OTP'
                message = f'Your OTP is: {otp} \nPlease do not provide this OTP with Anyone.\nIt is a system-generated message. Please do not reply to this email.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]

                try:
                    send_mail(subject, message, email_from, recipient_list)
                except exceptions.GoogleAuthError:
                    return Response({'error': 'Failed to send email.'}, status=500)
        
                return Response({
                    "data":[],
                    "message": "OTP successfully sent to your registered email.",
                    "status": 200
                })
            except:
                return Response({
                    "data": None,
                    "message": LoginMessages.WRONG_CREDENTIALS.value,
                    "status": 422
                })
        else:
            return Response({
                "data": serialize.errors,
                "message": None,
                "status": 422
            })

class Validate_otpAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            user = User.objects.get(email=email, deleted_at=None)
            s_otp = user.otp
            if str(otp) == user.otp:
                # OTP is valid, 
                user.last_login = timezone.now()
                user.save()
                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "data": {
                        "access_token": access_token,
                        "id": user.id,
                        "name": user.name,
                        "role": user.role,
                        "dep_id": user.department.id,
                        "University_id":user.uni.id,
                        "University_name":user.uni.name,
                    },
                    "message": "OTP verification successful",
                    "status": 200
                })
            else:
                return Response({
                    "data": [],
                    "message": "Invalid OTP",
                    "status": 400
                })
        
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some errors",
                "body": {},
                "exception": str(e) 
                }
            )
    