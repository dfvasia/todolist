from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions


# class NotCorrectPassword:
#     def __init__(self, password):
#         self.password = password
#
#     def __call__(self, value):
#         print(f'{value}!!! {self.password}')
#         if self.password == value:
#             print(f'{value}!!! {self.password}')
#         # if value.get('password') == value.get('password_repeat'):
#         #     return value
#         # raise exceptions.ValidationError('Пароли должны совпадать')


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'password', 'phone', 'first_name', 'username']

