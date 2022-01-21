

import pandas as pd
import numpy as np
from .dataset import Dataset


def normalizar(dataset):
    """Normaliza las columnas numericas del Dataset"""
    newDf = dataset.data.copy()

    for columna in newDf.select_dtypes(include='number'):
        minimo = newDf[columna].min()
        maximo = newDf[columna].max()
        newDf[columna] = newDf[columna].apply(lambda x: (x-minimo)/(maximo-minimo))
    newDs = Dataset(newDf, "{}_norm".format(dataset.id))
    return(newDs)

def estandarizar(dataset):
    """Estandariza las columnas numericas del Dataset"""
    newDf = dataset.data.copy()

    for columna in newDf.select_dtypes(include='number'):
        media = newDf[columna].mean()
        desviacion = newDf[columna].std()
        newDf[columna] = newDf[columna].apply(lambda x: (x-media)/(desviacion))
    newDs = Dataset(newDf, "{}_estand".format(dataset.id))
    return(newDs)


def filtrar(dataset, funcion):
    """Conseguir un subset de los datos donde se cumpla la funcion"""
    newDf = dataset.data.query(funcion)
    newDs = Dataset(newDf, "{}_filt".format(dataset.id))
    return newDs


class Discretizar:

    def discretizeCutPoints(self, x, cut_points):

        x_discretized = []
        for elem in x:
            if elem <= cut_points[0]:
                x_discretized.append('(-Inf,{}]'.format(cut_points[0]))
            elif elem > cut_points[-1]:
                x_discretized.append('({},+Inf)'.format(cut_points[-1]))
            else:
                for limite in range(1, len(cut_points)): #tramos desde el segundo punto a X, y de X al último punto de corte
                    if elem <= cut_points[limite]:
                        x_discretized.append('({},{}]'.format(cut_points[limite-1], cut_points[limite]))
                        break

        return(x_discretized)


    def discretizeEW(self,x, num_bins):
        minimo = min(x)
        maximo = max(x)
        intervalo = maximo - minimo
        tramo = float(format(intervalo / num_bins, '.4f'))
        cut_points=[]
        for i in range(1, num_bins): #3 puntos de corte
            cut_points.append(minimo + i * tramo)

        x_discretized = self.discretizeCutPoints(x, cut_points)
        return(x_discretized)


    def discretizeEF(self,x, num_bins):
        x_discretized = [0] * len(x)
        orderedIndeX = np.argsort(x)
        intervalo = len(x) / num_bins
        cut_points = []
        for i in range(1, num_bins): #sacar punto de corte y asignarlo los elementos del tramo 
            cutIndex = round(i * intervalo) - 1 #al empezar array en 0, desplazar corte una pos izq
            cut_points.append( x[orderedIndeX[cutIndex]] )
            
        #si quedan menos elementos que tramos, hay numeros repetidos en el vector a discretizar
        cut_points = np.unique(cut_points)
        
        x_discretized = self.discretizeCutPoints(x, cut_points)
        return(x_discretized)
    


def discretizar(dataset, columnas=None, metodo="frecuencia", puntos_corte=3):
    """
    Discretizar las columnas seleccionadas numericas del Dataset en tramos
    Con igual anchura o igual frecuencia, se dividiran en tramos (seleccionados en puntos_corte)
    y se conseguiran los puntos de corte conseguidos de cada algoritmo. Despues se discretizara con esos puntos
    Con manual, se discretizara con los puntos de corte proporcionados como vector en puntos_corte
    """
    if columnas is None:
        columnas = list(dataset.data.columns)

    dis = Discretizar()

    newDf = dataset.data.copy()

    if metodo == "frecuencia":
        for columna in newDf[columnas].select_dtypes(include='number'):
            valores = newDf[columna].to_numpy()
            discretizado = dis.discretizeEF(valores, puntos_corte)
            newDf[columna] = discretizado

    if metodo == "anchura":
        for columna in newDf[columnas].select_dtypes(include='number'):
            valores = newDf[columna].to_numpy()
            discretizado = dis.discretizeEW(valores, puntos_corte)
            newDf[columna] = discretizado

    if metodo == "manual":
        for columna in newDf[columnas].select_dtypes(include='number'):
            valores = newDf[columna].to_numpy()
            discretizado = dis.discretizeCutPoints(valores, puntos_corte)
            newDf[columna] = discretizado

    newDs = Dataset(newDf, "{}_{}".format(dataset.id, metodo))
    return newDs
    