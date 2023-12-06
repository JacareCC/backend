from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User, VisitedHistory, UserTier, Points
from business.models import Restaurant, TierReward
from rest_framework.decorators import api_view
from django.core.serializers import serialize
# Create your views here.
    
#Endpoint for getting a user's profile
@csrf_exempt
def get_profile(request):
    uid = request.headers.get("Authorization", "").split("Bearer ")[-1]
    user = User.objects.filter(user_uid=uid).first()
    history_data = VisitedHistory.objects.filter(user_id=user).all()
    business_data = Restaurant.objects.filter(owner_user_id=user).all()
    
    if user:
        if list(history_data.values()):
            history = list(history_data.values())
            for restaurant in history:
                restaurant_data = Restaurant.objects.filter(id=restaurant["restaurant_id_id"])
                restaurant_detail = restaurant_data.values()
                restaurant["name"] = restaurant_detail[0]["business_name"]
        else:
            history = "No history found"
        try:
            points_data = Points.objects.get(user_id=user)
            points = points_data.value if points_data else None
        except Points.DoesNotExist:
            points = "No points found"
        if list(business_data.values()):
            business = list(business_data.values())
        else:
            business = "No businesses registered"
    
        return JsonResponse({"success": {
            "user": {
                "username": user.user_name,
                "email": user.email,
                "birthday": user.birthday,
            },
            "business": business,
            "history": history,
            "points": points
        }}, status=200)
    else:
        JsonResponse({"error": "No user found"})

#Endpoint for updating user's profile
@api_view(["PATCH"])
@csrf_exempt
def update_user(request):
    if request.method == 'PATCH':
        body = request.data
        uid = request.headers.get("Authorization", "").split("Bearer ")[-1]
        user = User.objects.filter(user_uid=uid).first()
        if user:
            user.user_name = body.get("username", user.user_name)
            user.birthday = body.get("birthday", user.birthday)
            user.email = body.get("email", user.email)
            user.save()

        return JsonResponse({'message': 'User updated'}, status=200)
    else:
        return JsonResponse({"message" : "Could not find user"}, status=404)

#Endpoint for getting user favorites
@csrf_exempt
def get_user_saved_restaurants(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 
    user = User.objects.filter(user_uid=uid).exists()
    data = VisitedHistory.objects.filter(user_id=user, saved=True).all()
    saved_restaurants = list(data.values())
    if saved_restaurants:
        for restaurant in saved_restaurants:
            data = Restaurant.objects.filter(id=restaurant["restaurant_id_id"])
            restaurant_detail = data.values()
            restaurant["name"] = restaurant_detail[0]["business_name"]
        return JsonResponse({"message": saved_restaurants})
    else:
        return JsonResponse({"message": "No saved restaurants"})
    
#Endpoint for adding or removing to user favorites
@api_view(["PATCH"])
@csrf_exempt
def change_user_saved_restaurants(request):
    if request.method == 'PATCH':
        body = request.data
        uid = body.get("uid", None)
        id = body.get("id", None)
        user = User.objects.filter(user_uid=uid).exists()
        restaurant_id = body.get("restaurantId", None)
        if user and restaurant_id:
            data = VisitedHistory.objects.filter(id=id, user_id=user, restaurant_id=restaurant_id)
            if data:
                data_to_update = data.first()
                data_to_update.saved = not data_to_update.saved
                data_to_update.save()

        return JsonResponse({'message': 'Restaurant removed from saved'}, status=200)
    else:
        return JsonResponse({"message" : "could not find user or restaurant"}, status=404)
    

#Endpoint for user getting all their tiers
@csrf_exempt
def get_all_user_tiers(request):
    uid = request.headers.get("Authorization ", " ").splice("Bearer ")[-1]
    user = User.objects.filter(user_uid=uid).first()
    if not user:
        return JsonResponse({"error": "user not found"}, status=404)
    data = UserTier.objects.filter(user_id=user).all()
    user_tiers = list(data.values())
    if user_tiers:
        for tier in user_tiers:
            restaurant = Restaurant.objects.filter(id=tier["restaurant_id_id"]).first()
            tier_level = TierReward.objects.filter(id=tier["tier_level_id"]).first()
            if restaurant and tier_level:
                tier["restaurant"] = {"id": restaurant.id, "name": restaurant.business_name}    
                tier["level"] = {"id": tier_level.id, "name": tier_level.reward_level, "reward": tier_level.reward_description}
                return JsonResponse({"success": user_tiers}, status=200)
    else: 
        return JsonResponse({"error": "no tiers found"}, status=404)