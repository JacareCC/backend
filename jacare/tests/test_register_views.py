import pytest
import json
pytestmark = pytest.mark.django_db

class TestRegisterEndpoint:
    def test_succcessful_registration(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "uid": "new_test_uid",
            "email": "email@email.com"
        }
        #api call response from /register/ endpoint
        response = api_client().post("/register/", content_type='application/json', data=json.dumps(body))

        #check if the status code and response content are as expected
        assert response.status_code == 201
        assert "user registered successfully" in response.content.decode('utf-8').lower()
    
    def test_duplicate_uid_registration(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "uid": "test_6",
        }

        print(user.user_uid)

        #response from api call to /register/ endpoint  
        response = api_client().post("/register/", content_type='application/json', data=json.dumps(body))
        response_data = response.json()

        #check if status code and response content are as expected
        assert response.status_code == 400
        assert "user already registered" in response_data.get("error", "").lower()
        
    def test_deplicate_email_registration(self, user_factory, api_client):
        #user object to be used for test data, and body object to be used for request
        user = user_factory()
        body = {
            "uid": "new_test_uid",
            "email": "test@test.com",
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/register/", content_type='application/json', data=json.dumps(body))
        response_data = response.json()
        
        #check if status code and resposne content are as expected
        assert response.status_code == 400
        assert "email already registered" in response_data.get("error", "").lower()
    
    def test_missing_uid_registration(self, api_client):
        #object to be used for request
        body = {
            "email": "email@test.com",
        }

        #response from api call to /register/ endpoint
        response = api_client().post("/register/", content_type='application/json', data=json.dumps(body))
        response_data = response.json()
        
        #check if status code and resposne content are as expected
        assert response.status_code == 400
        assert "no uid found" in response_data.get("error", "").lower()