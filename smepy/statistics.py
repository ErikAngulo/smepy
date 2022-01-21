

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sn
from .dataset import Dataset

def varianzas(dataset):
    """Calcula la varianza de las columnas numericas"""
    numericas = dataset.data.select_dtypes(include='number')
    return(numericas.var())

class Estadisticos:

    ############### Entropia ###############

    def entropy(self, x):
        """Calcula la entropia"""
        count = {}
        for elem in x:
            count[elem] = count.get(elem, 0) + 1
        
        H = 0
        
        for key, value in count.items():
            prop = value / len(x)
            H -= prop * math.log(prop, 2)
            
        return H


    def entropyNormalized(self, df, normalizar=True):
        """Calcula la entropia de cada columna, normalizando por defecto"""
        entropies = df.apply(self.entropy, axis=0)
        if normalizar:
            #dividir los valores de cada columna por el logaritmo de cantidad valores distintos tenga la columna
            entropies = entropies.divide(np.log2(df.nunique()))
        return entropies

    ############# Mutual information ########

    def mutual_infor(self, X, y):
        """Informacion mutua de dos variables"""

        X_level = list(set(X))
        y_level = list(set(y))
        N = X.shape[0]
        I = 0

        for i in X_level:
            for j in y_level:
                p_xy = np.sum(y[X == i] == j) / N
                p_x = np.sum(X == i) /N
                p_y = np.sum(y == j) /N
                if p_xy == 0.0:
                    continue
                I += p_xy * np.log(p_xy / (p_y * p_x))

        return I


    #####################################



        
def entropias(dataset, normalizar=True, plot=False):
    """Calcula la entropia de cada columna, normalizando por defecto"""

    est = Estadisticos()
    entr = est.entropyNormalized(dataset.data, normalizar)
    if plot:
        entr.plot.bar(x='Columna', y='Entropia')

    return entr

def graficoBoxplot(dataset):
    """Visualizar Boxplot de cada variable"""
    dataset.data.boxplot()

def correlaciones(dataset, plot=False):
    """Calcular correlaciones de las variables numericas"""
    corrMatrix = dataset.data.select_dtypes(include='number').corr()
    if plot:
        sn.heatmap(corrMatrix, annot=True)
        plt.show()
    return(corrMatrix)

def infmutuas(dataset, plot=False):
    """Calcular informacion mutua de las variables string"""
    est = Estadisticos()
    colString = (dataset.data.applymap(type) == str).all(0)
    dfString = dataset.data[dataset.data.columns[colString]]
    vectores = dfString.to_numpy().T
    inf = np.zeros((len(vectores), len(vectores)))
    for i in range(0, len(vectores)):
        for j in range(i, len(vectores)):
            I = est.mutual_infor(vectores[i], vectores[j])
            inf[i,j] = I
            inf[j, i] = I
    if plot:
        sn.heatmap(inf, annot=True)
        plt.show()

    return inf


