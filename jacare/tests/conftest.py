from pytest_factoryboy import register
import pytest
from rest_framework.test import APIClient

from .factories import CustomerReviewsFactory
from user.tests.factories import UserFactory, PointsFactory
from business.tests.factories import RestaurantFactory

register(CustomerReviewsFactory)
register(UserFactory)
register(RestaurantFactory)
register(PointsFactory)

@pytest.fixture
def api_client():
    return APIClient