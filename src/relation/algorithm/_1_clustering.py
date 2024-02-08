"""first clustering for daily commuting algorithm (1)"""
from sklearn.cluster import DBSCAN
import numpy as np
from django.contrib.auth import get_user_model

from relation.algo_models import Cluster
from relation.models import Route

from math import radians, cos, sin, asin, sqrt
from ._1_extras import calculate_routes_centers, haversine




def initial_clustering(route_data, routes):
    # Configuration initiale de DBSCAN
    dbscan = DBSCAN(eps=0.00045, min_samples=2)  # Paramètres ajustés

    # Application de DBSCAN sur les données
    cluster_labels = dbscan.fit_predict(route_data)

    # Dictionnaire pour regrouper les trajets par label de cluster
    routes_by_cluster_label = {}

    cluster_to_update = []

    # Regrouper les trajets par leur label de cluster
    for route, cluster_label in zip(routes, cluster_labels):
        if cluster_label != -1:
            routes_by_cluster_label.setdefault(cluster_label, []).append(route)
            route.exceptional = False
        else:
            # Traiter les trajets considérés comme bruit 
            route.exceptional = True
        route.save()

    # Créer ou récupérer des clusters pour chaque groupe de trajets
    for cluster_label, routes in routes_by_cluster_label.items():
        # Créer un nouveau cluster (ou récupérer un cluster existant basé sur d'autres critères si nécessaire)
        cluster = Cluster.objects.create()  # Créer un nouveau cluster avec un UUID unique
        cluster_to_update.append(cluster)
        for route in routes:
            route.cluster = cluster
            route.save()

    return cluster_to_update
    


def update_clustering(user_id, route_data, new_routes):
    # Exécution de DBSCAN pour former des clusters
    dbscan = DBSCAN(eps=0.00045, min_samples=2)
    cluster_labels = dbscan.fit_predict(route_data)


    new_clusters = {}  # Pour stocker les trajets par cluster
    cluster_to_update = set()

    # Regrouper les routes par leur label de cluster
    for route, label in zip(new_routes, cluster_labels):
        if label != -1:  # Exclure les bruits
            new_clusters.setdefault(label, []).append(route)
        else:
            route.exceptional = True
            route.save()

    # Traiter chaque nouveau cluster
    for label, routes in new_clusters.items():
        process_cluster(user_id, label, routes, cluster_to_update)

    return list(cluster_to_update)


def process_cluster(user_id, label, routes, cluster_to_update):
    # Calculer le centre du nouveau cluster
    centre_lat_depart, centre_lon_depart, centre_lat_arrivee, centre_lon_arrivee = calculate_routes_centers(routes)

    # Trouver un cluster existant proche
    closest_cluster = find_closest_cluster(user_id, centre_lat_depart, centre_lon_depart, centre_lat_arrivee, centre_lon_arrivee)
    if closest_cluster:
        # Fusionner avec le cluster existant
        for route in routes:
            route.cluster = closest_cluster
            route.exceptional = False
            route.save()
        cluster_to_update.add(closest_cluster)
    else:
        # Créer un nouveau cluster
        new_cluster = Cluster.objects.create(
            centre_latitude_depart=centre_lat_depart, 
            centre_longitude_depart=centre_lon_depart,
            centre_latitude_arrivee=centre_lat_arrivee, 
            centre_longitude_arrivee=centre_lon_arrivee
        )
        for route in routes:
            route.cluster = new_cluster
            route.exceptional = True
            route.save()
        cluster_to_update.add(new_cluster)



def find_closest_cluster(user_id, lat_depart, lon_depart, lat_arrivee, lon_arrivee):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    closest_cluster = None
    min_distance = float('inf')  # Initialise à l'infini

    for cluster in user.get_user_clusters():
        # Calcul de la distance moyenne entre le nouveau cluster et chaque cluster existant
        distance_depart = haversine(cluster.centre_longitude_depart, cluster.centre_latitude_depart, lon_depart, lat_depart)
        distance_arrivee = haversine(cluster.centre_longitude_arrivee, cluster.centre_latitude_arrivee, lon_arrivee, lat_arrivee)
        avg_distance = (distance_depart + distance_arrivee) / 2

        # Vérifie si cette distance est la plus petite jusqu'à présent
        if avg_distance < min_distance:
            min_distance = avg_distance
            closest_cluster = cluster

    # Retourne le cluster le plus proche si la distance est inférieure à un seuil (par exemple, 50 mètres)
    return closest_cluster if min_distance < 50 else None


# ca beug
def test_noize_routes(user_id, routes):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    cluster_to_update = []
    for route in routes :
        for cluster in user.get_user_clusters():
            start_lat, start_lon, end_lat, end_lon = route.get_simplified_route()
            # Calcul de la distance entre le trajets bruit et chaque cluster existant
            distance_depart = haversine(cluster.centre_longitude_depart, cluster.centre_latitude_depart, start_lon, start_lat)
            distance_arrivee = haversine(cluster.centre_longitude_arrivee, cluster.centre_latitude_arrivee, end_lon, end_lat)
            
            if distance_depart <= 50 and distance_arrivee <= 50 :
                print("test_noize_routes positiv", route)
                route.cluster = cluster
                route.exceptional = False
                route.save()

                cluster_to_update.append(cluster)
    return cluster_to_update






