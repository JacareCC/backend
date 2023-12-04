from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import CustomerReviews
from user.models import User, Points, UserTier
from business.models import Restaurant, TierReward
import requests
import os 
import random
import json

api_key = os.environ.get("API_KEY")

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

#Helper function, adds weight to restaurants retrieved from google
def weight_data(restaurant_list, max_result_count):
    weight_array = []
    random_array_with_weight = []
    results_for_fe = []

    for restaurant in restaurant_list:
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
            restaurant["place_id"] = existing_restaurant.place_id
            tier_data = TierReward.objects.filter(restaurant_id=existing_restaurant).all()
            tier_array = list(tier_data.values())
            restaurant["tiers"] = tier_array
            continue
        else:
            new_restaurant = Restaurant(place_id=place_id, business_name=restaurant.get("displayName", {}).get("text"), claimed=False)
            new_restaurant.save()
            restaurant["place_id"] = new_restaurant.place_id
            restaurant["id"] = new_restaurant.id

    for weight in weight_array:
        new_weight = weight * random.randint(1,100)
        random_array_with_weight.append(new_weight)
      
    index_of_weights = sorted(range(len(random_array_with_weight)), key=lambda i: random_array_with_weight[i], reverse=True)[:max_result_count]
      
    for index in index_of_weights:
        results_for_fe.append(restaurant_list[index])
    return results_for_fe

#Endpoint to query restaraunts from google 
@api_view(['POST'])
@csrf_exempt
def query_restaraurant(request):

    body = request.data
    cuisine_options = body.get("cuisineOptions", None)
    location = body.get("location", None)
    price = body.get("price", None)
    distance = body.get("distanceToTravel", 500)
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

    json_data = {
        "includedTypes": cuisine_options,
        "locationRestriction": location_restriction,
        "excludedPrimaryTypes": ["hotel", "resort_hotel", "department_store"]
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask":"places.location,places.displayName,places.priceLevel,places.currentOpeningHours,places.id"
    }


    response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=json_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        filtered_results = filter_data(data.get('places', []), price, openNow)
        while len(filtered_results) < max_result_count and distance < 50000:
            distance *= 2
            location_restriction["circle"]["radius"] = distance
            response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=json_data, headers=headers)
            data = response.json()
            filtered_results = filter_data(data.get('places', []), price, openNow)
          
            
        weighted_results = weight_data(filtered_results, max_result_count)

        return JsonResponse({"result": weighted_results}, status=200)
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

#Endpoint for creating new review
@api_view(["POST"])
@csrf_exempt
def new_review(request):
    body = request.data
    restaurant_id = body.get('restaurant_place_id', None)
    user_uid = body.get('user_uid', None)
    user = User.objects.filter(user_uid=user_uid).first()
    restaurant = Restaurant.objects.filter(id=restaurant_id).first()

    if restaurant and user:
        new_review_made = CustomerReviews(user_id=user,restaurant_id=restaurant, data = body)
        new_review_made.save()
        user_points_exists = Points.objects(user_id=user).exists()
        if user_points_exists:
            user_points = Points.objects.filter(user_id=user).first()
            user_points.value += 1
            user_points.save()
        else:
            new_user_points = Points(user_id=user, value=1)
            new_user_points.save()
        return HttpResponse("success", status=201)
    else: 
        return JsonResponse({"error": "failed to save review"}, status=500)

#Endpoint for purchasing tiers with points
@api_view(["POST"])
@csrf_exempt
def purchase_tier(request):
    body = request.data
    tier_id = body.get("tierId", None)
    user_uid = body.get("uid", None)
    restaurant_id = body.get("restaurantId", None)
    restaurant = Restaurant.objects.filter(id=restaurant_id).first()
    user = User.objects.filter(user_uid=user_uid).first()
    tier = TierReward.objects.filter(id=tier_id).first()
    cost = tier.points_required
    tier_exists = UserTier.objects.filter(user_id=user, tier_level=tier, restaurant_id=restaurant).exists()

    if not user:
        return JsonResponse({"error": "user not found"}, status=404)
    elif not restaurant:
        return JsonResponse({"error": "restaurant not found"}, status=404)
    elif not tier:
        return JsonResponse({"error": "tier not found"}, status=404)
    elif tier_exists:
        return JsonResponse({"error": "user already has tier"}, status=404)
    else:
        user_points = Points.objects.filter(user_id=user).first()
        if user_points.value < cost:
            return JsonResponse({"error": "not enough points"}, status=404)
        else: 
            new_user_tier = UserTier(user_id=user, tier_level=tier, restaurant_id=restaurant)
            new_user_tier.save()
            user_points.value -= cost
            user_points.save()
            return JsonResponse({"success": "purchased new tier"}, status=201)




    