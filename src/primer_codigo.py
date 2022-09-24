#print("Hello World")
from operator import truediv
import numpy as np
import argparse
import pandas as pd

def calcular_min_max(lista_numeros, verbose=1):
    ''' 
    Retorna los valores minimo y maximo de una lista de numeros
    Args:
        lista_numeros: type list
    '''
    
    min_value = min(lista_numeros)
    max_value = max(lista_numeros)

    if verbose == 1:
        print('Valor minimo:', min_value)
        print('Valor maximo:', max_value)
    else:
        pass
    return min_value, max_value

def calcular_valores_centrales(lista_numeros, verbose= 1):
    """Calcula la media y la desviacion estandar de una lñista de numeros

    Args:
        lista_numeros (list): lista con valores numericos
        verbose (bool, optional): para decidir si imprimir mensajes en pantalla. Defaults to True.

    Returns:
        tuple : (media, dev_std)
    """
    media = np.mean(lista_numeros)
    dev_std = np.std(lista_numeros)

    if verbose == 1:
        print('Media :', media)
        print('Desviacion Estandar :', dev_std)
    else:
        pass

    return media, dev_std


def calcular_valores(lista_numeros, verbose = 1):
    """Retorna una tupla con los valores suma, minimo, maximo, media y dev std

    Args:
        lista_numeros (_type_): _description_
        verbose (_type_): _description_

    Returns:
        _type_: _description_
    """
    suma = np.sum(lista_numeros)
    if verbose == 1:
        print('Suma :', suma)
    else:
        pass

    min_val, max_val = calcular_min_max(lista_numeros, verbose)
    media, dev_std = calcular_valores_centrales(lista_numeros)
     
    return suma, min_val, max_val, media, dev_std

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", type= int, default= 1, help="para imprimir en pantalla")
    args = parser.parse_args()

    print("*****", args.verbose, type(args.verbose))

    lista_valores = [5, 4, 8, 9, 21]
    calcular_valores(lista_valores, verbose=args.verbose)

if __name__ == '__main__':
    main()
