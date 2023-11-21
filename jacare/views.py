from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Customer
from firebase_admin import auth


@csrf_exempt
def login_user(request):
    uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    print(user)
    

    user = Customer.objects.filter(customer_uid=uid).exists()
    
    if user:
        return JsonResponse({'success': 'Logged in'}, status=200)
    else: 
        return JsonResponse({'Error': 'Please register before loggin in'}, status=401)

@api_view(['POST'])
@csrf_exempt
def register_user(request):
    uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    
    user_exists = Customer.objects.filter(customer_uid=uid).exists()

    if user_exists:
        return JsonResponse({'error': 'User already registered'}, status=400)
    else:
        new_user = Customer(customer_uid=uid)
        new_user.save()

        return JsonResponse({'success': 'User registered successfully'}, status=201)
    
