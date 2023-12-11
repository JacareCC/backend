from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from user.models import User, Points
from business.models import RegistrationRequests, Restaurant, TierReward
from jacare.models import CustomerReviews
# Create your views here.

#Endpoint for updating business profile
@api_view(["PATCH"])
@csrf_exempt
def update_business(request):
    if request.method == 'PATCH':
        body = request.data
        uid = request.headers.get("Authorization", "").split("Bearer ")[-1]
        user = User.objects.filter(user_uid=uid).first()
        restaurant_id = body.get("id", None)
        if user:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id, owner_user_id=user)
                restaurant.email = body.get("email", restaurant.email)
                restaurant.phone_number = body.get("phoneNumber", restaurant.phone_number)
                restaurant.contact_person = body.get("contactPerson", restaurant.contact_person)
                restaurant.save()
                return JsonResponse({'message': 'updated'}, status=200)
            except Restaurant.DoesNotExist:
                return JsonResponse({"error": "could not find restaurant"}, status=404)
        else:
            return JsonResponse({"message" : "Could not find user"}, status=404)
            

#Endpoint for creating a new registration request
@csrf_exempt 
@api_view(["POST"])
def new_registration_request(request):
    body = request.data 
    uid = body.get('user_uid', None)
    user = User.objects.filter(user_uid=uid).first()
    if user:
        registration = RegistrationRequests(
            user_id=user,
            first_name=body['first_name'],
            last_name=body['last_name'],
            business_name=body['business_name'],
            email=body['email'],
            contact_person=body['contact_person'],
            address=body['address'],
            phone_number=body['phone_number'],
        )
        registration.save()
        return JsonResponse({'message': 'Registration request created successfully'}, status=201)
    else: 
        return JsonResponse({"error": "failed to create registration request"}, status=500)

#Endpoint for verifying whether a user is owner of the business on business pages
@csrf_exempt
def verify_user(request, id):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1]
    user = User.objects.filter(user_uid=uid).first()
    business = Restaurant.objects.filter(user_id=user, id=id).exists()
    if business:
        return HttpResponse("verified", status=200)
    elif not business:
        return JsonResponse({"error": "not verified"}, status=400)
    elif not user:
        return JsonResponse({"error": "user not found"}, status=400)


    
#Endpoint for getting a user's businsses profile
@csrf_exempt
def get_business(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1]
    user = User.objects.filter(user_uid=uid).first()
    restaurant_data = Restaurant.objects.filter(owner_user_id=user).all()
    if restaurant_data:
        restaurant_list = list(restaurant_data.values())
        for restaurant in restaurant_list:
            reviews = CustomerReviews.objects.filter(restaurant_id=restaurant["id"]).all()
            rewards = TierReward.objects.filter(restaurant_id=restaurant["id"]).all()
            if reviews:
                restaurant["review"] = list(reviews.values())
            else:
                restaurant["review"] = "No reviews found"
            if rewards:
                restaurant["rewards"] = list(rewards.values())

            else: 
                restaurant["rewards"] = "No rewards found"

        return JsonResponse({"success": restaurant_list})
    else:
        return JsonResponse({"error": "No business found"}, status=404)

#Endpoint for specific business page
@csrf_exempt
def get_specific_business(request, id):
    business_id = id
    try:
        business = Restaurant.objects.get(id=business_id)
        try:
            business_tiers_data = TierReward.objects.filter(restaurant_id=business).all()
            business_tiers = list(business_tiers_data.values())
            rewards = business_tiers if business_tiers else "no rewards found"
            return JsonResponse({"success": {
                "name": business.business_name,
                "placeId": business.place_id,
                "rewards": rewards,
            }}, status=200)
        except TierReward.DoesNotExist:
            return JsonResponse({"error": "rewards not found"}, status=404)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": "could not find business"}, status=404)

#Endpoint for verifying reviews
@api_view(["PATCH"])
@csrf_exempt
def verify_review(request):
    if request.method == 'PATCH':
        body = request.data
        id = body.get("id", None)
        review = CustomerReviews.objects.filter(id=id).first()
        if review:
            review.isVerified = not review.isVerified
            review.save()
            user = review.user_id 
            user_points = Points.objects.filter(user_id=user).first()
            user_points.value += 5
            user_points.save()
        return JsonResponse({'success': 'Verified'}, status=200, safe=False)
    else:
        return JsonResponse({"error" : "failed to verify"}, status=404, safe=False)

#Endpoint for hiding and unhiding reviews
@api_view(["PATCH"])
@csrf_exempt
def hide_review(request):
    if request.method == 'PATCH':
        body = request.data
        id = body.get("id", None)
        review = CustomerReviews.objects.filter(id=id).first()
        if review:
            review.isHidden = not review.isHidden
            message = "Hidden" if review.isHidden else "Unhidden"
            review.save()
        return JsonResponse({'success': f'{message}'}, status=200, safe=False)
    else:
        return JsonResponse({"error" : "failed to execute"}, status=404, safe=False)


#Endpoint for restaurant owners getting all tiers for their restaurant 
@csrf_exempt
def get_all_tiers(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1] 
    user = User.objects.filter(user_uid=uid).first()
    restaurant = Restaurant.objects.filter(owner_user_id=user).first()
    data = TierReward.objects.filter(restaurant_id=restaurant).all()

    if data:
        tiers = list(data.values())
        return JsonResponse({"success": tiers}, status=200, safe=False)
    else: 
        return JsonResponse({"error": "failed to get tiers"}, status=500, safe=False)
    
#Endpoint for business creating a tier reward level
@api_view(["POST"])
@csrf_exempt
def new_tier_level(request):
    body = request.data
    id = body.get("id", None)
    restaurant_id = body.get("restaurant_id", None)
    user = User.objects.filter(id=id).first()
    restaurant = Restaurant.objects.filter(owner_user_id=user, id=restaurant_id).first()

    if restaurant:
        reward_level = body.get("tier", None)
        reward_description = body.get("description", None)
        points_required = body.get("points", None)
        refresh_in_days = body.get("refresh", None)
        refresh_date = timezone.now() + timedelta(days=refresh_in_days)
        tier = TierReward(reward_level=reward_level, reward_description=reward_description, points_required=points_required, restaurant_id=restaurant, refreshes_in=refresh_date)
        tier.save()
        return JsonResponse({"success": "tier created"}, status=201)
    else: 
        return JsonResponse({"error": "restaurant not found"}, status=404)
    
#Endpoint for business editing their tier
@api_view(["PATCH"])
@csrf_exempt
def edit_tier(request, id):
    if request.method == 'PATCH':
        body = request.data
        tier = TierReward.objects.get(id=id)
        if tier:
            tier.reward_level = body.get("tier", tier.reward_level)
            tier.reward_description = body.get("description", tier.reward_description)
            tier.points_required = body.get("cost", tier.points_required)
            refresh_in_days = body.get("refresh", tier.refreshes_in)
            refresh_date = timezone.now() + timedelta(days=refresh_in_days)
            tier.refreshes_in = refresh_date
            tier.save()
        return JsonResponse({'success': 'tier edited'}, status=200, safe=False)
    else:
        return JsonResponse({"error" : "failed to edit"}, status=404, safe=False)
    
#Endpoint for business deleting a tier reward level
@api_view(["DELETE"])
@csrf_exempt
def delete_tier_level(request, id):
    tier_id = id
    tier = TierReward.objects.get(id=tier_id)
    if tier:
        tier.delete()
        return JsonResponse({"sucess": "deleted"}, status=204)
    else:
        return JsonResponse({"error": "tier not found"}, status=404)