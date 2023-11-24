from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Customer
from firebase_admin import auth
import json
import requests
import os 
api_key = os.environ.get("API_KEY")

def filter_by_price(places, userPrice):
    google_price_level = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }

    filtered_places = [
        place for place in places
        if google_price_level.get(place.get('priceLevel'), 0) <= userPrice
    ]

    return filtered_places

@csrf_exempt
def login_user(request):
    uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    print(uid)  

    user = Customer.objects.filter(customer_uid=uid).exists()
    print(user)
    
    if user:
        return JsonResponse({'success': 'Logged in'}, status=200)
    else: 
        return JsonResponse({'Error': 'Please register before logging in'}, status=401)

@api_view(['POST'])
@csrf_exempt
def register_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid = body['uid']
    print(uid)
    
    
    user_exists = Customer.objects.filter(customer_uid=uid).exists()

    if user_exists:
        return JsonResponse({'error': 'User already registered'}, status=400)
    else:
        new_user = Customer(customer_uid=uid)
        new_user.save()

        return JsonResponse({'success': 'User registered successfully'}, status=201)
    
@api_view(['POST'])
def query_restaraurant(request):

    body = request.data
    cuisine_type = body.get('cuisineType', None)
    location = body.get('location', None)
    price = body.get('price', None)
    distance = body.get('distanceToTravel', None)
    max_result_count = body.get('amountOfOptions', None)
    openNow = body.get('openNow', None)

    location_restriction = { 
            "circle": {
                "center": {
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                },
            "radius": distance
        }   
    }

    data = {
        "includedTypes": [cuisine_type],
        "maxResultCount": max_result_count,
        "locationRestriction": location_restriction,
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask":"places.displayName,places.priceLevel"
    }

    response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        filtered_results = filter_by_price(data.get('places', []), price)
        return JsonResponse({"result": filtered_results}, status=200)
    else:
        return JsonResponse({'error': 'Failed to fetch data from Google Places API'}, status=response.status_code)
