import pandas as pd
from shapely import wkt
from math import inf
import geopandas as gpd
import matplotlib.pyplot as plt


data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')

data = data.fillna({"harassmentRisk": data["harassmentRisk"].mean()})

graph = {}
origenes_unicos =  data.origin.unique()
for i in origenes_unicos:
    graph[i] = {}

#Vamos a definir 3 opciones para la ruta más optima segun:
#La menor distancia, el menor riesgo y la menor distancia con el menor riesgo
for i in range(len(data)):
    #graph[data["origin"][i]][data["destination"][i]] = (data["length"][i])
    #graph[data["origin"][i]][data["destination"][i]] = (data["harassmentRisk"][i])
    graph[data["origin"][i]][data["destination"][i]] = (data["length"][i] * data["harassmentRisk"][i])
    if  data["oneway"][i]== True:
            #graph[data["destination"][i]] = {data["origin"][i]: (data["length"][i])}
            #graph[data["destination"][i]] = {data["origin"][i]: (data["harassmentRisk"][i])}
            graph[data["destination"][i]] = {data["origin"][i]: (data["length"][i] * data["harassmentRisk"][i])}

    

def dijkstra(graph, start, goal):
    shortest_distance = {}  
    track_predecesor = {}  
    unseenNodes = graph 
    infinity = inf
    path = []


    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0


    while unseenNodes:
        min_distance_node = None

        for node in unseenNodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node
                
        path_options = graph[min_distance_node].items()
        
        for child_node, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecesor[child_node] = min_distance_node

        unseenNodes.pop(min_distance_node)

    currentNode = goal
    
    while currentNode is not start:
        try:
            path.insert(0, currentNode)
            currentNode = track_predecesor[currentNode]
        except KeyError:
            break
        
    path.insert(0, start)

    if shortest_distance[goal] != infinity:
        print("La valor mas corto es: " + str(shortest_distance[goal]))
        print("El camino mas optimo es: " + str(path))
        return path
        
    
origen = "(-75.5728593, 6.2115169)"
destino = "(-75.5666527, 6.2091202)"


resultado = dijkstra(graph, origen, destino)

#=======================================================

#intento de graficar la ruta más optima...
"""
#Load area
area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

#Load streets
edges = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
edges['harassmentRisk'] = edges['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(edges)


#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street edges
edges.plot(ax=ax, linewidth=0.3, column='harassmentRisk',legend=True, missing_kwds={'color': 'dimgray'})

plt.title("Ruta mas optimna")
plt.tight_layout()
plt.savefig("rutaOptima.png")
"""