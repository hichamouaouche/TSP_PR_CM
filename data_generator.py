
import numpy as np
import json
import os

def generate_tsp_instance(n, seed=None):
  
    if seed is not None:
        np.random.seed(seed)
    
    # Générer les coordonnées des villes dans [0, 100] x [0, 100]
    cities = np.random.uniform(0, 100, size=(n, 2))
    
    # Calculer la matrice de distances euclidiennes
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                distances[i][j] = np.sqrt(dx**2 + dy**2)
    
    instance = {
        'n': n,
        'cities': cities.tolist(),
        'distances': distances.tolist()
    }
    
    return instance

def save_instance(instance, filename):
    """Sauvegarde une instance dans un fichier JSON"""
    with open(filename, 'w') as f:
        json.dump(instance, f, indent=2)
    print(f"Instance sauvegardée: {filename}")

def load_instance(filename):
    """Charge une instance depuis un fichier JSON"""
    with open(filename, 'r') as f:
        instance = json.load(f)
    instance['cities'] = np.array(instance['cities'])
    instance['distances'] = np.array(instance['distances'])
    return instance

if __name__ == "__main__":
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Générer les trois instances avec des graines fixes pour la reproductibilité
    print("Génération des instances TSP...")
    
    # Instance A: 20 villes
    instance_a = generate_tsp_instance(20, seed=42)
    save_instance(instance_a, 'data/instance_20.json')
    
    # Instance B: 50 villes
    instance_b = generate_tsp_instance(50, seed=123)
    save_instance(instance_b, 'data/instance_50.json')
    
    # Instance C: 80 villes
    instance_c = generate_tsp_instance(80, seed=456)
    save_instance(instance_c, 'data/instance_80.json')
    
    print("\nToutes les instances ont été générées avec succès!")
