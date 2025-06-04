"""
Módulo que contiene las enumeraciones del sistema
"""

from enum import Enum

class TipoGasto(Enum):
    TRANSPORTE = 1
    ALOJAMIENTO = 2
    ALIMENTACION = 3
    ENTRETENIMIENTO = 4
    COMPRAS = 5

class FormaPago(Enum):
    EFECTIVO = 1
    TARJETA = 2