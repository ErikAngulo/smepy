

import pandas as pd

numero = 0

class Dataset:
    """Clase Dataset para guardar los datos en Tablas"""

    
    def __sigNumero(self):
        """Asignar nombre al Dataset si usuario no ha proporcionado"""
        global numero
        numero += 1
        return str(numero)

    def __init__(self, datos, nombre=None):
        """Funcion constructora"""
        #datos como diccionario de columnas, key nombre, value vector
        df = pd.DataFrame(data=datos)
        if df.shape[0] < 2:
            raise Exception("La base de datos a crear debe de tener al menos dos filas")
        if nombre is None:
            nombre = self.__sigNumero()
        self.id = nombre
        self.data = df

    def __str__(self):
        "Imprimir el Dataset"
        imprimir = "Nombre del Dataset: {}\n".format(self.id)
        imprimir += "Columnas del Dataset: {}\n".format(self.data.shape[1])
        imprimir += "Filas del Dataset: {}\n".format(self.data.shape[0])
        imprimir += "Contenido del Dataset:\n"
        imprimir += str(self.data)
        return imprimir

    def nombres_columna(self, nombres):
        "Cambiar el nombre de las columnas"
        if len(nombres) == self.data.shape[1]:
            #array con el nombre de todas las columnas
            self.data.columns = nombres
        else:
            #diccionario con los nombres antiguos (key) y nombres nuevos (value)
            self.data = self.data.rename(nombres, axis='columns')


def leer_datos(path, nombre=None, encabezado = True, sep=",", decimal='.'):
    "Leer un fichero de tipo csv y convertir sus datos a Dataset"
    header = 0 if encabezado else None
    datos = pd.read_csv(path, sep=sep, decimal=decimal, header=header)
    return(Dataset(datos, nombre))

def guardar_datos(dataset, path):
    "Guardar el contenido del Dataset como csv"
    if isinstance(dataset, Dataset):
        dataset.data.to_csv(path, index=False)


