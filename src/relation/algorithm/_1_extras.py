
from relation.models import Route

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    # Convertir les coordonnées en radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Formule de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Rayon de la Terre en kilomètres
    return float(c * r * 1000)

def calculate_average_centers(routes):
    # Calculer la moyenne des coordonnées de départ et d'arrivée
    sum_lat_depart, sum_lon_depart, sum_lat_arrivee, sum_lon_arrivee = 0, 0, 0, 0
    count = 0

    for route in routes:
        simplified_route = route.get_simplified_route()
        if simplified_route:
            sum_lat_depart += simplified_route[0]
            sum_lon_depart += simplified_route[1]
            sum_lat_arrivee += simplified_route[2]
            sum_lon_arrivee += simplified_route[3]
            count += 1

    if count == 0:
        return None

    return (sum_lat_depart / count, sum_lon_depart / count,
            sum_lat_arrivee / count, sum_lon_arrivee / count)


def calculate_cluster_centers(cluster):
    routes = Route.objects.filter(cluster=cluster)
    avg_centers = calculate_average_centers(routes)
    
    if avg_centers:
        cluster.centre_latitude_depart, cluster.centre_longitude_depart, \
        cluster.centre_latitude_arrivee, cluster.centre_longitude_arrivee = avg_centers
        cluster.save()

    return cluster

def calculate_routes_centers(routes):
    return calculate_average_centers(routes)

