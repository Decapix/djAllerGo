from django.db import models
from user.models import User
import uuid


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='route', on_delete=models.CASCADE)
    