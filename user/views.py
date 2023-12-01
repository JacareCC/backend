from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User, VisitedHistory, UserTier, Points
from business.models import Restaurant, TierReward
from rest_framework.decorators import api_view
# Create your views here.

#Endpoint to retrieve visited history 
@csrf_exempt
def user_history(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 
    user = User.objects.filter(user_uid=uid).first()
    data = VisitedHistory.objects.filter(user_id=user).all()
    history = list(data.values())
    if history:
        for restaurant in history:
            data = Restaurant.objects.filter(id=restaurant["restaurant_id_id"])
            restaurant_detail = data.values()
            restaurant["name"] = restaurant_detail[0]["business_name"]
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
        new_history = VisitedHistory(restaurant_id=restaurant, user_id=user)
        new_history.save()
        return HttpResponse("success", status=201)
    else: 
        return JsonResponse({"error": "failed to save history"}, status=500)
    
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