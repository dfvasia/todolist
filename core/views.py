# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions

from core.models import User
from core.serializers import UserSerializer


class CoreViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [IsAuthenticated],
                                    'retrieve': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'perform_update': [IsAuthenticated],
                                    'destroy': [IsAuthenticated],
                                    }

    def create(self, request, *args, **kwargs):
        password: dict = request.data
        if password['password'] == password.pop('password_repeat'):
            return super().create(request, *args, **kwargs)
        raise exceptions.ValidationError('Пароли должны совпадать')

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]