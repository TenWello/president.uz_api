# news/tasks.py

from celery import shared_task
from .models import News
from .management.commands.fetch_presidentuz import fetch_presidentuz

@shared_task
def fetch_and_save_presidentuz_news():
    news_list = fetch_presidentuz()
    for item in news_list:
        News.objects.get_or_create(
            link=item['link'],
            defaults={
                'title': item['title'],
                'image': item['image'],
                'published_at': item['published_at'],
            }
        )
    return f"{len(news_list)} news checked and updated."
