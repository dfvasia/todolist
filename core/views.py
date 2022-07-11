# Create your views here.
import django.contrib.auth.backends
from django.contrib.auth import login, logout
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    UserSerializer,
    UpdatePasswordSerializer,
)


class SignupView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        s: LoginSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        login(request=request, user=s.validated_data, backend='django.contrib.auth.backends.ModelBackend')
        return Response(s.data, status=200)


class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


class UpdatePasswordView(UpdateAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
