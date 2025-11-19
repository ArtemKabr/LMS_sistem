# lms_project/celery.py — конфигурация Celery
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_project.settings")

app = Celery("lms_project")

# загружает настройки из Django settings с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# автоматический поиск задач в каждом app/tasks.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """Отладочная задача Celery"""
    print(f"Debug task executed: {self.request!r}")
