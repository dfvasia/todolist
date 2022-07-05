from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions


from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = (
            'id',
            'email',
            'last_name',
            'password',
            'phone',
            'first_name',
            'username',
        )

    def validate(self, attrs: dict):
        password: str = attrs.get('password')
        password_repeat: str = attrs.pop('password_repeat', None)
        if password == password_repeat:
            return attrs
        raise exceptions.ValidationError('Пароли должны совпадать')

    def create(self, data):
        return User.objects.create_user(**data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict):
        username: str = attrs.get('username')
        password: str = attrs.pop('password')
        user = authenticate(username=username, password=password)
        if user:
            attrs['user'] = user
            return attrs
        raise exceptions.ValidationError('Логин или пароль не корректны')


class UserSerializer(serializers.ModelSerializer):
    ...
