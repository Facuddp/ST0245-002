# Medellín Shortest Path Visualization

Este proyecto grafica el mapa de Medellín mostrando el camino más corto desde el punto A (Universidad EAFIT) hasta el punto B (Universidad Nacional) utilizando Python y el algoritmo de Dijkstra, implementado con grafos y estructuras de datos únicas.

Se proponen 3 soluciones a los caminos más cortos tomando en cuenta diferentes variables como lo son el riesgo de acoso y la distancia más corta. Uno priorizando la distancia y el riesgo, otro solo el riesgo y otro solo la distancia. 

Se puede ver más información sobre la investigación del proyecto, la complejidad del algoritmo implementado y los tiempos de ejecución en los documentos proporcionados.

## Tecnologías Utilizadas

- **Algoritmo**: Dijkstra
- **Lenguaje**: Python
- **Bibliotecas**:
  - `pandas` para manipulación y análisis de datos
  - `geopandas` para trabajar con datos geoespaciales
  - `matplotlib` para la visualización de datos
  - `shapely` para la manipulación de geometrías

## Características

- **Cálculo del Camino Más Corto**: Implementación del algoritmo de Dijkstra para encontrar la ruta más corta entre dos puntos en un grafo que representa la ciudad de Medellín.
- **Visualización del Mapa**: Representación gráfica del mapa de Medellín y la ruta calculada utilizando `geopandas` y `matplotlib`.
- **Manipulación Geométrica**: Uso de `shapely` para operaciones geométricas y manejo de datos espaciales.
