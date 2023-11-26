import json

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.forms import (UserForm)

from app.models import User


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            form = UserForm(data)
        else:
            form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]

        return JsonResponse({'users': user_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': f'User with ID {user_id} deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with ID {user_id} does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)