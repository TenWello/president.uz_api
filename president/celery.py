import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'presidentuz_api.settings')

app = Celery('presidentuz_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
