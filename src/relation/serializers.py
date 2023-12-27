from rest_framework import serializers
from .models import Trajet

class TrajetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajet
        fields = ['id', 'latitude', 'longitude', ...]  # ajoute les autres champs nécessaires
