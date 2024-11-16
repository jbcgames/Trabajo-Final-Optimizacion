import random  
import math    

def bin_packing_simulated_annealing(weights, capacity, initial_temp, cooling_rate, max_iterations):
    # Función para calcular el número de contenedores usados en una solución
    def num_bins(solution):
        bins = []  # Lista para almacenar las capacidades utilizadas de los contenedores
        for item, bin_id in enumerate(solution):  # Iterar sobre cada elemento y su contenedor asignado
            while len(bins) <= bin_id:  # Asegurar que la lista tenga suficientes contenedores
                bins.append(0)  # Inicializar nuevos contenedores
            bins[bin_id] += weights[item]  # Sumar el peso del elemento al contenedor asignado
        return len([b for b in bins if b > 0])  # Contar los contenedores que tienen peso

    # Generar una solución inicial aleatoria
    def generate_initial_solution():
        return [random.randint(0, len(weights) - 1) for _ in weights]  # Asignar cada elemento a un contenedor aleatorio

    # Generar una solución vecina perturbando la solución actual
    def generate_neighbor(solution):
        neighbor = solution[:]  # Copiar la solución actual
        item_to_move = random.randint(0, len(weights) - 1)  # Elegir un elemento aleatorio
        new_bin = random.randint(0, len(weights) - 1)  # Elegir un nuevo contenedor aleatorio
        neighbor[item_to_move] = new_bin  # Mover el elemento al nuevo contenedor
        return neighbor

    # Validar si una solución es factible (ningún contenedor excede la capacidad)
    def is_valid(solution):
        bins = {}  # Diccionario para almacenar el peso acumulado por contenedor
        for item, bin_id in enumerate(solution):  # Iterar sobre cada elemento y su contenedor asignado
            if bin_id not in bins:
                bins[bin_id] = 0  # Inicializar el contenedor si no existe
            bins[bin_id] += weights[item]  # Sumar el peso del elemento al contenedor
            if bins[bin_id] > capacity:  # Si la capacidad es excedida, la solución no es válida
                return False
        return True  # Si ningún contenedor excede la capacidad, es válida

    # Función objetivo: minimizar el número de contenedores usados
    def objective(solution):
        return num_bins(solution)  # Retorna el número de contenedores necesarios

    # Inicialización del algoritmo
    current_solution = generate_initial_solution()  # Generar una solución inicial aleatoria
    while not is_valid(current_solution):  # Asegurarse de que la solución inicial sea válida
        current_solution = generate_initial_solution()

    best_solution = current_solution[:]  # Guardar la mejor solución encontrada
    current_temp = initial_temp  # Establecer la temperatura inicial

    # Ciclo principal del recocido simulado
    for iteration in range(max_iterations):
        # Generar una solución vecina de la solución actual
        neighbor_solution = generate_neighbor(current_solution)

        # Validar si la solución vecina es factible
        if not is_valid(neighbor_solution):
            continue  # Ignorar soluciones inválidas

        # Calcular los costos de la solución actual y la vecina
        current_cost = objective(current_solution)
        neighbor_cost = objective(neighbor_solution)

        # Decidir si aceptar la solución vecina
        if neighbor_cost < current_cost:  # Si la solución vecina es mejor, aceptarla
            current_solution = neighbor_solution
            if neighbor_cost < objective(best_solution):  # Actualizar la mejor solución encontrada
                best_solution = neighbor_solution
        else:
            # Aceptar soluciones peores con una probabilidad dependiente de la temperatura
            delta = neighbor_cost - current_cost  # Diferencia entre los costos
            probability = math.exp(-delta / current_temp)  # Calcular probabilidad de aceptación
            if random.random() < probability:  # Aceptar con probabilidad calculada
                current_solution = neighbor_solution

        # Reducir la temperatura (enfriamiento)
        current_temp *= cooling_rate  # Multiplicar la temperatura por el factor de enfriamiento

        # Imprimir progreso cada 100 iteraciones (opcional)
        if iteration % 100 == 0:
            print(f"Iteración {iteration}, Mejor número de contenedores: {objective(best_solution)}")

    # Retornar la mejor solución encontrada y su costo
    return best_solution, objective(best_solution)

# Parámetros del problema
weights = [1, 2, 3, 4, 5, 1, 3, 3, 4, 2]  # Pesos de los elementos
capacity = 10  # Capacidad de cada contenedor

# Parámetros del recocido simulado
initial_temp = 1000    # Temperatura inicial
cooling_rate = 0.95    # Factor de enfriamiento (reduce la temperatura gradualmente)
max_iterations = 100000  # Número máximo de iteraciones

# Resolver el problema usando recocido simulado
solution, num_bins_used = bin_packing_simulated_annealing(weights, capacity, initial_temp, cooling_rate, max_iterations)

# Mostrar los resultados
print(f"Solución encontrada: {solution}")  # Asignación de cada elemento a un contenedor
print(f"Número mínimo de contenedores utilizados: {num_bins_used}")
