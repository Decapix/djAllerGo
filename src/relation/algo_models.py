from django.db import models
import uuid

class Cluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    centre_latitude_depart = models.FloatField(default=0.0)
    centre_longitude_depart = models.FloatField(default=0.0)
    centre_latitude_arrivee = models.FloatField(default=0.0)
    centre_longitude_arrivee = models.FloatField(default=0.0)
