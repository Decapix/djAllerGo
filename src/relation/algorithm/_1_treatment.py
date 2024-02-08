"""treatement for daily commuting algorithm (1)"""
import numpy as np
from celery import shared_task
from django.contrib.auth import get_user_model
from relation.algo_models import Cluster
from relation.models import Route
from ._1_clustering import update_clustering, initial_clustering, test_noize_routes
from ._1_extras import calculate_cluster_centers
from django.db.models import Q


@shared_task
def treatment(user_id):
    try:
        # 1.1
        User = get_user_model()
        user = User.objects.get(id=user_id)
        cluster_to_update = []
        # mise a jour des cluster
        if user.route_clustering_begins:
            # les enciens bruits
            old_noiz = Route.objects.filter(user=user, exceptional=True )
            # les routes qui sont a inclure dans le process, pas traite ou bruits
            unprocessed_routes = Route.objects.filter(user=user).filter(Q(exceptional=True) | Q(exceptional=None))
            
            if unprocessed_routes.exists():
                route_data = [route.get_simplified_route() for route in unprocessed_routes]
                route_data = np.array(route_data)

                cluster_to_update = update_clustering(user_id, route_data, unprocessed_routes)

            # traiter les bruits du deuxieme dbscan
            old_noiz_ids = old_noiz.values_list('id', flat=True)  # Récupère les IDs des éléments de old_noiz
            noize_routes = Route.objects.filter(user=user, exceptional=True ).exclude(id__in=old_noiz_ids)

            print("okokok", noize_routes)
            cluster_to_update += test_noize_routes(user_id, noize_routes)
        
        # initialisation
        else:
            
            all_routes = Route.objects.filter(user=user )
            route_data = [route.get_simplified_route() for route in all_routes]
            route_data = np.array(route_data)
            cluster_to_update = initial_clustering(route_data, all_routes)
            user.route_clustering_begins = True
            user.save()

        for cluster in list(set(cluster_to_update)):
            calculate_cluster_centers(cluster)

        # 1.2 | do representative routes
        clusters = user.get_user_clusters()
        for cluster in clusters:
            print(cluster)

    except Exception as e:
        print("Error in treatment function: ", e)


        
        





