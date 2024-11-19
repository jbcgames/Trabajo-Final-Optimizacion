# Trabajo Final de Optimización

Este proyecto aborda el **Problema de Empaquetamiento Unidimensional**, implementando el algoritmo de **Recocido Simulado** para minimizar el número de contenedores necesarios al empaquetar objetos de distintos pesos, respetando una capacidad máxima por contenedor.

## Descripción del Problema

El objetivo es asignar un conjunto de objetos con diferentes pesos al menor número posible de contenedores, sin exceder la capacidad máxima de cada uno. Este problema es de naturaleza NP-completa, lo que dificulta encontrar soluciones óptimas en tiempo razonable mediante métodos exactos.

## Implementación

Se desarrollaron tres scripts principales en Python:

1. **Código con Gurobi (`Codigo_Gurobi.py`)**: Utiliza el solver Gurobi para encontrar soluciones óptimas al problema.
2. **Código con Recocido Simulado (`Codigo_Recocido_simulado.py`)**: Implementa el algoritmo de recocido simulado para aproximar soluciones eficientes.
3. **Código Completo (`Codigo_completo.py`)**: Integra ambas metodologías y permite comparar sus resultados.

Además, se incluye el archivo `Resultados_Bin_Packing.xlsx` con los resultados obtenidos y análisis comparativos entre las soluciones de Gurobi y el recocido simulado.

## Requisitos

- Python 3.x
- Bibliotecas necesarias (instalación con `pip`):
  ```bash
  pip install numpy gurobipy
Nota: Gurobi requiere una licencia válida para su uso.

## Uso
- Clona el repositorio:
    ```bash
    git clone https://github.com/jbcgames/Trabajo-Final-Optimizacion.git
- Navega al directorio del proyecto:
    ```bash
    cd Trabajo-Final-Optimizacion
# Ejecuta el script deseado:
- Para Gurobi:
    ```bash
    python Codigo_Gurobi.py
- Para Recocido Simulado:
    ```bash
    python Codigo_Recocido_simulado.py
- Para el código completo:
    ```bash
    python Codigo_completo.py

## Resultados
Los resultados experimentales demuestran que el recocido simulado ofrece soluciones cercanas al óptimo en menor tiempo comparado con Gurobi, aunque con una ligera pérdida de precisión. Se recomienda ajustar parámetros como la temperatura inicial, el factor de enfriamiento y el número de iteraciones para optimizar el rendimiento del recocido simulado.

## Créditos
Este proyecto fue desarrollado por:

- Miguel Ángel Álvarez Guzmán
- Daniel Felipe Meneses Rojas
Para más detalles, consulta el informe final incluido en el repositorio.