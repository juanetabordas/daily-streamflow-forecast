import numpy as np
import pandas as pd
import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def Serie_Cuenca (Shapefile, Data, Latitudes, Longitudes, Fechas):
    cut_data, lon_lat_nc = cut(Shapefile, Data, Latitudes, Longitudes)
    fechas = Fechas
    mean_1 = np.nanmean(cut_data, axis=1)
    mean_cuenca = np.nanmean(mean_1, axis=1)
    mean_cuenca = pd.Series(mean_cuenca, index=fechas)
    return mean_cuenca

def cut(Shapefile, data, lats, lons):

    # "Encuentra las latitudes y las longitudes del shapefile"
    listx=[]
    listy=[]
    test = shapefile.Reader(Shapefile)
    for sr in test.shapeRecords():
        for xNew,yNew in sr.shape.points:
            listx.append(xNew)
            listy.append(yNew)
    # "Trues y Falses de posiciones que están dentro del shape"
    lons_lats_vect = np.column_stack((listx, listy))
    polygon        = Polygon(lons_lats_vect)
    resultado = []
    lon_lat   = []
    for i in lons:
        for j in lats:
            lon_lat.append([i,j])
            point = Point(i, j)
            resultado.append(polygon.contains(point))
    result  = np.array(resultado)
    lon_lat = np.array(lon_lat)
    # "Posiciones que están dentro del shape"
    lon_lat_nc = []
    for i in range(len(result)):
        if result[i] == True:
            lon_lat_nc.append(lon_lat[i])
    lon_lat_nc = np.array(lon_lat_nc)
    # "Matríz con 1's y NAN's para generar índice"
    mat_mult = np.zeros((data.shape[1], data.shape[2]))
    for P in lon_lat_nc:
        pos_lat = np.where(lats == P[1]) [0][0]
        pos_lon = np.where(lons == P[0]) [0][0]
        mat_mult[pos_lat, pos_lon] = 1
    mat_mult[mat_mult == 0] = np.NAN
    # "Cortando"
    cut_data = data * mat_mult
    return cut_data, lon_lat_nc



############################## CON POLIGONOS ############################################3333

def Serie_Cuenca_P (Polygon, Data, Latitudes, Longitudes, Fechas):
    
    cut_data, lon_lat_nc = cut_P(Polygon, Data, Latitudes, Longitudes)
    fechas = Fechas
    mean_1 = np.nanmean(cut_data, axis=1)
    mean_cuenca = np.nanmean(mean_1, axis=1)
    mean_cuenca = pd.Series(mean_cuenca, index=fechas)
    
    return mean_cuenca

def cut_P(polygon, data, lats, lons):
    
    resultado = []
    lon_lat   = []
    for i in lons:
        for j in lats:
            lon_lat.append([i,j])
            point = Point(i, j)
            resultado.append(polygon.contains(point))
    result  = np.array(resultado)
    lon_lat = np.array(lon_lat)

    # "Posiciones que están dentro del shape"
    lon_lat_nc = []
    for i in range(len(result)):
        if result[i] == True:
            lon_lat_nc.append(lon_lat[i])
    lon_lat_nc = np.array(lon_lat_nc)

    # "Matríz con 1's y NAN's para generar índice"
    mat_mult = np.zeros((data.shape[1], data.shape[2]))
    for P in lon_lat_nc:
        pos_lat = np.where(lats == P[1]) [0][0]
        pos_lon = np.where(lons == P[0]) [0][0]
        mat_mult[pos_lat, pos_lon] = 1
    mat_mult[mat_mult == 0] = np.NAN
    
    # "Cortando"
    cut_data = data * mat_mult
    return cut_data, lon_lat_nc

def Polygon_Generator(x_y_curve1, x_y_curve2):
    """
    Genera polígono a partir de la unión de varias curvas

    x_y_curve1: curva 1 definida por tuplas de x,y
    x_y_curve2: curva 2 definida por tuplas de x,y

    return: shapely.geometry.polygon
    """
    # x_y_curve1 = [(0.121,0.232),(2.898,4.554),(7.865,9.987)]
    # x_y_curve2 = [(1.221,1.232),(3.898,5.554),(8.865,7.987)]

    polygon_points = []

    for xyvalue in x_y_curve1:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 1

    for xyvalue in x_y_curve2[::-1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 2 in the reverse order (from last point to first point)

    for xyvalue in x_y_curve1[0:1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append the first point in curve 1 again, to it "closes" the polygon

    polygon = Polygon(polygon_points)

    return polygon
