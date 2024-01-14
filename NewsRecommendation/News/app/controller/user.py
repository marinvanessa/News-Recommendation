import json

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from ..forms.user import (UserCreationForm)
from django.contrib.auth.decorators import login_required
from ..models.user import CustomUser
from django.contrib.sessions.models import Session

from django.db.models import Max


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # Get all users
        users = CustomUser.objects.all()

        # Check if there's a user with the provided username and password
        user = None
        for u in users:
            if u.username == username and check_password(password, u.password):
                user = u
                break

        if user is not None:
            request.session['user_id'] = user.id

            login(request, user)
            # Send the redirect URL in the JSON response
            redirect_url = reverse('get_all_news')  # Change this to the correct URL name
            return JsonResponse({'message': 'Login successful', 'user_id': user.id, 'redirect_url': redirect_url})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    elif request.method == 'GET':
        # Render the login page or redirect to it
        return render(request, 'app/login.html')

    else:
        return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            form = UserCreationForm(data)
        else:
            form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # Redirect to the login page after successful registration
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    elif request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'app/register.html', {'form': form})

    return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)


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


@csrf_exempt
def get_user_by_id(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            user_data = {'id': user.id, 'username': user.username}
            return JsonResponse({'user': user_data})
        except User.DoesNotExist:
            return HttpResponseNotFound('User not found')
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def delete_all_users(request):
    if request.method == 'DELETE':
        try:
            CustomUser.objects.all().delete()
            return JsonResponse({'message': 'All users deleted successfully'})
        except Exception as e:
            return HttpResponseServerError(f'Error deleting users: {str(e)}')
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
