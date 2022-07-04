# Create your views here.
from django.contrib.auth import login
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny


from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    UserSerializer,
)


class SignupView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        s: LoginSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.validated_data['user']
        login(request, user=user)
        user_serializer = UserSerializer(instance=user)
        return Respo
