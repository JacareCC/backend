from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from user.models import User, Points
from business.models import RegistrationRequests, Restaurant, TierReward
from jacare.models import CustomerReviews
# Create your views here.

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
    
#Endpoint for businsses profile
@csrf_exempt
def get_business(request):
    uid = request.headers.get("Authorization", "").split('Bearer ')[-1]
    user = User.objects.filter(user_uid=uid).first()
    restaurant = Restaurant.objects.filter(owner_user_id=user).first()
    if restaurant:
        review_data = CustomerReviews.objects.filter(restaurant_id=restaurant).all()
        rewards_data = TierReward.objects.filter(restaurant_id=restaurant).all()
        if review_data:
            reviews = list(review_data.values())
        else:
            reviews = "No reviews found"
        if rewards_data:
            rewards = list(rewards_data.values())
        else: 
            rewards = "No rewards found"

        return JsonResponse({"success": {
            "name": restaurant.business_name,
            "email": restaurant.email,
            "phoneNumber": restaurant.phone_number,
            "representative": restaurant.contact_person,
            "address": restaurant.address,
            "rewardsSettings": rewards,
            "reviews": reviews
        }}, status=200)
    else:
        return JsonResponse({"error": "No business found"})
            

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
    uid = body.get("uid", None)
    user = User.objects.filter(user_uid=uid).first()
    restaurant = Restaurant.objects.filter(owner_user_id=user).first()

    if restaurant:
        reward_level = body.get("tier", None)
        reward_description = body.get("description", None)
        points_required = body.get("points", None)
        tier = TierReward(reward_level=reward_level, reward_description=reward_description, points_required=points_required, restaurant_id=restaurant)
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