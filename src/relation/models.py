from django.db import models
from user.models import User
import uuid
from django.contrib.gis.db import models as gismodels
from .algo_models import Cluster

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departure = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='route', on_delete=models.CASCADE)
    cluster = models.ForeignKey('Cluster', on_delete=models.SET_NULL, null=True)
    exceptional = models.BooleanField(default=None, null=True)

    def __str__ (self):
        return f"{self.user} - {self.departure}"
    
    def get_simplified_route(self):
        # Tri des points de la route par position ou time_from_start
        points = self.points.all().order_by('position')

        # Vérifier s'il y a des points dans la route
        if not points:
            return None

        # Récupérer le premier et le dernier point
        start_point = points.first().point
        end_point = points.last().point

        # Extraire les coordonnées de latitude et longitude
        start_lat, start_lon = start_point.coords
        end_lat, end_lon = end_point.coords

        # Renvoyer les coordonnées
        return (start_lat, start_lon, end_lat, end_lon)

class RepresentativeRoute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departure = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='representative_route', on_delete=models.CASCADE)
    cluster = models.OneToOneField(Cluster, on_delete=models.CASCADE, related_name='representativeRoute')

class Point(models.Model):
    """a route is group of point

    Args:
        position : first, seconde, third ... from 0
        time_from_start : second 0 = start
        
    """
    position = models.PositiveIntegerField()
    time_from_start = models.PositiveIntegerField()
    point = gismodels.PointField(blank=True, null=True, srid=4326)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points', null=True, default=None)
    
    def __str__(self):
        formatted_departure = self.route.departure.strftime('%d %B %Y') if self.route.departure else 'Unknown'
        return f"{self.route.user} - {formatted_departure} - {self.position}"

class RepresentativePoint(models.Model):
    """a route is group of point

    Args:
        position : first, seconde, third ... from 0
        time_from_start : second 0 = start
        
    """
    position = models.PositiveIntegerField()
    time_from_start = models.PositiveIntegerField()
    point = gismodels.PointField(blank=True, null=True, srid=4326)
    route = models.ForeignKey(RepresentativeRoute, on_delete=models.CASCADE, related_name='points', null=True, default=None)
    
    def __str__(self):
        formatted_departure = self.route.departure.strftime('%d %B %Y') if self.route.departure else 'Unknown'
        return f"{self.route.user} - {formatted_departure} - {self.position}"