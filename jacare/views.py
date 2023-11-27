from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import User, Restaurant, visited_history, CustomerReviews
from firebase_admin import auth
import json
import requests
import os 
import random
import numpy as np
api_key = os.environ.get("API_KEY")

#This is a helper function to filter returned restaraunts from google
def filter_data(places, user_price, open_now=False):
    google_price_level = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }

    if open_now is True:
        result = [
            place for place in places
            if google_price_level.get(place.get("priceLevel"), 0) <= user_price and
                (place.get("currentOpeningHours", {}).get("openNow", False) if "currentOpeningHours" in place else False)
        ]
    else: 
        result = [
            place for place in places
            if google_price_level.get(place.get("priceLevel"), 0) <= user_price
        ]

    return result


#Endpoint for logging users in
@csrf_exempt
def login_user(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 

    user = User.objects.filter(user_uid=uid).exists()
    
    if user:
        return JsonResponse({"success": "Logged in"}, status=200)
    else: 
        return JsonResponse({"Error": "Please register before logging in"}, status=401)

#Endpoint for registering users 
@api_view(['POST'])
@csrf_exempt
def register_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid = body["uid"]

    user_exists = User.objects.filter(user_uid=uid).exists()

    if user_exists:
        return JsonResponse({"error": "User already registered"}, status=400)
    else:
        new_user = User(user_uid=uid)
        new_user.save()

        return JsonResponse({"success": "User registered successfully"}, status=201)
    
#Endpoint to query restaraunts from google 
@api_view(['POST'])
@csrf_exempt
def query_restaraurant(request):

    body = request.data
    cuisine_options = body.get("cuisineOptions", None)
    location = body.get("location", None)
    price = body.get("price", None)
    distance = body.get("distanceToTravel", None)
    openNow = body.get("openNow", None)
    max_result_count = body.get("amountOfOptions", None)

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
        "includedTypes": cuisine_options,
        # "maxResultCount": max_result_count,
        "locationRestriction": location_restriction,
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask":"places.location,places.displayName,places.priceLevel,places.currentOpeningHours,places.id"
    }

    response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=data, headers=headers)

    weight_array = []
    if response.status_code == 200:
        data = response.json()
        filtered_results = filter_data(data.get('places', []), price, openNow)
        for restaurant in filtered_results:
            weight = 0
            place_id = restaurant.get("id")
            existing_restaurant = Restaurant.objects.filter(place_id=place_id).first()
            review_count = len(CustomerReviews.objects.filter(restaurant_id=existing_restaurant).all())
            if review_count <= 25:
                weight += .4
            if review_count <= 50 and review_count > 25:
                weight += .3
            if review_count <= 75 and review_count > 50:
                weight += .2
            if review_count > 75:
                weight += .1
            if existing_restaurant and existing_restaurant.claimed is True:
                weight += .3
            if existing_restaurant and existing_restaurant.retaurant_level:
                weight += existing_restaurant.retaurant_level * .1
            weight_array.append(weight)

            if existing_restaurant:
                restaurant["id"] = existing_restaurant.id
                continue
            else:
                new_restaurant = Restaurant(place_id=place_id, business_name=restaurant.get("displayName", {}).get("text"), claimed=False)
                new_restaurant.save()
                restaurant["id"] = new_restaurant.id
        random_array_with_weight = []
        for weight in weight_array:
            new_weight = weight * random.randint(1,100)
            random_array_with_weight.append(new_weight)
      
        index_of_weights = sorted(range(len(random_array_with_weight)), key=lambda i: random_array_with_weight[i], reverse=True)[:max_result_count]
      

        results_for_fe = []
        for index in index_of_weights:
            results_for_fe.append(filtered_results[index])
        
        print(results_for_fe)
        return JsonResponse({"result": results_for_fe}, status=200)
    else:
        return JsonResponse({"error": "Failed to fetch data from Google Places API"}, status=response.status_code)


#Endpoint to retrieve specific restaraunt detail from db 
@csrf_exempt
def restaurant_detail(request, id): 
    restaurant = Restaurant.objects.filter(id=id).first()
    reviews = list(CustomerReviews.objects.filter(restaurant_id=id).all())
    data = {
        "reviews": reviews,
        "id": id,
        "place_id": restaurant.place_id,
        "name": restaurant.business_name,
    }
    if restaurant:
        return JsonResponse({"success": data}, status=200)
    else:
        return JsonResponse({"error": "no restaraunt found"}, status=500)

#Endpoint to retrieve visited history 
@csrf_exempt
def user_history(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 
    user = User.objects.filter(user_uid=uid).first()
    data = visited_history.objects.filter(user_id=user).all()
    history = list(data.values())
    if history:
        return JsonResponse({"success": history}, status=200)
    else:
        return JsonResponse({"error": "no history found "}, status=500)
    
#Endpoint to add to visited history
@api_view(['POST'])
@csrf_exempt
def add_to_user_history(request):  
    body = request.data
    restaurant_id = body.get('restaurant_id', None)
    user_uid = body.get('uid', None)

    user = User.objects.filter(user_uid=user_uid).first()
    restaurant = Restaurant.objects.filter(id=restaurant_id).first()
    
    if user: 
        new_history = visited_history(restaurant_id=restaurant, user_id=user)
        new_history.save()
        return HttpResponse("success", status=200)
    else: 
        return JsonResponse({"error": "failed to save history"}, status=500)


# @api_view(["POST"])
# @csrf_exempt
# def new_review(request):
#     body = request.data
    
    