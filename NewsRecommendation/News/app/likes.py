import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.forms import UserLikesForm
from app.models import News, UserLikes, User

@csrf_exempt
def create_user_likes(request):
    if request.method == 'POST':
        # Ensure that data is sent in a valid JSON format in the request body
        data = json.loads(request.body.decode('utf-8'))

        # Extract necessary data from the JSON object
        vnews_id = data.get('news', None)
        vuser_id = data.get('user', None)

        # Check if necessary data exists in the JSON object
        if vnews_id is None or vuser_id is None:
            return JsonResponse({'error': 'Invalid data', 'errors': 'News ID, Like value, and User ID are required'}, status=400)

        try:
            # Trying to get an entry with the specified user ID and news ID
            user_likes_entry = UserLikes.objects.get(user_id=vuser_id, news_id=vnews_id)
            print("UserLikes entry found:", user_likes_entry)

            # If an entry exists, update the like value
            news = News.objects.get(id=vnews_id)
            news.number_of_likes -= 1
            user_likes_entry.delete()

        except UserLikes.DoesNotExist:
            # Handle the case where the entry doesn't exist
            form_data = {'user': vuser_id, 'news': vnews_id}
            form = UserLikesForm(form_data)
            if form.is_valid():
                user_likes = form.save()
            news = News.objects.get(id=vnews_id)
            news.number_of_likes += 1

        # Update the number of likes for the respective news

        news.save()

        return JsonResponse({'message': 'UserLikes updated successfully'})

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
