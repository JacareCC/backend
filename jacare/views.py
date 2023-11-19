from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, CustomerReviews, RestaurantUser, RestaurantsOwned, Restaurant
from firebase_admin import auth


@csrf_exempt
def authenticate_firebase_user(request):
    # Obter UID do usuário a partir do cabeçalho Authorization
    user_uid = request.headers.get("Authorization", '').split('Bearer ')[-1]

    firebase_token = auth.create_custom_token(user_uid)
    custom_token_str = firebase_token.decode('utf-8')

    if firebase_token:
        return JsonResponse({'custom_token': custom_token_str})
    else:
        return JsonResponse({'error': 'Failed to create custom token'}, status=500)
    # try:
    #     # verify token
    #     print(firebase_token)
        
    #     decoded_token = auth.verify_id_token(firebase_token)
    #     user_id = decoded_token['uid']
        
    #     # workspace
    #     # 

    #     return JsonResponse({'message': 'Custom token generated'})
    
    # except Exception as e:

    #     return JsonResponse({'error': str(e)}, status=401)

@csrf_exempt
def create_customer_review(request):
    # Adicione aqui a lógica para criar uma avaliação de cliente
    # Certifique-se de que o usuário esteja autenticado antes de criar a revisão

    # Exemplo simples de resposta JSON
    return JsonResponse({'message': 'Avaliação do cliente criada com sucesso!'})

# Adicione mais views conforme necessário para outras operações no seu banco de dados

# Exemplo de uma view que lista todos os clientes
@csrf_exempt
def list_customers(request):
    customers = Customer.objects.all()
    customer_list = [{'customer_uid': customer.customer_uid, 'first_name': customer.first_name, 'last_name': customer.last_name} for customer in customers]
    return JsonResponse({'customers': customer_list})
