from django.urls import path as p
from .views import *

urlpatterns = [
    p('route-reception/', RouteReceptionView.as_view(), name='route-reception'),
]