from django.db import IntegrityError, connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from teamMember.serializers import teamMemberSerializer
from authentication_management.utils.contant import LoginMessages
from core.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view 

# Create your views here.
class RegisterteamMemberAPIView(APIView):
  
  def post(self, request):
    serialize = teamMemberSerializer(data=request.data)
    # try:
    # print(User.objects.get('email')) 
    if serialize.is_valid():
      serialize.save()
      return Response(
        {
          "data": serialize.data,
          "message": "success",
          "status": 200
        }
      )
    else:
      #  serialize.is_valid() == False:
      return Response(
        {
          "data": "",
          "message": serialize.errors,#"Error is already registered",
          "status": 422
        }
      )
