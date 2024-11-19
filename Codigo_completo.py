import random  
import math    
import pandas as pd
import time
import gurobipy as gp
from gurobipy import GRB

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

def solve_with_gurobi(weights, capacity):
    n = len(weights)
    UB = n
    try:
        model = gp.Model()
        x = model.addVars(n, UB, vtype=GRB.BINARY)
        y = model.addVars(UB, vtype=GRB.BINARY)

        # Minimize the number of bins used
        model.setObjective(gp.quicksum(y[j] for j in range(UB)), GRB.MINIMIZE)

        # Pack each item in exactly one bin
        model.addConstrs(gp.quicksum(x[i, j] for j in range(UB)) == 1 for i in range(n))

        # Bin capacity constraint
        model.addConstrs(gp.quicksum(weights[i] * x[i, j] for i in range(n)) <= capacity * y[j] for j in range(UB))

        # Solve the model
        start_time = time.time()
        model.optimize()
        gurobi_time = time.time() - start_time

        if model.status == GRB.OPTIMAL:
            bin_for_item = [-1 for _ in range(n)]
            for i in range(n):
                for j in range(UB):
                    if x[i, j].X > 0.5:
                        bin_for_item[i] = j
            return model.ObjVal, bin_for_item, gurobi_time
        else:
            return None, None, None

    except gp.GurobiError as e:
        print(f"Error de Gurobi: {e}")
        return None, None, None

# Configuración de instancias
instances = [
    {
        "weights": [4, 7, 18, 14, 15, 5, 18, 6, 18, 10, 2, 1, 10, 11, 16],
        "capacity": random.randint(50, 100),
        "initial_temp": random.choice([500, 1000, 1500, 2000]),
        "cooling_rate": random.choice([0.95, 0.90, 0.85, 0.80]),
        "max_iterations": random.choice([100, 500, 5000, 10000]),
    }
    for _ in range(10000)
]

# Ejecución de todas las instancias
results = []
for idx, instance in enumerate(instances):
    print(f"Ejecución de la instancia {idx + 1}")

    # Resolver con Recocido Simulado
    sa_start_time = time.time()
    sa_solution, sa_bins_used = bin_packing_simulated_annealing(
        instance["weights"],
        instance["capacity"],
        instance["initial_temp"],
        instance["cooling_rate"],
        instance["max_iterations"],
    )
    sa_time = time.time() - sa_start_time

    # Resolver con Gurobi
    gurobi_bins_used, gurobi_solution, gurobi_time = solve_with_gurobi(
        instance["weights"],
        instance["capacity"]
    )

    # Calcular brecha si es posible
    brecha = None
    if gurobi_bins_used is not None and sa_bins_used is not None:
        brecha = ((sa_bins_used - gurobi_bins_used) / gurobi_bins_used) * 100

    # Agregar resultados
    results.append({
        "Instancia": idx + 1,
        "Número de Ítems": len(instance["weights"]),
        "Capacidad": instance["capacity"],
        "T₀": instance["initial_temp"],
        "α": instance["cooling_rate"],
        "Iteraciones": instance["max_iterations"],
        "Óptima (Gurobi)": gurobi_bins_used,
        "Óptima (Recocido)": sa_bins_used,
        "Brecha (%)": brecha,
        "Tiempo (Gurobi)": gurobi_time,
        "Tiempo (Recocido)": sa_time,
        "Pesos": instance["weights"],
        "Capacidad": instance["capacity"],
        "Recocido Solución": sa_solution,
        "Recocido Contenedores": sa_bins_used,
        "Gurobi Solución": gurobi_solution,
        "Gurobi Contenedores": gurobi_bins_used,
    })

# Guardar resultados en un archivo Excel
df_results = pd.DataFrame(results)
file_path = "Resultados_Bin_Packing.xlsx"
df_results.to_excel(file_path, index=False)

# Mostrar resultados finales
for result in results:
    print(f"Instancia {result['Instancia']}: Recocido {result['Óptima (Recocido)']} contenedores, Gurobi {result['Óptima (Gurobi)']} contenedores")
print(f"Resultados guardados en {file_path}")