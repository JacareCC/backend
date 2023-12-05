# import pytest
# import requests
# from requests.exceptions import RequestException
# from requests_mock.contrib import fixture

# BASE_URL = 'http://localhost:8000/user/'


# # #history function tests

# def test_get_all_user_tiers_without_uid():
#     response = requests.get(BASE_URL + 'history')
#     assert response.status_code == 500

# def test_add_to_user_history_with_fake_data():
#     fake_data = {
#         'restaurant_id': 'fake_restaurant_id',
#         'uid': 'fake_user_uid',
#     }
#     response = requests.post(BASE_URL + 'history/add/', data=fake_data)
#     assert response.status_code == 500



# # @pytest.fixture
# # def mock_request():
# #     with fixture.Fixture() as mock:
# #         yield mock

# # @pytest.mark.django_db
# # def test_add_to_user_history(mock_request):
# #     fake_data = {
# #         'restaurant_id': 'fake_restaurant_id',
# #         'user_uid': 'fake_user_uid',
# #     }

# #     # Configurando o mock para simular a chamada HTTP
# #     mock_request.post(BASE_URL + 'history/add/', text="success", status_code=201)

# #     response = requests.post(BASE_URL + 'history/add/', data=fake_data)

# #     # Verificando se a chamada HTTP foi feita corretamente
# #     assert mock_request.called

# #     # Verificando se a resposta é a esperada
# #     assert response.status_code == 201

# #     # Adicione mais asserções conforme necessário



# #     # if response.status_code == 201:
# #     #     print(f"Fake add successful with status code {status_code}")
# #     # else:
# #     #     print(f"Fake add failed with status code {response.status_code}")

    

# # # Restante do seu teste...

# # # def test_call_endpoints_without_auth():S
# # #     tier_all = requests.get(ENDPOINT + 'tier/all/')
# # #     assert tier_all.status_code == 404

# # #     favorites_all = requests.get(ENDPOINT + 'favorites/all')
# # #     assert favorites_all.status_code == 404

# # #     historu = requests.get(ENDPOINT + 'history/')
# # #     assert favorites_all.status_code == 404


# #     # path('history/', user_history),
# #     # path('history/add/', add_to_user_history),
# #     # path('tier/all/', get_all_user_tiers),
# #     # path('favorites/all', get_user_saved_restaurants),
# #     # path('favorites/add/', change_user_saved_restaurants),
# #     # path('favorites/remove/', change_user_saved_restaurants),

# # # import json
# # # from django.test import Client
# # # import pytest
# # # from user.models import User, VisitedHistory
# # # from business.models import Restaurant

# # # @pytest.mark.django_db
# # # def test_user_history(api_client, user_factory, visited_history_factory, restaurant_factory):

# # #     user = user_factory()
# # #     history_entry = visited_history_factory(user_id=user)
# # #     restaurant = restaurant_factory()
# #     history_entry.restaurant_id = restaurant
# #     history_entry.save()

# #     response = api_client.get(ENDPOINT_HISTORY)

# #     assert response.status_code == 200
# #     data = response.json()

# #     assert "success" in data

# #     assert "name" in data["success"][0]

