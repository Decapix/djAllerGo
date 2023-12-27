from geopy.distance import geodesic


Δ = [
    ("coordonnélong1", "coordonnélat1", "heur1"),
    ("coordonnélong2", "coordonnélat2", "heur2"),
    ("coordonnélong3", "coordonnélat3", "heur3"),
    ("coordonnélong4", "coordonnélat4", "heur4"),
    ("coordonnélong5", "coordonnélat5", "heur5"),
    ...
]

trajets = [
    [("coordonnélong1.1", "coordonnélat1.1", "heur1.1"), ("coordonnélong1.2", "coordonnélat1.2", "heur1.2"), ("coordonnélong1.3", "coordonnélat1.3", "heur1.3"), ("coordonnélong1.4", "coordonnélat1.4", "heur1.4"), ("coordonnélong1.5", "coordonnélat1.5", "heur1.5")],
    [("coordonnélong2.1", "coordonnélat2.1", "heur2.1"), ("coordonnélong2.2", "coordonnélat2.2", "heur2.2"), ("coordonnélong2.3", "coordonnélat2.3", "heur2.3"), ("coordonnélong2.4", "coordonnélat2.4", "heur2.4"), ("coordonnélong2.5", "coordonnélat2.5", "heur2.5")],
    [("coordonnélong3.1", "coordonnélat3.1", "heur3.1"), ("coordonnélong3.2", "coordonnélat3.2", "heur3.2"), ("coordonnélong3.3", "coordonnélat3.3", "heur3.3"), ("coordonnélong3.4", "coordonnélat3.4", "heur3.4"), ("coordonnélong3.5", "coordonnélat3.5", "heur3.5")],
]




# Définir les coordonnées des deux points
point1 = (48.8566, 2.3522)  # Paris
point2 = (40.7128, -74.0060)  # New York

# Calculer la distance en mètres
distance = geodesic(point1, point2).meters


def incircle(p, d) :
    """si le cercle de diamètre (1/10longeur de t avec max 20 km) de de centre p contient d alors on renvoie true"""
    return True



def trajet_similaire(Δ, trajets) :
    for t in trajets :
        for p in t :
            for d in Δ:
                while incircle(p, d) :
                    pass
                