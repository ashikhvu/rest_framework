from rest_framework import serializers
from .models import ProfileModel,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        try:
            token['vendor_id'] = user.vendor_id
        except:
            token['vendor_id'] = 0

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        models= ProfileModel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['full_name','email','phone','password','password2']

    def validate(self, attrs):
        if self.password == self.password2:
            raise serializers.ValidationError({"password":"Password doesn't match !"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            full_name=self.validated_data['full_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
        )
        email_user,mobile = user.email.split('@')
        user.set_password(validate_password['password'])
        user.save()
        return user