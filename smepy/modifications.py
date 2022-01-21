

import pandas as pd
import numpy as np
from .dataset import Dataset


def normalizar(dataset):
    "Normaliza las columnas numericas del Dataset"
    newDf = dataset.data.copy()

    for columna in newDf.select_dtypes(include='number'):
        minimo = newDf[columna].min()
        maximo = newDf[columna].max()
        newDf[columna] = newDf[columna].apply(lambda x: (x-minimo)/(maximo-minimo))
    newDs = Dataset(newDf, "{}_norm".format(dataset.id))
    return(newDs)

def estandarizar(dataset):
    "Estandariza las columnas numericas del Dataset"
    newDf = dataset.data.copy()

    for columna in newDf.select_dtypes(include='number'):
        media = newDf[columna].mean()
        desviacion = newDf[columna].std()
        newDf[columna] = newDf[columna].apply(lambda x: (x-media)/(desviacion))
    newDs = Dataset(newDf, "{}_estand".format(dataset.id))
    return(newDs)


def filtrar(dataset, funcion):
    "Conseguir un subset de los datos donde se cumpla la funcion"
    newDf = dataset.data.query(funcion)
    newDs = Dataset(newDf, "{}_filt".format(dataset.id))
    return newDs


