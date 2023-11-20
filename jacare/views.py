from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, CustomerReviews, RestaurantUser, RestaurantsOwned, Restaurant
from firebase_admin import auth


@csrf_exempt
def authenticate_firebase_user(request):

    user_uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    print(user_uid)
    

    firebase_token = auth.create_custom_token(user_uid)
    custom_token_str = firebase_token.decode('utf-8')

    if firebase_token:
        return JsonResponse({'custom_token': custom_token_str})
    else:
        return JsonResponse({'error': 'Failed to create custom token'}, status=500)


@csrf_exempt
def create_customer_review(request):

    return JsonResponse({'message': 'Avaliação do cliente criada com sucesso!'})


@csrf_exempt
def list_customers(request):
    customers = Customer.objects.all()
    customer_list = [{'customer_uid': customer.customer_uid, 'first_name': customer.first_name, 'last_name': customer.last_name} for customer in customers]
    return JsonResponse({'customers': customer_list})
