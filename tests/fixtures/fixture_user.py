import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        middle_name="TestUser",
        last_name="TestUser",
        first_name="TestUser",
        password="510765_kaka",
        id_admin=True,
    )


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        "access": str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client
