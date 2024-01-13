import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models.news import News
from app.models.likes import UserLikes
from ..forms.likes import UserLikesForm


@csrf_exempt
def create_user_likes(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        vnews_id = data.get('news', None)
        vuser_id = data.get('user', None)
        vrating = data.get('rating', None)

        if vnews_id is None or vuser_id is None:
            return JsonResponse({'error': 'Invalid data', 'errors': 'News ID, Like value, and User ID are required'}, status=400)

        try:
            user_likes_entry = UserLikes.objects.get(user_id=vuser_id, news_id=vnews_id)
            print("UserLikes entry found:", user_likes_entry)

            news = News.objects.get(id=vnews_id)
            news.number_of_likes -= 1
            user_likes_entry.delete()

        except UserLikes.DoesNotExist:
            form_data = {'user': vuser_id, 'news': vnews_id, 'rating': vrating}
            form = UserLikesForm(form_data)
            if form.is_valid():
                user_likes = form.save()
            news = News.objects.get(id=vnews_id)
            news.number_of_likes += 1

        news.save()

        return JsonResponse({'message': 'UserLikes updated successfully'})

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
