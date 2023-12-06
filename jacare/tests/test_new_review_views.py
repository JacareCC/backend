import json
import pytest
pytestmark = pytest.mark.django_db

class TestNewReviewsEndpoint:
    def test_successful_review(self, points_factory, restaurant_factory, user_factory, api_client):
        #setup data needed for test
        user = user_factory()
        points = points_factory()
        restaurant = restaurant_factory()
        body = {
            "user_uid": user.user_uid,
            "restaurant_place_id": restaurant.id,
            "food": 5,
            "accessibility": 5,
            "atmosphere": 5
        }

        #response from api call to /review/new/
        response = api_client().post('/review/new/', content_type='application/json', data=json.dumps(body))

        #check if status code is as expected 
        assert response.status_code == 201