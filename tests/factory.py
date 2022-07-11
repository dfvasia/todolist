import factory.django

from core.models import User
from goals.models import GoalCategory, Board


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("name")
    password = "qwerty123"


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = "board_name"


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = "category"
    user_id = 1
    board = factory.SubFactory(BoardFactory)
