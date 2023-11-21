from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer
from firebase_admin import auth


@csrf_exempt
def login_user(request):
    # Obter UID do usuário a partir do cabeçalho Authorization
    uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    print(user)
    

    user = Customer.objects.filter(customer_uid=uid).exists()
    
    if user:
        return JsonResponse({'success': 'Logged in'}, status=200)
    else: 
        return JsonResponse({'Error': 'Please register before loggin in'}, status=401)


# @csrf_exempt
# def register_user(request):
#     uid = request.headers.get("Authorization", '').split('Bearer ')[-1]
    
    



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
