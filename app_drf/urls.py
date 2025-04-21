from django.urls import path,include
from . import views

urlpatterns = [
    path('user/token/',views.MyTokenObtainPiarView.as_view(),name='user_token'),
    path('user/register/',views.RegisterView.as_view(),name='user_register'),
]