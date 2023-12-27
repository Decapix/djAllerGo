from rest_framework import viewsets
from .models import Trajet
from .serializers import TrajetSerializer

class TrajetViewSet(viewsets.ModelViewSet):
    queryset = Trajet.objects.all()
    serializer_class = TrajetSerializer

    def create(self, request, *args, **kwargs):
        # Ici, tu peux ajouter ta logique personnalisée pour la création des objets Trajet
        # Par exemple, analyser les données de géolocalisation, effectuer des tests, etc.
        return super().create(request, *args, **kwargs)
