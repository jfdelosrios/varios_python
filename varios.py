# -*- coding: utf-8 -*-
"""varios.py"""

from os import system 
from IPython.display import clear_output
import json
import pandas as pd
from sqlite3 import connect


def cacharrearBaseDatos(_path:str, query:str) ->dict:
  """
  Ejecuta un query en una base de datos que se encuentra en el path.
  En la salida genera un diccionario que tiene las claves:

  * status: da a conocer si fue satisfactoria la consulta.
  
  * out: dataFrame.
  """
  
  try:
    conn = connect(_path)
    tabla = pd.read_sql(query, conn)
  except pd.io.sql.DatabaseError as error:
    return {'status': ['error', error], 'out': pd.DataFrame()}

  return {'status': ['ok', ''], 'out': tabla}


def limpiarPantalla(_plataforma:str='') -> None:
  """Limpia pantalla e terminal"""
  
  if(_plataforma=='colab'):
    clear_output()
  else:
    system('cls')


def leer_json(_path:str) -> dict:
  """Lee archivo json desde una ubicacion especifica."""

  try:
    with open(_path) as f:
      _json=json.load(f)
  except FileNotFoundError as error:
    return {'status':['error', error], 'out': dict()}
  except json.decoder.JSONDecodeError as error:
    return {'status':['error', 'Error de lectura de {} . {}'.format(_path, error)], 'out': dict()}

  return {'status':['ok', ''], 'out': _json}


def floor2(number: float, n: int = 0) -> float:
  """Redondea flotante n cantidad de digitos decimales."""

  if((number - round(number, n)) < 0):
    return round(round(number, n) - pow(10, -n), n)
  else:
    return round(number, n)