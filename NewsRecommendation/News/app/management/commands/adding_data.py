import random
from django.core.management.base import BaseCommand
from app.models.likes import UserLikes
from app.models.user import CustomUser
from app.models.news import News

class Command(BaseCommand):
    help = 'Generate random ratings and save them in the database'

    def handle(self, *args, **options):
        num_users = 3
        num_news = 1000

        for user_id in range(1, num_users + 1):
            for news_id in range(1, num_news + 1):
                try:
                    user_instance = CustomUser.objects.get(id=user_id)
                    news_instance = News.objects.get(id=news_id)

                    rating = round(random.uniform(0, 5), 1)

                    user_like = UserLikes(user_id=user_id, news_id=news_id, rating=rating)
                    user_like.save()
                except News.DoesNotExist:
                    continue

        self.stdout.write(self.style.SUCCESS('Random ratings have been generated and saved.'))