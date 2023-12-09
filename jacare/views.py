from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from rest_framework.decorators import api_view
from .models import CustomerReviews
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
    email = body["email"]

    user_exists = User.objects.filter(user_uid=uid).exists()

    if user_exists:
        return JsonResponse({"error": "User already registered"}, status=400)
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
            restaurant_review_data = CustomerReviews.objects.filter(restaurant_id=existing_restaurant).all()
            restaurant_review_list = list(restaurant_review_data.values())
            if restaurant_review_list:
                accessibility = 0
                customer_service = 0
                value_for_price = 0
                atmosphere = 0
                food_quality = 0
                for review in restaurant_review_list:
                    review.accessibility += accessibility
                    review.customer_service += customer_service
                    review.value_for_price += value_for_price
                    review.atmosphere += atmosphere
                    review.food_quality += food_quality
                num_reviews = len(restaurant_review_list)
                accessibility /= num_reviews
                customer_service /= num_reviews
                value_for_price /= num_reviews
                atmosphere /= num_reviews
                food_quality /= num_reviews
                accessibility_percentage = (accessibility / 5) * 100
                customer_service_percentage = (customer_service / 5) * 100
                value_for_price_percentage = (value_for_price / 5) * 100
                atmosphere_percentage = (atmosphere / 5) * 100
                food_quality_percentage = (food_quality / 5) * 100
                restaurant["accessibility"] = accessibility_percentage
                restaurant["customer_service"] = customer_service_percentage
                restaurant["value_for_price"] = value_for_price_percentage
                restaurant["food_quality"] = atmosphere_percentage
                restaurant["atmosphere"] = food_quality_percentage
            else:
                restaurant["accessibility"] = None
                restaurant["customer_service"] = None
                restaurant["value_for_price"] = None
                restaurant["food_quality"] = None
                restaurant["atmosphere"] = None
        else:
            new_restaurant = Restaurant(place_id=place_id, business_name=restaurant.get("displayName", {}).get("text"), location=restaurant.get("location", {}),claimed=False)
            new_restaurant.save()
            restaurant["place_id"] = new_restaurant.place_id
            restaurant["id"] = new_restaurant.id
            new_history = VisitedHistory(restaurant_id=new_restaurant, user_id=user)
            new_history.save()
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

    body = request.data
    cuisine_options = body.get("cuisineOptions", None)
    location = body.get("location", None)
    price = body.get("price", None)
    distance = body.get("distanceToTravel", 500)
    openNow = body.get("openNow", None)
    max_result_count = body.get("amountOfOptions", None)
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 
    user = User.objects.filter(user_uid=uid).first()

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
        "excludedPrimaryTypes": ["hotel", "resort_hotel", "department_store", "bar", "fast_food_restaurant", "coffee_shop", "ice_cream_shop"]
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
        formatted_results = format_data(weighted_results, user)
        return JsonResponse({"result": formatted_results}, status=200)
    else:
        return JsonResponse({"error": "Failed to fetch data from Google Places API"}, status=response.status_code)


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
        user_points_exists = Points.objects.filter(user_id=user).exists()
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




    