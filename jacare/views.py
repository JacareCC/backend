from django.http import JsonResponse

def helloWorld(request):
    if request.method == 'GET':
        hello = { 'message': 'Hello World' }
        return JsonResponse(hello)