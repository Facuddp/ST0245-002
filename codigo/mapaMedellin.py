# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:56:32 2022

@author: WINDOWS 11
"""
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt

#Load area
area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)


#Load streets
edges = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
edges['geometry'] = edges['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(edges)



#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street edges
edges.plot(ax=ax, linewidth=0.3, column='harassmentRisk', legend=True, missing_kwds={'color': 'dimgray'})

plt.title("Riesgo de acoso en las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-riesgo-de-acoso.png")



fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street edges
edges.plot(ax=ax, linewidth=0.3, column='length', legend=True, missing_kwds={'color': 'dimgray'})

plt.title("Longitud en metros de las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-de-called-con-longitud.png")

