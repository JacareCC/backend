from pytest_factoryboy import register
import pytest
from rest_framework.test import APIClient

from .factories import CustomerReviewsFactory
from user.tests.factories import UserFactory

register(CustomerReviewsFactory)
register(UserFactory)

@pytest.fixture
def api_client():
    return APIClient