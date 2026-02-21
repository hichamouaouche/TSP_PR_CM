
import numpy as np
import json
import time
import os
from algorithms import (HillClimbingFirst, HillClimbingBest, 
                        MultiStartHC, SimulatedAnnealing, TabuSearch)
from data_generator import load_instance
import matplotlib.pyplot as plt
from datetime import datetime

class TSPExperiment:
    """Classe pour gérer les expériences sur le TSP"""
    
    def __init__(self, instance_file):
        """
        Args:
            instance_file: chemin vers le fichier d'instance
        """
        self.instance = load_instance(instance_file)
        self.distances = self.instance['distances']
        self.n = self.instance['n']
        self.results = {}
        
    def run_algorithm(self, algorithm_name, num_runs=30):

        print(f"\n{'='*60}")
        print(f"Exécution: {algorithm_name} sur instance n={self.n}")
        print(f"{'='*60}")
        
        costs = []
        times = []
        eval_counts = []
        best_tour = None
        best_cost = float('inf')
        
        for run in range(num_runs):
            start_time = time.time()
            
            # Créer l'instance de l'algorithme
            if algorithm_name == "Hill Climbing First":
                solver = HillClimbingFirst(self.distances)
                solver.reset_eval_count()
                tour, cost, history = solver.solve(max_iterations=1000)
                
            elif algorithm_name == "Hill Climbing Best":
                solver = HillClimbingBest(self.distances)
                solver.reset_eval_count()
                tour, cost, history = solver.solve(max_iterations=1000)
                
            elif algorithm_name == "Multi-Start HC":
                solver = MultiStartHC(self.distances)
                solver.reset_eval_count()
                tour, cost, history = solver.solve(num_starts=30, hc_type='best')
                
            elif algorithm_name == "Simulated Annealing":
                solver = SimulatedAnnealing(self.distances)
                solver.reset_eval_count()
                tour, cost, history = solver.solve(T0=100, alpha=0.95, T_min=0.01, max_iterations=10000)
                
            elif algorithm_name == "Tabu Search":
                solver = TabuSearch(self.distances)
                solver.reset_eval_count()
                tour, cost, history = solver.solve(tabu_tenure=20, max_iterations=1000)
            
            end_time = time.time()
            exec_time = end_time - start_time
            
            costs.append(cost)
            times.append(exec_time)
            eval_counts.append(solver.eval_count)
            
            if cost < best_cost:
                best_cost = cost
                best_tour = tour
            
            print(f"Run {run+1}/{num_runs}: Coût = {cost:.2f}, Temps = {exec_time:.4f}s")
        
        results = {
            'algorithm': algorithm_name,
            'n': self.n,
            'best_cost': best_cost,
            'best_tour': best_tour,
            'mean_cost': np.mean(costs),
            'std_cost': np.std(costs),
            'min_cost': np.min(costs),
            'max_cost': np.max(costs),
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'mean_evals': np.mean(eval_counts),
            'all_costs': costs,
            'all_times': times
        }
        
        print(f"\n--- Résumé ---")
        print(f"Meilleur coût: {best_cost:.2f}")
        print(f"Coût moyen: {np.mean(costs):.2f} ± {np.std(costs):.2f}")
        print(f"Temps moyen: {np.mean(times):.4f}s ± {np.std(times):.4f}s")
        
        return results
    
    def run_all_experiments(self, num_runs=30):
        """Exécute tous les algorithmes"""
        algorithms = [
            "Hill Climbing First",
            "Hill Climbing Best",
            "Multi-Start HC",
            "Simulated Annealing",
            "Tabu Search"
        ]
        
        for algo in algorithms:
            self.results[algo] = self.run_algorithm(algo, num_runs)
        
        return self.results
    
    def save_results(self, output_dir='results'):
        """Sauvegarde les résultats"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Préparer les données pour la sauvegarde (convertir en types JSON-sérialisables)
        results_to_save = {}
        for algo, result in self.results.items():
            results_to_save[algo] = {
                'algorithm': result['algorithm'],
                'n': result['n'],
                'best_cost': float(result['best_cost']),
                'mean_cost': float(result['mean_cost']),
                'std_cost': float(result['std_cost']),
                'min_cost': float(result['min_cost']),
                'max_cost': float(result['max_cost']),
                'mean_time': float(result['mean_time']),
                'std_time': float(result['std_time']),
                'mean_evals': float(result['mean_evals']),
                'all_costs': [float(c) for c in result['all_costs']],
                'all_times': [float(t) for t in result['all_times']]
            }
        
        filename = f"{output_dir}/results_n{self.n}.json"
        with open(filename, 'w') as f:
            json.dump(results_to_save, f, indent=2)
        print(f"\nRésultats sauvegardés: {filename}")
    
    def generate_comparison_table(self):
        """Génère un tableau de comparaison"""
        print(f"\n{'='*100}")
        print(f"TABLEAU DE COMPARAISON - Instance n={self.n}")
        print(f"{'='*100}")
        
        header = f"{'Algorithme':<25} {'Meilleur':<12} {'Moyen':<15} {'Écart-type':<12} {'Temps (s)':<15} {'Évals':<10}"
        print(header)
        print('-' * 100)
        
        for algo, result in self.results.items():
            row = f"{algo:<25} {result['best_cost']:<12.2f} {result['mean_cost']:<15.2f} {result['std_cost']:<12.2f} {result['mean_time']:<15.4f} {result['mean_evals']:<10.0f}"
            print(row)
        
        print('=' * 100)
    
    def plot_results(self, output_dir='figures'):
        """Génère des graphiques de comparaison"""
        os.makedirs(output_dir, exist_ok=True)
        
        algorithms = list(self.results.keys())
        
        # Graphique 1: Comparaison des coûts moyens
        fig, ax = plt.subplots(figsize=(12, 6))
        
        means = [self.results[algo]['mean_cost'] for algo in algorithms]
        stds = [self.results[algo]['std_cost'] for algo in algorithms]
        
        x_pos = np.arange(len(algorithms))
        ax.bar(x_pos, means, yerr=stds, capsize=5, alpha=0.7, color='steelblue')
        ax.set_xlabel('Algorithme', fontsize=12)
        ax.set_ylabel('Coût moyen', fontsize=12)
        ax.set_title(f'Comparaison des coûts moyens (n={self.n} villes)', fontsize=14)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/comparison_mean_cost_n{self.n}.png', dpi=300)
        print(f"Graphique sauvegardé: {output_dir}/comparison_mean_cost_n{self.n}.png")
        plt.close()
        
        # Graphique 2: Boxplot des distributions de coûts
        fig, ax = plt.subplots(figsize=(12, 6))
        
        data = [self.results[algo]['all_costs'] for algo in algorithms]
        ax.boxplot(data, labels=algorithms)
        ax.set_xlabel('Algorithme', fontsize=12)
        ax.set_ylabel('Coût', fontsize=12)
        ax.set_title(f'Distribution des coûts (n={self.n} villes)', fontsize=14)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/boxplot_costs_n{self.n}.png', dpi=300)
        print(f"Graphique sauvegardé: {output_dir}/boxplot_costs_n{self.n}.png")
        plt.close()
        
        # Graphique 3: Comparaison des temps d'exécution
        fig, ax = plt.subplots(figsize=(12, 6))
        
        times = [self.results[algo]['mean_time'] for algo in algorithms]
        time_stds = [self.results[algo]['std_time'] for algo in algorithms]
        
        ax.bar(x_pos, times, yerr=time_stds, capsize=5, alpha=0.7, color='coral')
        ax.set_xlabel('Algorithme', fontsize=12)
        ax.set_ylabel('Temps moyen (s)', fontsize=12)
        ax.set_title(f'Comparaison des temps d\'exécution (n={self.n} villes)', fontsize=14)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(algorithms, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/comparison_time_n{self.n}.png', dpi=300)
        print(f"Graphique sauvegardé: {output_dir}/comparison_time_n{self.n}.png")
        plt.close()
        
        # Graphique 4: Visualisation de la meilleure solution
        best_algo = min(self.results.items(), key=lambda x: x[1]['best_cost'])
        best_tour = best_algo[1]['best_tour']
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        cities = self.instance['cities']
        
        # Dessiner le tour
        for i in range(len(best_tour)):
            city1 = best_tour[i]
            city2 = best_tour[(i + 1) % len(best_tour)]
            ax.plot([cities[city1][0], cities[city2][0]], 
                   [cities[city1][1], cities[city2][1]], 
                   'b-', linewidth=1, alpha=0.6)
        
        # Dessiner les villes
        ax.scatter(cities[:, 0], cities[:, 1], c='red', s=100, zorder=5)
        
        # Marquer la ville de départ
        start_city = best_tour[0]
        ax.scatter([cities[start_city][0]], [cities[start_city][1]], 
                  c='green', s=200, marker='*', zorder=10, label='Départ')
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title(f'Meilleure solution trouvée (n={self.n}, coût={best_algo[1]["best_cost"]:.2f})\nAlgorithme: {best_algo[0]}', 
                    fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/best_tour_n{self.n}.png', dpi=300)
        print(f"Graphique sauvegardé: {output_dir}/best_tour_n{self.n}.png")
        plt.close()


def run_complete_experiment():
    """Exécute l'expérience complète sur toutes les instances"""
    instances = [
        'data/instance_20.json',
        'data/instance_50.json',
        'data/instance_80.json'
    ]
    
    all_results = {}
    
    print("\n" + "="*60)
    print("DÉBUT DE L'EXPÉRIMENTATION COMPLÈTE")
    print("="*60)
    
    for instance_file in instances:
        print(f"\n{'#'*60}")
        print(f"# Instance: {instance_file}")
        print(f"{'#'*60}")
        
        experiment = TSPExperiment(instance_file)
        results = experiment.run_all_experiments(num_runs=30)
        experiment.save_results()
        experiment.generate_comparison_table()
        experiment.plot_results()
        
        all_results[f"n={experiment.n}"] = results
    
    print("\n" + "="*60)
    print("EXPÉRIMENTATION TERMINÉE")
    print("="*60)
    
    return all_results


if __name__ == "__main__":
 
    if not os.path.exists('data/instance_20.json'):
        print("Génération des instances TSP...")
        import data_generator
        data_generator.main()
    
    results = run_complete_experiment()
    
    

