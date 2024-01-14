import math
import random 
import matplotlib.pyplot as plt

class City:
    id = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        City.id += 1
        self.id = City.id
        
def distance(city1, city2):
    '''Calcula la distancia entre dos ciudades'''
    
    x1, y1 = city1.x, city1.y
    x2, y2 = city2.x, city2.y
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def total_distance(route):
    '''Calcula la distancia total de una ruta'''
    
    total = 0
    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])
        
    total += distance(route[-1], route[0])  # Regreso al punto de inicio
    return total

def greedy_construction(city_list):
    '''Regresa una ruta óptima desde una ciudad aleatoria'''
    
    start_city = random.choice(city_list)
    current_city = start_city
    remaining_cities = set(city_list) - {current_city} # Establece las cidades restantes por visitar
    route = [current_city]

    while remaining_cities:
        candidates = list(remaining_cities)
        # Ordenar de acuerdo a la distancia con respecto a la ciudad actual
        candidates.sort(key=lambda city: distance(current_city, city))
        
        next_city = candidates[0]
        route.append(next_city)
        current_city = next_city
        remaining_cities.remove(current_city) # Actualiza las ciudades restantes por visitar

    return route

def local_search(route):
    '''Mejora la ruta manteniendo la primera ciudad'''''
    
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2): # Omite la primera y última ciudad
            for j in range(i + 2, len(route)): # Omite la ciudad siguiente a i
                new_route = route.copy()
                new_route[i:j] = route[j - 1:i - 1:-1]  # Invierte el orden de las ciudades entre i y j
                if total_distance(new_route) < total_distance(route):
                    route = new_route
                    improved = True
    return route

def show_route(route, distance, index):
    '''Muestra la ruta en un plano cartesiano'''
    
    x, y = zip(*[(city.x, city.y) for city in route]) # Separa las coordenadas en dos listas
    plt.plot(x, y,)
    plt.scatter(x, y, marker='x', color='red')
    
    labels = ['Ciudad ' + str(city.id) for city in route] # Etiqueta cada ciudad
    for label, x, y in zip(labels, x, y):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points') # Coloca la etiqueta en cada punto
        
    plt.title("Iteración: " + str(index + 1) + "| Distancia: " + str(round(distance, 2)) + " Km| Inicio: Ciudad " + str(route[0].id))
    plt.xlabel('Km')
    plt.ylabel('Km')
    plt.show()

def grasp(city_list, max_iterations):
    '''Aplica el algoritmo GRASP para encontrar la mejor ruta entre las ciudades con
    un número máximo de iteraciones'''
    
    best_solution = None
    best_distance = float('inf')

    for i in range(max_iterations):
        current_solution = greedy_construction(city_list) # Encuentra una solución inicial
        current_solution = local_search(current_solution) # Mejora la solución inicial
        current_distance = total_distance(current_solution) # Calcula la distancia de la ruta

        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance
        
        show_route(best_solution, best_distance, i)
        
    return best_solution, best_distance

cities = [City(0, 0), City(5, 1), City(2, 7), City(3, 4)]
iterations = 5

best_route, best_distance = grasp(cities, iterations)
print("Mejor ruta encontrada:", best_route)
print("Distancia total:", best_distance)

