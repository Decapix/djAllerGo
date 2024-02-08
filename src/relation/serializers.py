from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Route, Point as RoutePoint


class PointSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        model = RoutePoint
        fields = ['position', 'time_from_start', 'latitude', 'longitude', 'route']

    def create(self, validated_data):
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        point = Point(longitude, latitude)
        return RoutePoint.objects.create(point=point, **validated_data)



    
class RouteSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Route
        fields = ['departure', 'points']

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        route = Route.objects.create(**validated_data)
        for point_data in points_data:
            point_data['route'] = route.id  # Passe l'ID de la route, qui est un UUID
            point_serializer = PointSerializer(data=point_data)
            if point_serializer.is_valid():
                point_serializer.save()
            else:
                raise serializers.ValidationError(point_serializer.errors)
        return route

