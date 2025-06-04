"""
Módulo para manejar la conversión de monedas usando API externa
"""

import requests
from typing import Optional


class ConversorMoneda:
    """
    Clase que maneja la conversión de monedas usando tasas de cambio actualizadas

    Atributos:
        api_url (str): Endpoint base de la API
        cache_tasas (dict): Diccionario para cachear tasas
    """

    def __init__(self, api_url: str = "https://api.exchangerate-api.com/v4/latest/"):
        """
        Inicializa el conversor con la URL base

        Args:
            api_url: URL base de la API de tasas de cambio
        """
        self.api_url = api_url
        self.cache_tasas = {}

    def obtener_tasa_cambio(self, moneda_origen: str, moneda_destino: str) -> float:
        """
        Obtiene la tasa de cambio entre dos monedas

        Args:
            moneda_origen: Código de moneda origen (ej. 'USD')
            moneda_destino: Código de moneda destino (ej. 'COP')

        Returns:
            float: Tasa de conversión

        Raises:
            ConnectionError: Si falla la conexión con la API
            ValueError: Si las monedas no son válidas
        """
        if moneda_origen == moneda_destino:
            return 1.0

        clave_cache = f"{moneda_origen}_{moneda_destino}"
        if clave_cache in self.cache_tasas:
            return self.cache_tasas[clave_cache]

        try:
            respuesta = requests.get(f"{self.api_url}{moneda_origen}")
            respuesta.raise_for_status()
            datos = respuesta.json()

            if moneda_destino not in datos['rates']:
                raise ValueError(f"Moneda destino {moneda_destino} no soportada")

            tasa = datos['rates'][moneda_destino]
            self.cache_tasas[clave_cache] = tasa
            return tasa

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error al conectar con API: {str(e)}")