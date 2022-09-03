# -*- coding: utf-8 -*-
"""varios.py"""

from os import system 
from IPython.display import clear_output
from json import load
from json.decoder import JSONDecodeError
from pandas import DataFrame, read_sql
from pandas.io.sql import DatabaseError
from sqlite3 import connect
from msvcrt import kbhit
from datetime import datetime
from pytz import timezone

def cacharrearBaseDatos(_path:str, query:str) -> dict[list[str,str],DataFrame]:
  """
  Ejecuta un query en una base de datos que se encuentra en el path.
  En la salida genera un diccionario que tiene las claves:

  * status: da a conocer si fue satisfactoria la consulta.
  
  * out: dataFrame.
  """
  
  try:
    conn = connect(_path)
  except DatabaseError as error:
    return {'status': ['error', error], 'out': DataFrame()}
  
  try:
    tabla = read_sql(query, conn)
  except DatabaseError as error:
    return {'status': ['error', error], 'out': DataFrame()}

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
      _json = load(f)
  except FileNotFoundError as error:
    return {'status':['error', error], 'out': dict()}
  except JSONDecodeError as error:
    return {'status':['error', 'Error de lectura de {} . {}'.format(_path, error)], 'out': dict()}

  return {'status':['ok', ''], 'out': _json}


def floor2(number: float, n: int = 0) -> float:
  """Redondea flotante n cantidad de digitos decimales."""

  if((number - round(number, n)) < 0):
    return round(round(number, n) - pow(10, -n), n)
  else:
    return round(number, n)


def EncontrarFechaBarraActual(_timeFrame: str) -> int:
    """
    Suponiendo que el mercado esta abierto, 
    Encuentra cual es la fecha asignada a la barra actual para cierto timeFrame.
    
    No funciono bien la función datetime.utcnow()
    """

    _fecha = transformarTiempo(
            _fecha = datetime.now(tz = timezone('UTC')), 
            _timeFrame = _timeFrame
            )

    return datetime.timestamp(_fecha)


def transformarTiempo(_fecha: datetime, _timeFrame:str) -> datetime:
    """

    para un timeframe (_interval). ver constantes KLINE_INTERVAL

    https://python-binance.readthedocs.io/en/latest/constants.html
    
    Devuelve un datetime acorde a la apertura de la barra .
    """
    
    _fecha = _fecha.replace(second = 0, microsecond = 0)

    if(_timeFrame == '1m'):
        return _fecha

    if(_timeFrame == '3m'):
        return _fecha.replace(minute = int(_fecha.minute / 3) * 3)

    if(_timeFrame == '5m'):
        return _fecha.replace(minute = int(_fecha.minute / 5) * 5)

    if(_timeFrame == '15m'):
        return _fecha.replace(minute = int(_fecha.minute / 15) * 15)

    if(_timeFrame == '30m'):
        return _fecha.replace(minute = int(_fecha.minute / 30) * 30)
        
    _fecha = _fecha.replace(minute = 0)

    if(_timeFrame == '1h'):
      return _fecha

    if(_timeFrame == '2h'):
      return _fecha.replace(hour = int(_fecha.hour / 2) * 2)

    if(_timeFrame == '4h'):
      return _fecha.replace(hour = int(_fecha.hour / 4) * 4)

    if(_timeFrame == '6h'):
        return _fecha.replace(hour = int(_fecha.hour / 6) * 6)

    if(_timeFrame == '8h'):
        return _fecha.replace(hour = int(_fecha.hour / 8) * 8)

    if(_timeFrame == '12h'):
        return _fecha.replace(hour = int(_fecha.hour / 12) * 12)

    _fecha = _fecha.replace(hour = 0)

    if(_timeFrame == '1d'):
        return _fecha

    if(_timeFrame == '3d'):
        return _fecha.replace(day = int(_fecha.day / 3) * 3)

    if(_timeFrame == '1w'):
      return -1 #falta por programar

    _fecha = _fecha.replace(day = 1)

    if(_timeFrame == '1M'):
        return _fecha

    return -1


def pausar() -> None:
    """Espera a que el usuario oprima una tecla para continuar."""

    print('\nOprima una tecla para finalizar.')

    while(True):

        if (not (kbhit())):
            continue

        return