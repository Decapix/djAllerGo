from django.contrib import admin

from .algo_models import Cluster
from .models import Route, Point, RepresentativePoint, RepresentativeRoute



    
class PointInline(admin.StackedInline):
    model = Point
    extra = 0
    fields = ['position', 'time_from_start', 'point']
    readonly_fields = ['position', 'time_from_start', 'point']

class RouteAdmin(admin.ModelAdmin):
    inlines = [PointInline]
    list_display = ['__str__', 'user', 'departure']
    list_filter = ['user', 'departure']
    search_fields = ['user__phone_number', 'departure']
    ordering = ['-departure']


class RepresentativePointInline(admin.StackedInline):
    model = RepresentativePoint
    extra = 0
    fields = ['position', 'time_from_start', 'point']
    readonly_fields = ['position', 'time_from_start', 'point']

class RepresentativeRouteAdmin(admin.ModelAdmin):
    inlines = [RepresentativePointInline]
    list_display = ['__str__', 'user', 'departure']
    list_filter = ['user', 'departure']
    search_fields = ['user__phone_number', 'departure']
    ordering = ['-departure']

admin.site.register(Route, RouteAdmin)
admin.site.register(Point) 
admin.site.register(RepresentativeRoute, RepresentativeRouteAdmin)
admin.site.register(RepresentativePoint) 
admin.site.register(Cluster) 

