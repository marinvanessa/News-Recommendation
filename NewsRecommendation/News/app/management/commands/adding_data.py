import random
from django.core.management.base import BaseCommand
from app.models.likes import UserLikes
from app.models.user import CustomUser
from app.models.news import News

class Command(BaseCommand):
    help = 'Generate random ratings and save them in the database'

    def handle(self, *args, **options):
        # Number of users and news
        num_users = 3
        num_news = 100

        # Generate random ratings for each user-news pair
        for user_id in range(1, num_users + 1):
            for news_id in range(1, num_news + 1):
                try:
                    # Assuming you have User and News instances corresponding to user_id and news_id
                    user_instance = CustomUser.objects.get(id=user_id)
                    news_instance = News.objects.get(id=news_id)

                    # Generate a random rating between 0 and 5
                    rating = round(random.uniform(0, 5), 1)

                    # Create a new UserLikes object and save it
                    user_like = UserLikes(user_id=user_id, news_id=news_id, rating=rating)
                    user_like.save()
                except News.DoesNotExist:
                    # Skip to the next news_id if the News doesn't exist
                    continue

        self.stdout.write(self.style.SUCCESS('Random ratings have been generated and saved.'))