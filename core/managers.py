from django.contrib.auth.models import (BaseUserManager)


class UserManager(BaseUserManager):
    """
    функция создания пользователя — в нее мы передаем обязательные поля
    """

    def create_user(self, username, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password=None):
        """
        Функция для создания суперпользователя — с ее помощью мы создаем администратора
        это можно сделать с помощью команды createsuperuser
        """

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.save(using=self._db)
        return user
