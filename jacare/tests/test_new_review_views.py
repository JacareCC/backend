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

    def test_no_data_review(self, points_factory, restaurant_factory, user_factory, api_client):
        #setup data needed for test
        user = user_factory()
        points = points_factory()
        restaurant = restaurant_factory()


        #resposne from api called to /review/new/
        response = api_client().post('/review/new/', content_type='application/json', data=None)

        #check if status code is as expected
        assert response.status_code == 400 
    
    def test_invalid_user_review(self, points_factory, restaurant_factory, user_factory, api_client):
       #setup data needed for test
        user = user_factory()
        points = points_factory()
        restaurant = restaurant_factory()
        body = {
            "user_uid": "invalid user",
            "restaurant_place_id": restaurant.id,
            "food": 5,
            "accessibility": 5,
            "atmosphere": 5
        }

        #response from api call to /review/new/
        response = api_client().post('/review/new/', content_type='application/json', data=json.dumps(body))
        response_data = response.json()

        #check if status code is as expected 
        assert response.status_code == 400
        assert "no user found" in response_data.get("error", "") 
    
        
    def test_invalid_restaurant_review(self, points_factory, restaurant_factory, user_factory, api_client):
       #setup data needed for test
        user = user_factory()
        points = points_factory()
        restaurant = restaurant_factory()
        body = {
            "user_uid": user.user_uid,
            "restaurant_place_id": 10000,
            "food": 5,
            "accessibility": 5,
            "atmosphere": 5
        }

        #response from api call to /review/new/
        response = api_client().post('/review/new/', content_type='application/json', data=json.dumps(body))
        response_data = response.json()

        #check if status code is as expected 
        assert response.status_code == 400
        assert "no restaurant found" in response_data.get("error", "") 