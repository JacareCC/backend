import pytest
pytestmark = pytest.mark.django_db

class TestAppViews:
    def test_successful_login(self, user_factory, api_client):
        #user object to be used for test data
        user = user_factory()

        #api call response from /login/ endpoint
        response = api_client().get("/login/", HTTP_AUTHORIZATION=f'Bearer {user.user_uid}')

        #check if status code and response content are as expected
        assert response.status_code == 200
        assert 'login successful' in response.content.decode('utf-8').lower()

    def test_login_with_no_header(self, user_factory, api_client):
        #user object to be used for test data
        user = user_factory()

        #api call response from /login/ endpoint
        response = api_client().get("/login/")

        #check if status code and reponse content are as expected
        assert response.status_code == 401
        assert 'authentication required' in response.content.decode('utf-8').lower()
    
        


    
