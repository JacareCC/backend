import pytest
import json
import random
pytestmark = pytest.mark.django_db

class TestSearchEndpoint:
    def test_successful_search(self, api_client, user_factory, restaurant_factory, customer_reviews_factory):
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /search/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')

        #checking if status code is as expected
        assert response.status_code == 200

    def test_missing_body(self, api_client, user_factory):
        #user object to be used for test data 
        user = user_factory

        #response from api call to /search/ endpoint
        response = api_client().post("/search/", content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #checking if status code and content body are as expected
        assert response.status_code == 400
        assert "Search parameters not found" in response_data.get("error", "")

    def test_missing_uid(self, api_client):
        #object to be used for request
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/register/", content_type='application/json', data=json.dumps(body))
        response_data = response.json()

        #check if status code and resposne content are as expected
        assert response.status_code == 400
        assert "no uid found" in response_data.get("error", "").lower()
    
    def test_rural_location(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": -163.472214,
                "latitude": 37.548803
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        print(response_data)
        #check if status code and response content are as expected
        assert response.status_code == 200
    
    def test_invalid_location_type(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": "test",
                "latitude": "test"
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 400
        assert "invalid location" in response_data.get("error", "").lower()

    def test_missing_location(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 400
        assert "location not found" in response_data.get("error", "").lower()
    
    def test_missing_cuisine_options(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 400
        assert "cuisineOptions not found" in response_data.get("error", "")
    
    def test_missing_amount_options(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 4,
            "distance": 1000,
            "openNow": False,
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 400
        assert "amountOfOptions not found" in response_data.get("error", "")
    
    def test_missing_distance(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 4,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 200
    
    def test_different_prices(self, user_factory, api_client):
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": random.randint(0, 4),
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /search/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')

        #checking if status code is as expected
        assert response.status_code == 200
    
    def test_invalid_price(self, user_factory, api_client):
        user = user_factory()
        body = {
            "cuisineOptions": "restaurant",
            "location": {
                "longitude": 139.7345,
                "latitude": 35.6619
            },
            "price": 100,
            "distance": 1000,
            "openNow": False,
            "amountOfOptions": 5
        }

        #response from api call to /search/ endpoint
        response = api_client().post("/search/", content_type='application/json', data=json.dumps(body), HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')
        response_data = response.json()
        #checking if status code is as expected
        assert response.status_code == 400
        assert "price is out of range" in response_data.get("error", "")
