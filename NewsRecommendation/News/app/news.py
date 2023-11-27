import json

# Create your views here.

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from app.forms import (NewsForm)

from app.models import News


@csrf_exempt
def create_news(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            form = NewsForm(data)
        else:
            form = NewsForm(request.POST)

        if form.is_valid():
            news = form.save()
            return JsonResponse({'message': 'News created successfully', 'news_id': news.id})
        else:
            return JsonResponse({'error': 'Invalid data', 'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def get_all_news(request):
    if request.method == 'GET':
        news = News.objects.all()
        news_data = [{'id': news.id, 'description': news.description} for news in news]

        return JsonResponse({'news': news_data})
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
def get_news_by_id(request, news_id):
    if request.method == 'GET':
        try:
            news = News.objects.get(id=news_id)
            news_data = {'id': news.id, 'description': news.description}
            return JsonResponse({'news': news_data})
        except News.DoesNotExist:
            return HttpResponseNotFound('News not found')
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

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