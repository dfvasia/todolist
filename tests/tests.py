from http import HTTPStatus
import pytest
from goals.models import GoalCategory, Board, BoardParticipant
from goals.serializers import GoalCategorySerializer


CATEGORY_NAME = 'category_name'



@pytest.mark.django_db
def test_get_all_owner(
        client,
        logged_in_user,
        categories_for_user1
):
    category_1, category_2 = categories_for_user1

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get('/goals/goal_category/list')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_allowed_reader(
        client,
        logged_in_user,
        user2,
        categories_for_user2_user1_reader
):
    category_1, category_2 = categories_for_user2_user1_reader

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get('/goals/goal_category/list')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_allowed_writer(
        client,
        logged_in_user,
        user2,
        categories_for_user2_user1_writer
):
    category_1, category_2 = categories_for_user2_user1_writer

    expected_response = [
        GoalCategorySerializer(category_1).data,
        GoalCategorySerializer(category_2).data,
    ]
    response = client.get('/goals/goal_category/list')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_owner(
        client,
        logged_in_user,
        category_for_user1
):
    category = category_for_user1
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f'/goals/goal_category/{category.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_forbidden_user_rights(
        client,
        logged_in_user,
        category_for_user2
):
    category = category_for_user2

    response = client.get(f'/goals/goal_category/{category.id}')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_get_one_allowed_reader(
        client,
        logged_in_user,
        category_for_board_user2_user1_reader
):
    category = category_for_board_user2_user1_reader
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f'/goals/goal_category/{category.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_one_allowed_writer(
        client,
        logged_in_user,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    expected_response = GoalCategorySerializer(category).data

    response = client.get(f'/goals/goal_category/{category.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_not_found(client, logged_in_user):
    response = client.get('/goals/goal_category/1000')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_not_found_for_user_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    category = category_for_user2
    response = client.get(f'/goals/goal_category/{category.id}')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_create_owner(client, logged_in_user):
    category_name = 'Testing category name'
    board_name = 'Testing board name'
    board = Board.objects.create(title=board_name)
    BoardParticipant.objects.create(board=board, user=logged_in_user)

    data = {
        'title': category_name,
        'board': board.id
    }

    response = client.post(
        f'/goals/goal_category/create',
        data,
        content_type='application/json'
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_create_allowed_writer(
        client,
        logged_in_user,
        user2,
        board,
        category_for_board_user2_user1_writer
):
    category_name = 'Testing category name'

    data = {
        'title': category_name,
        'board': board.id
    }

    response = client.post(
        f'/goals/goal_category/create',
        data,
        content_type='application/json'
    )

    assert response.status_code == HTTPStatus.CREATED


def get_patch_response(client, category):
    return client.patch(
        f'/goals/goal_category/{category.id}',
        {'title': CATEGORY_NAME},
        content_type='application/json'
    )


@pytest.mark.django_db
def test_partial_update_owner(client, logged_in_user, category_for_user1):
    category = category_for_user1

    expected_response = GoalCategorySerializer(category).data
    expected_response['title'] = CATEGORY_NAME

    response = get_patch_response(client, category)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop('updated')
    expected_response.pop('updated')

    assert response_json == expected_response


@pytest.mark.django_db
def test_partial_update_forbidden_user_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    response = get_patch_response(client, category_for_user2)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_partial_update_forbidden_reader(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_reader
):
    response = get_patch_response(client, category_for_board_user2_user1_reader)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_update_allowed_writer(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    response = get_patch_response(client, category)

    expected_response = GoalCategorySerializer(category).data
    expected_response['title'] = CATEGORY_NAME

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop('updated')
    expected_response.pop('updated')

    assert response_json == expected_response


@pytest.mark.django_db
def test_delete_owner(
        client,
        logged_in_user,
        category_for_user1
):
    category = category_for_user1
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True


@pytest.mark.django_db
def test_delete_forbidden_user_rights(
        client,
        logged_in_user,
        user2,
        category_for_user2
):
    category = category_for_user2
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_forbidden_reader(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_reader
):
    category = category_for_board_user2_user1_reader
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_allowed_writer(
        client,
        logged_in_user,
        user2,
        category_for_board_user2_user1_writer
):
    category = category_for_board_user2_user1_writer
    url = f'/goals/goal_category/{category.id}'

    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    category_is_deleted = GoalCategory.objects.get(id=category.id)
    assert category_is_deleted.is_deleted is True
