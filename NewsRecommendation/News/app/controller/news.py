import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from ..forms.news import (NewsForm)
from ..models.news import News

from ..recommendation import cleaning_data, calculate_matrix_of_similarity, recommend_top_news


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
        news = News.objects.all()
        news_data = [{'id': news.id, 'title': news.title, 'description': news.description, 'link': news.link} for news
                     in news]
        return JsonResponse({'news': news_data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


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
