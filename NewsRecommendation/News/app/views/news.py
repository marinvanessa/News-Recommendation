import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from ..forms.news import (NewsForm)
from ..models.news import News
from ..models.likes import UserLikes

def logout_view(request):
    # Clear user session or perform any other logout actions
    request.session.clear()

    # Redirect to the home page or any other desired page
    return redirect('get_all_news')  # Assuming 'get_all_news' is the name of your home page URL pattern
@csrf_exempt
def create_news_list(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            news_list = data.get('news_list', [])

            created_news_ids = []

            for news_data in news_list:
                form = NewsForm(news_data)
                if form.is_valid():
                    news = form.save()
                    created_news_ids.append(news.id)
                else:
                    return JsonResponse({'error': 'Invalid data', 'errors': form.errors}, status=400)

            return JsonResponse({'message': 'News created successfully', 'created_news_ids': created_news_ids})
        else:
            return JsonResponse({'error': 'Invalid content type. Expected application/json'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def get_all_news(request):
    if request.method == 'GET':
        # Fetch all news items
        news = News.objects.all()

        # Get the user's ID (None if not logged in)
        # Get the user's ID from the session
        user_id = request.session.get('user_id', None)

        # Initialize an empty list to store news data with ratings
        news_data = []

        # Iterate through each news item and fetch the corresponding rating from UserLikes
        for news_item in news:
            # Get the rating for the current news item if available, else set default to 0
            rating = UserLikes.objects.filter(news=news_item, user_id=user_id).first()
            rating_value = rating.rating if rating else 0

            # Append news data including the rating
            news_data.append({
                'id': news_item.id,
                'title': news_item.title,
                'description': news_item.description,
                'link': news_item.link,
                'rating': rating_value,
            })

        # Render the HTML template with the news data
        return render(request, 'news_list.html', {'news_data': news_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def update_rating(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)

        # Get the news item and new rating from the form
        news_id = request.POST.get('news_id')
        new_rating = request.POST.get('new_rating')

        # Update or create a UserLikes entry for the user and news item
        user_likes, created = UserLikes.objects.update_or_create(
            user_id=user_id,
            news_id=news_id,
            defaults={'rating': new_rating}
        )

        return redirect('get_all_news')  # You might want to redirect to a different page after submitting the form
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def get_news_by_id(request, news_id):
    if request.method == 'GET':
        try:
            news = News.objects.get(id=news_id)
            news_data = {'id': news.id, 'title': news.title, 'description': news.description, 'link': news.link}
            return JsonResponse({'news': news_data})
        except News.DoesNotExist:
            return HttpResponseNotFound('News not found')
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@csrf_exempt
def recommend_news(request, news_id):
    if request.method == 'GET':
        news = News.objects.all()

        similarity_matrix = calculate_matrix_of_similarity(cleaning_data(news))
        return recommend_top_news(news, similarity_matrix, news_id)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def delete_news(request, news_id):
    if request.method == 'DELETE':
        try:
            user = News.objects.get(id=news_id)
            user.delete()
            return JsonResponse({'message': f'News with ID {news_id} deleted successfully'})
        except News.DoesNotExist:
            return JsonResponse({'error': f'News with ID {news_id} does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)


@csrf_exempt
def delete_all_news(request):
    if request.method == 'DELETE':
        try:
            News.objects.all().delete()
            return JsonResponse({'message': 'All news deleted successfully'})
        except Exception as e:
            return HttpResponseServerError(f'Error deleting users: {str(e)}')
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
