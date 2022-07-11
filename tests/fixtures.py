import pytest

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment

T_USERNAME = "Vasia"
T_USERNAME_TWO = "user_2"
USER_PASSWORD = "qwerty123"
EMAIL = 'admin@admin.ru'
EMAIL_2 = 'admin2@admin.ru'
F_NAME = 'User'
CATEGORY_NAME = "category name"
CATEGORY_NAME_2 = "category name 2"
GOAL_NAME = "name"
GOAL_NAME_2 = "name 2"
DUE_DATE = "2022-07-11"
COMMENT_TEXT = "comment"
COMMENT_TEXT_2 = "comment 2"


@pytest.fixture()
@pytest.mark.django_db
def user1(client, django_user_model):
    return django_user_model.objects.create_user(
        username=T_USERNAME,
        password=USER_PASSWORD,
        email=EMAIL,
        first_name=F_NAME,
        last_name=F_NAME
    )


@pytest.fixture()
@pytest.mark.django_db
def user2(client, django_user_model):
    return django_user_model.objects.create_user(
        username=T_USERNAME_TWO,
        password=USER_PASSWORD,
        email=EMAIL_2,
        first_name=F_NAME,
        last_name=F_NAME
    )


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user(client, user1):
    client.login(username=user1.username, password=USER_PASSWORD)
    return user1


@pytest.fixture()
@pytest.mark.django_db
def logged_in_user2(client, user2):
    client.login(username=T_USERNAME_TWO, password=USER_PASSWORD)
    return user2


@pytest.fixture()
@pytest.mark.django_db
def board(client):
    board_name = "Testing board name"
    return Board.objects.create(title=board_name)


@pytest.fixture()
@pytest.mark.django_db
def board2(client):
    board_name = "Testing board name 2"
    return Board.objects.create(title=board_name)


@pytest.fixture()
@pytest.mark.django_db
def category_for_user1(client, user1, board, board_part_user1_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture()
@pytest.mark.django_db
def goal_for_category_user2_user1_writer(client, category_for_board_user2_user1_writer):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_writer,
        due_date=DUE_DATE
    )


def make_categories(user, board):
    category = GoalCategory.objects.create(title=CATEGORY_NAME, user=user, board=board)
    category_2 = GoalCategory.objects.create(title=CATEGORY_NAME_2, user=user, board=board)
    return category, category_2


def make_goals(category):
    goal = Goal.objects.create(title=GOAL_NAME, category=category, due_date=DUE_DATE)
    goal_2 = Goal.objects.create(title=GOAL_NAME_2, category=category, due_date=DUE_DATE)
    return goal, goal_2


def make_comments(goal, user):
    comment = GoalComment.objects.create(text=COMMENT_TEXT, goal=goal, user=user)
    comment_2 = GoalComment.objects.create(text=COMMENT_TEXT_2, goal=goal, user=user)
    return comment, comment_2


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user1(client, user1, board, board_part_user1_owner):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user2_user1_reader(
        client, user1, board, board_part_user2_owner, board_part_user1_reader
):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def categories_for_user2_user1_writer(client, user1, board, board_part_user1_writer, board_part_user2_owner):
    return make_categories(user1, board)


@pytest.fixture()
@pytest.mark.django_db
def board_part_user1_owner(client, board, user1):
    return BoardParticipant.objects.create(board=board, user=user1)


@pytest.fixture()
@pytest.mark.django_db
def board_part_board2_user1_owner(client, board2, user1):
    return BoardParticipant.objects.create(board=board2, user=user1)


@pytest.fixture()
@pytest.mark.django_db
def board_part_user2_owner(client, board, user2):
    return BoardParticipant.objects.create(board=board, user=user2)


@pytest.fixture()
@pytest.mark.django_db
def board_part_user1_reader(client, board, user1):
    return BoardParticipant.objects.create(board=board, user=user1, role=BoardParticipant.Role.reader)


@pytest.fixture()
@pytest.mark.django_db
def board_part_board2_user1_reader(client, board2, user1):
    return BoardParticipant.objects.create(board=board2, user=user1, role=BoardParticipant.Role.reader)


@pytest.fixture()
@pytest.mark.django_db
def board_part_user1_writer(client, board, user1):
    return BoardParticipant.objects.create(board=board, user=user1, role=BoardParticipant.Role.writer)


@pytest.fixture()
@pytest.mark.django_db
def category_for_user2(client, board, user2, board_part_user2_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user2, board=board)


@pytest.fixture()
@pytest.mark.django_db
def category_for_board_user2_user1_reader(client, board, user1, user2, board_part_user1_reader):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture()
@pytest.mark.django_db
def category_for_board_user2_user1_writer(client, board, user1, user2, board_part_user1_writer):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)
