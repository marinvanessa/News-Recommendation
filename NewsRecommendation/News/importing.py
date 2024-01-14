import csv
import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsrecommendation.settings")

setup()

from app.models.news import News

def import_news_from_csv(file_path, limit=1000):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        count = 0
        for row in csv_reader:
            news_obj = News.objects.create(
                title=row['title'][:100],
                description=row['description'][:150],
                link=row['link'][:100]
            )
            news_obj.save()
            count += 1
            if count >= limit:
                break

if __name__ == "__main__":
    csv_file_path = 'E:\\sac2\\NewsRecommendation\\Dataset\\bbc_news.csv'
    import_news_from_csv(csv_file_path, limit=1000)
