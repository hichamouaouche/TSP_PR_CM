
import numpy as np
import random
import time
from copy import deepcopy

class TSPSolver:
    """Classe de base pour résoudre le TSP"""
    
    def __init__(self, distances):

        self.distances = distances
        self.n = len(distances)
        self.eval_count = 0
    
    def evaluate(self, tour):

        self.eval_count += 1
        cost = 0
        for i in range(self.n):
            city1 = tour[i]
            city2 = tour[(i + 1) % self.n]
            cost += self.distances[city1][city2]
        return cost
    
    def random_solution(self):
        """Génère une solution aléatoire"""
        tour = list(range(self.n))
        random.shuffle(tour)
        return tour
    
    def get_neighbors_swap(self, tour):

        neighbors = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                neighbor = tour.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors
    
    def reset_eval_count(self):
        """Réinitialise le compteur d'évaluations"""
        self.eval_count = 0


class HillClimbingFirst(TSPSolver):
    """Hill Climbing avec stratégie First Improvement"""
    
    def solve(self, initial_solution=None, max_iterations=1000):
        
        if initial_solution is None:
            current = self.random_solution()
        else:
            current = initial_solution.copy()
        
        current_cost = self.evaluate(current)
        history = [current_cost]
        
        iteration = 0
        improved = True
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # Parcourir les voisins et accepter le premier qui améliore
            for i in range(self.n):
                if improved:
                    break
                for j in range(i + 1, self.n):
                    neighbor = current.copy()
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbor_cost = self.evaluate(neighbor)
                    
                    if neighbor_cost < current_cost:
                        current = neighbor
                        current_cost = neighbor_cost
                        history.append(current_cost)
                        improved = True
                        break
        
        return current, current_cost, history


class HillClimbingBest(TSPSolver):
    """Hill Climbing avec stratégie Best Improvement"""
    
    def solve(self, initial_solution=None, max_iterations=1000):
      
        if initial_solution is None:
            current = self.random_solution()
        else:
            current = initial_solution.copy()
        
        current_cost = self.evaluate(current)
        history = [current_cost]
        
        iteration = 0
        improved = True
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            best_neighbor = None
            best_cost = current_cost
            
            # Explorer tous les voisins et choisir le meilleur
            neighbors = self.get_neighbors_swap(current)
            for neighbor in neighbors:
                neighbor_cost = self.evaluate(neighbor)
                if neighbor_cost < best_cost:
                    best_neighbor = neighbor
                    best_cost = neighbor_cost
                    improved = True
            
            if improved:
                current = best_neighbor
                current_cost = best_cost
                history.append(current_cost)
        
        return current, current_cost, history


class MultiStartHC(TSPSolver):
    """Multi-start Hill Climbing"""
    
    def solve(self, num_starts=30, hc_type='best', max_iterations=1000):
       
        best_tour = None
        best_cost = float('inf')
        all_costs = []
        
        if hc_type == 'first':
            hc = HillClimbingFirst(self.distances)
        else:
            hc = HillClimbingBest(self.distances)
        
        for _ in range(num_starts):
            initial = self.random_solution()
            tour, cost, _ = hc.solve(initial, max_iterations)
            all_costs.append(cost)
            
            if cost < best_cost:
                best_cost = cost
                best_tour = tour
        
        self.eval_count = hc.eval_count
        return best_tour, best_cost, all_costs


class SimulatedAnnealing(TSPSolver):
    """Recuit Simulé (Simulated Annealing)"""
    
    def solve(self, initial_solution=None, T0=100, alpha=0.95, T_min=0.01, max_iterations=10000):
     
        if initial_solution is None:
            current = self.random_solution()
        else:
            current = initial_solution.copy()
        
        current_cost = self.evaluate(current)
        best_tour = current.copy()
        best_cost = current_cost
        
        history = [current_cost]
        T = T0
        iteration = 0
        
        while T > T_min and iteration < max_iterations:
            iteration += 1
            
            # Générer un voisin aléatoire (swap)
            i, j = random.sample(range(self.n), 2)
            neighbor = current.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            
            neighbor_cost = self.evaluate(neighbor)
            delta = neighbor_cost - current_cost
            
            # Acceptation selon le critère de Metropolis
            if delta <= 0 or random.random() < np.exp(-delta / T):
                current = neighbor
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_tour = current.copy()
                    best_cost = current_cost
            
            history.append(best_cost)
            
            # Refroidissement
            if iteration % 100 == 0:
                T *= alpha
        
        return best_tour, best_cost, history


class TabuSearch(TSPSolver):
    """Recherche Tabou (bonus)"""
    
    def solve(self, initial_solution=None, tabu_tenure=20, max_iterations=1000):
     
        if initial_solution is None:
            current = self.random_solution()
        else:
            current = initial_solution.copy()
        
        current_cost = self.evaluate(current)
        best_tour = current.copy()
        best_cost = current_cost
        
        history = [current_cost]
        tabu_list = []
        
        for iteration in range(max_iterations):
            neighbors = self.get_neighbors_swap(current)
            
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_move = None
            
            # Trouver le meilleur voisin non-tabou
            for neighbor in neighbors:
                neighbor_cost = self.evaluate(neighbor)
                
                # Déterminer le mouvement
                move = None
                for i in range(self.n):
                    if neighbor[i] != current[i]:
                        j = neighbor.index(current[i])
                        move = tuple(sorted([i, j]))
                        break
                
                # Critère d'aspiration: accepter si meilleur que best_cost
                if neighbor_cost < best_cost or move not in tabu_list:
                    if neighbor_cost < best_neighbor_cost:
                        best_neighbor = neighbor
                        best_neighbor_cost = neighbor_cost
                        best_move = move
            
            if best_neighbor is None:
                break
            
            current = best_neighbor
            current_cost = best_neighbor_cost
            
            # Mettre à jour la liste tabou
            if best_move:
                tabu_list.append(best_move)
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)
            
            if current_cost < best_cost:
                best_tour = current.copy()
                best_cost = current_cost
            
            history.append(best_cost)
        
        return best_tour, best_cost, history
