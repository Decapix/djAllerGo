from rest_framework.views import APIView
from .models import Route, Point
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .algorithm._1_treatment import treatment


class RouteReceptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        routes_data = request.data

        for route_data in routes_data:
            serializer = RouteSerializer(data=route_data)
            if serializer.is_valid():
                route = serializer.save(user=user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        treatment.delay(user.id)
        return Response({"message": "Routes received successfully."}, status=status.HTTP_201_CREATED)
