import pandas as pd
from shapely import wkt
import geopandas as gpd
import matplotlib.pyplot as plt
import heapq
from collections import deque


data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')

data = data.fillna({"harassmentRisk": data["harassmentRisk"].mean()})

#se crea grafo
def createGraph1(data):
    graph1={}
    origenes_unicos =  data.origin.unique()
    for i in origenes_unicos:
        graph1[i] = {}
    for i in range(len(data.harassmentRisk)):
      if not(data.origin[i] in graph1):
          graph1[data.origin[i]]={}
          graph1[data.origin[i]][data.destination[i]]= ((data.length[i]),(data.harassmentRisk[i]))
      else:
          graph1[data.origin[i]][data.destination[i]]= ((data.length[i]),(data.harassmentRisk[i]))
      
      if not(data.destination[i] in graph1) and (data.oneway[i] == True) :
          graph1[data.destination[i]]={}
          graph1[data.destination[i]][data.origin[i]]= ((data.length[i]),(data.harassmentRisk[i]))
    return graph1

#menor distancia
def dijkstra1(graph, start, goal):
    risk = 0
    distances = {vertex: float('infinity') for vertex in graph}
    previous = {vertex: None for vertex in graph}

    distances[start] = 0
    previous[start] = None

    cola = [(distances[start], start)]

    while cola:
        distance, actual = heapq.heappop(cola)
        if actual == goal:
            break
        for hijos in graph[actual]:
            distance = distances[actual] + (((graph[actual][hijos][0])))
            
            try:
                if distance < distances[hijos]:
                    risk += graph[actual][hijos][1]
                    distances[hijos] = distance
                    previous[hijos] = actual
                    heapq.heappush(cola, (distance, hijos))
            except KeyError:
                continue
        
    return previous, risk / len(previous)

#menor riesgo
def dijkstra2(graph, start, goal):
    risk = 0
    distances = {vertex: float('infinity') for vertex in graph}
    previous = {vertex: None for vertex in graph}

    distances[start] = 0
    previous[start] = None

    cola = [(distances[start], start)]

    while cola:
        distance, actual = heapq.heappop(cola)
        if actual == goal:
            break
        for hijos in graph[actual]:
            distance = distances[actual] + (((graph[actual][hijos][1])))
            
            try:
                if distance < distances[hijos]:
                    risk += graph[actual][hijos][1]
                    distances[hijos] = distance
                    previous[hijos] = actual
                    heapq.heappush(cola, (distance, hijos))
            except KeyError:
                continue
        
    return previous, risk / len(previous)

#menor distancia y riesgo
def dijkstra3(graph, start, goal):
    risk = 0
    distances = {vertex: float('infinity') for vertex in graph}
    previous = {vertex: None for vertex in graph}

    distances[start] = 0
    previous[start] = None

    cola = [(distances[start], start)]

    while cola:
        distance, actual = heapq.heappop(cola)
        if actual == goal:
            break
        for hijos in graph[actual]:
            distance = distances[actual] + (0.1+(graph[actual][hijos][1])) * (graph[actual][hijos][0])
            
            try:
                if distance < distances[hijos]:
                    risk += graph[actual][hijos][1]
                    distances[hijos] = distance
                    previous[hijos] = actual
                    heapq.heappush(cola, (distance, hijos))
            except KeyError:
                continue
        
    return previous, risk / len(previous)


def path(previo, actual, ruta):
    if previo[actual] is None:
        ruta.append(actual)
        return ruta
    else:
        ruta.append(actual)
        return path(previo, previo[actual], ruta)

graph = createGraph1(data)

start = "(-75.5774817, 6.2000058)"
goal = "(-75.5796501, 6.260673)"

#ruta1

ruta_distancia = dijkstra1(graph, start, goal)
ruta11 = deque()
path1 = path(ruta_distancia[0], goal, ruta11)

ruta1 = []
length1 = 0
while path1:
    nodo = path1.pop()
    ruta1.append(nodo)
    if path1:
        next1 = path1.pop()
        length1 += graph[nodo][next1][0]
        path1.append(next1)
        
print("==============================") 
print("Camino con menor distancia:")
print("Riesgo promedio:", ruta_distancia[1])
print("Distancia total: ", length1)
print("==============================")

#=======================================================
#ruta2
ruta_riesgo = dijkstra2(graph, start, goal)
ruta22 = deque()
path2 = path(ruta_riesgo[0], goal, ruta22)

ruta2 = []
length2 = 0
while path2:
    nodo = path2.pop()
    ruta2.append(nodo)
    if path2:
        next2 = path2.pop()
        length2 += graph[nodo][next2][0]
        path2.append(next2)
print("Camino con menor riesgo:")
print("Riesgo promedio:", ruta_riesgo[1])
print("Distancia total: ", length2)
print("==============================")            
#=======================================================
#ruta3
ruta_promedio = dijkstra3(graph, start, goal)
ruta33 = deque()
path3 = path(ruta_promedio[0], goal, ruta22)

ruta3 = []
length3 = 0
while path2:
    nodo = path3.pop()
    ruta3.append(nodo)
    if path2:
        next3 = path3.pop()
        length3 += graph[nodo][next3][0]
        path3.append(next3)
print("Camino con menor distancia y riesgo:")
print("Riesgo promedio:", ruta_promedio[1])
print("Distancia total: ", length3)   
print("==============================")
#=======================================================

#intento de graficar la ruta más optima...
area = pd.read_csv('poligono_de_medellin.csv', sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

# Load streets

#ruta 1
edges1 = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
edges1['harassmentRisk'] = edges1['harassmentRisk'].fillna(edges1['harassmentRisk'].mean())
edges1.loc[edges1.harassmentRisk < 50, 'harassmentRisk'] = 0
for i in range(len(ruta1) - 2):
    edges1.loc[(edges1['origin'] == ruta1[i]) &
               (edges1['destination'] == ruta1[i + 1]), 'harassmentRisk'] = 100
edges1 = edges1.loc[edges1['harassmentRisk'] > 0]
edges1['geometry'] = edges1['geometry'].apply(wkt.loads)
edges1 = gpd.GeoDataFrame(edges1)


#ruta 2
edges2 = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
edges2['harassmentRisk'] = edges2['harassmentRisk'].fillna(
    edges2['harassmentRisk'].mean())
edges2.loc[edges2.harassmentRisk < 50, 'harassmentRisk'] = 0
for i in range(len(ruta2) - 2):
    edges2.loc[(edges2['origin'] == ruta2[i]) &
               (edges2['destination'] == ruta2[i + 1]), 'harassmentRisk'] = 100
edges2 = edges2.loc[edges2['harassmentRisk'] > 0]
edges2['geometry'] = edges2['geometry'].apply(wkt.loads)
edges2 = gpd.GeoDataFrame(edges2)


#ruta 3
edges3 = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
edges3['harassmentRisk'] = edges3['harassmentRisk'].fillna(
    edges3['harassmentRisk'].mean())
edges3.loc[edges3.harassmentRisk < 50, 'harassmentRisk'] = 0
for i in range(len(ruta3) - 2):
    edges3.loc[(edges3['origin'] == ruta3[i]) &
               (edges3['destination'] == ruta3[i + 1]), 'harassmentRisk'] = 100
edges3 = edges3.loc[edges3['harassmentRisk'] > 0]
edges3['geometry'] = edges3['geometry'].apply(wkt.loads)
edges3 = gpd.GeoDataFrame(edges3)



# Create plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street edges
edges1.plot(ax=ax, linewidth=1, color='green', label="Menor distancia")
edges2.plot(ax=ax, linewidth=1, color='yellow', label="Menos riesgo")
edges3.plot(ax=ax, linewidth=1, color='purple', label="Menor distancia y riesgo")

plt.title("Rutas que reducen acoso en medellin")
plt.tight_layout()
plt.legend(title="Calles", loc="upper right")
plt.savefig("Mapa_tres_caminos.png")

