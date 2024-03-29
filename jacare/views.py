from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from rest_framework.decorators import api_view
from .models import CustomerReviews, CheckinHistory
from user.models import User, Points, UserTier, VisitedHistory
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
        return HttpResponse("Login successful", status=200)
    else: 
        return HttpResponse("Authentication required", status=401)
    

#Endpoint for registering users 
@api_view(['POST'])
@csrf_exempt
def register_user(request):
    body = request.data
    uid = body.get("uid", None)
    email = body.get("email", None) 
        
    user_exists = User.objects.filter(user_uid=uid).exists()
    email_exists = User.objects.filter(email=email).exists()

    if not uid:
        return JsonResponse({"error": "No uid found"}, status=400)
    if user_exists:
        return JsonResponse({"error": "User already registered"}, status=400)
    if email_exists:
        return JsonResponse({"error": "Email already registered"}, status=400)
    else:
        new_user = User(user_uid=uid, email=email)
        new_user.save()
        points = Points(user_id=new_user, value=0)
        points.save()
        return JsonResponse({"success": "User registered successfully"}, status=201)
    
#This is a helper function to format result data 
def format_data(restaurant_list, user):
    for restaurant in restaurant_list:
        place_id = restaurant.get("id")
        existing_restaurant = Restaurant.objects.filter(place_id=place_id).first()
        if existing_restaurant:
            restaurant["id"] = existing_restaurant.id
            restaurant["place_id"] = existing_restaurant.place_id
            tier_data = TierReward.objects.filter(restaurant_id=existing_restaurant).all()
            tier_array = list(tier_data.values())
            restaurant["tiers"] = tier_array 
            new_history = VisitedHistory(restaurant_id=existing_restaurant, user_id=user)
            new_history.save()
        else:
            new_restaurant = Restaurant(place_id=place_id, business_name=restaurant.get("displayName", {}).get("text"), location=restaurant.get("location", {}),claimed=False)
            new_restaurant.save()
            restaurant["place_id"] = new_restaurant.place_id
            restaurant["id"] = new_restaurant.id
            new_history = VisitedHistory(restaurant_id=new_restaurant, user_id=user)
            new_history.save()
    return restaurant_list

#This is a helper function to format result data if there is no user
def format_data_no_user(restaurant_list):
    for restaurant in restaurant_list:
        place_id = restaurant.get("id")
        existing_restaurant = Restaurant.objects.filter(place_id=place_id).first()
        if existing_restaurant:
            restaurant["id"] = existing_restaurant.id
            restaurant["place_id"] = existing_restaurant.place_id
            tier_data = TierReward.objects.filter(restaurant_id=existing_restaurant).all()
            tier_array = list(tier_data.values())
            restaurant["tiers"] = tier_array 
        else:
            new_restaurant = Restaurant(place_id=place_id, business_name=restaurant.get("displayName", {}).get("text"), location=restaurant.get("location", {}),claimed=False)
            new_restaurant.save()
            restaurant["place_id"] = new_restaurant.place_id
            restaurant["id"] = new_restaurant.id
    return restaurant_list

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

    for weight in weight_array:
        new_weight = weight * random.randint(1,100)
        random_array_with_weight.append(new_weight)

    if len(restaurant_list) < max_result_count:  
        index_of_weights = sorted(range(len(random_array_with_weight)), key=lambda i: random_array_with_weight[i], reverse=True)[:len(restaurant_list)]
    else:
        index_of_weights = sorted(range(len(random_array_with_weight)), key=lambda i: random_array_with_weight[i], reverse=True)[:max_result_count]    
      
    for index in index_of_weights:
        results_for_fe.append(restaurant_list[index])
    return results_for_fe

#Endpoint to query restaraunts from google 
@api_view(['POST'])
@csrf_exempt
def query_restaraurant(request):
    body = request.data if request.data else None
    if not body:
        return JsonResponse({"error": "Search parameters not found"}, status=400)
    
    cuisine_options = body.get("cuisineOptions", None)
    location = body.get("location", None)
    price = body.get("price", None)
    distance = body.get("distanceToTravel", 500)
    openNow = body.get("openNow", None)
    max_result_count = body.get("amountOfOptions", None)
    uid = request.headers.get("Authorization", None).split('Bearer ')[-1] 
    user = None

    if uid:
        user = User.objects.filter(user_uid=uid).first()

    if not cuisine_options:
        return JsonResponse({"error": "cuisineOptions not found"}, status=400)
    
    if type(price) is not int:
        return JsonResponse({"error": "price not found"}, status=400)
    
    if price < 0 or price > 4:
        return JsonResponse({"error": "price is out of range"}, status=400)

    if not max_result_count:
        return JsonResponse({"error": "amountOfOptions not found"}, status=400)
    
    if location:
        if type(location["longitude"]) is float and type(location["latitude"]) is float:
            location_restriction = { 
                "circle": {
                    "center": {
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                    },
                "radius": distance
                }   
            }
        else:
            return JsonResponse({"error": "Invalid location"}, status=400)
    else:
        return JsonResponse({"error": "Location not found"}, status=400)

    json_data = {
        "includedTypes": cuisine_options,
        "locationRestriction": location_restriction,
        "excludedPrimaryTypes": ["hotel", "resort_hotel", "department_store", "bar", "fast_food_restaurant", "coffee_shop", "ice_cream_shop"]
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask":"places.location,places.displayName,places.priceLevel,places.currentOpeningHours,places.id"
    }

    ## set keys or strings to variables in order to avoid typos. variable names will throw errors but string will not
    ## make as many things into variables to be more readable.
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
        if user:
            formatted_results = format_data(weighted_results, user)
        elif not user:
            formatted_results = format_data_no_user(weighted_results)
        return JsonResponse({"result": formatted_results}, status=200)
    else:
        return JsonResponse({"error": "Failed to fetch data from Google Places API"}, status=response.status_code)


#Endpoint for creating new review
#Error handling might only be necessary on the frontend unless there is a specific use case
@api_view(["POST"])
@csrf_exempt
def new_review(request):
    body = request.data
    if not body:
        return JsonResponse({"error": "no body found"}, status=400)
    
    restaurant_id = body.get('restaurant_place_id', None)
    user_uid = body.get('user_uid', None)
    user = User.objects.filter(user_uid=user_uid).first()
    restaurant = Restaurant.objects.filter(id=restaurant_id).first()

    if not user:
        return JsonResponse({"error": "no user found"}, status=400)
    
    if not restaurant:
        return JsonResponse({"error": "no restaurant found"}, status=400)
    
    new_review_made = CustomerReviews(user_id=user,restaurant_id=restaurant, data = body)
    new_review_made.save()
    user_points_exists = Points.objects.filter(user_id=user).exists()
    if user_points_exists:
        user_points = Points.objects.filter(user_id=user).first()
        user_points.value += 1
        user_points.save()
    else:
        new_user_points = Points(user_id=user, value=1)
        new_user_points.save()
    return HttpResponse("success", status=201)

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
    tier_exists = UserTier.objects.filter(user_id=user, tier=tier, restaurant_id=restaurant).first()

    if not user:
        return JsonResponse({"error": "user not found"}, status=404)
    elif not restaurant:
        return JsonResponse({"error": "restaurant not found"}, status=404)
    elif not tier:
        return JsonResponse({"error": "tier not found"}, status=404)
    elif tier_exists and not tier_exists.has_refreshed():
        return JsonResponse({"error": "reward has not refreshed yet"}, status=400)
    else:
        user_points = Points.objects.filter(user_id=user).first()
        if not user_points:
            return JsonResponse({"error": "no points found"}, status=404)
        if user_points.value < cost:
            return JsonResponse({"error": "not enough points"}, status=404)
        else: 
            new_user_tier = UserTier(user_id=user, tier=tier, restaurant_id=restaurant)
            new_user_tier.save()
            user_points.value -= cost
            user_points.save()
            return JsonResponse({"success": "purchased new tier"}, status=201)


@csrf_exempt
@api_view(['POST'])
def check_in(request):
    body = request.data 
    user_uid = body.get("uid", None)
    restaurant_id = body.get("restaurant_id", None)
    user = User.objects.get(user_uid=user_uid).first()
    restaurant = Restaurant.objects.get(id=restaurant_id).first()
    if not user:
        return JsonResponse({"error": "user not found"}, status=400)
    if not restaurant:
        return JsonResponse({"error": "restaurant not found"}, status=400)
    
    checkin = CheckinHistory(user=user, restaurant=restaurant)
    checkin.save()
    return JsonResponse({"success": "checked in"}, status=201)




    