import json

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..forms.news import (NewsForm)
from ..models.likes import UserLikes
from ..models.news import News


def logout_view(request):
    request.session.clear()

    return redirect('get_all_news')


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
        news = News.objects.all()[:100]

        user_id = request.session.get('user_id', None)

        news_data = []

        for news_item in news:
            rating = UserLikes.objects.filter(news=news_item, user_id=user_id).first()
            rating_value = rating.rating if rating else 0

            news_data.append({
                'id': news_item.id,
                'title': news_item.title,
                'description': news_item.description,
                'link': news_item.link,
                'rating': rating_value,
            })

        return render(request, 'news_list.html', {'news_data': news_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


def update_rating(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)

        news_id = request.POST.get('news_id')
        new_rating = request.POST.get('new_rating')

        if new_rating is None:
            pass
        else:
            user_likes, created = UserLikes.objects.update_or_create(
                user_id=user_id,
                news_id=news_id,
                defaults={'rating': new_rating}
            )

        return redirect('get_all_news')
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
