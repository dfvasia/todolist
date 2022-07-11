from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_get_profile(client, logged_in_user):

    expected_response = {
        "id": logged_in_user.id,
        "username": "Vasia",
        "first_name": "User",
        "last_name": "User",
        "email": "admin@admin.ru"
    }

    response = client.get(
        "/core/profile",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response
