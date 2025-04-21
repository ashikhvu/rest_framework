from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny

# Create your views here.
class MyTokenObtainPiarView(TokenObtainPairView):
    serializer = MyTokenObtainPairSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer