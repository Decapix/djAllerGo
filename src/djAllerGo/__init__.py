from __future__ import absolute_import, unicode_literals

# Ceci va s'assurer que l'application Celery est toujours importée
# quand Django démarre afin que les tâches partagées puissent utiliser cette application.
from .celery import app as celery_app

__all__ = ('celery_app',)
