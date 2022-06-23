from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from core.managers import UserManager


class User(AbstractUser):
    # username = models.CharField(error_messages={'Незаполненно поле'}, help_text='150 символов или знаков. Только, буквы, цифры и @/./+/-/_.',
    #                              max_length=150, verbose_name='Пользователь', unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, verbose_name='Пользователь', unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=200, verbose_name='Почтовый ящик')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Статус')
    phone = PhoneNumberField(verbose_name='Телефон')
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='Разрешения')
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='Группы')
    password = models.CharField(max_length=128, verbose_name='ХЕШ пароля')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Последний вход')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

    objects = UserManager()
