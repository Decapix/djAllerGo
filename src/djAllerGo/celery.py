from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir la variable d'environnement par défaut pour le fichier de configuration Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djAllerGo.settings')

app = Celery('djAllerGo')

# Utiliser la configuration de la base de données Django pour le courtier de messages
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches des applications installées
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")