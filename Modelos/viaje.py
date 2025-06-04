from datetime import date
from typing import List, Optional
from Modelos.gasto import Gasto
from Modelos.enums import TipoGasto, FormaPago


class Viaje:
    """
    Atributos:
        id (str): Identificador único
        destino (str): Nombre del destino
        es_exterior (bool): Indica si es internacional
        fecha_inicio (date): Fecha de inicio
        fecha_fin (date): Fecha de finalización
        presupuesto_diario (float): Presupuesto diario en COP
        gastos (List[Gasto]): Lista de gastos asociados
    """

    def __init__(self, id: str, destino: str, es_exterior: bool,
                 fecha_inicio: date, fecha_fin: date, presupuesto_diario: float):
        """
        Args:
            id: Identificador único del viaje
            destino: Nombre del lugar de destino
            es_exterior: True si es un viaje internacional
            fecha_inicio: Fecha de inicio del viaje
            fecha_fin: Fecha de finalización
            presupuesto_diario: Presupuesto diario en pesos colombianos
        """
        self.id = id
        self.destino = destino
        self.es_exterior = es_exterior
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.gastos = []

    def agregar_gasto(self, gasto: Gasto):
        """
        Agrega un gasto al viaje después de validaciones

        Args:
            gasto: Objeto Gasto a agregar

        Raises:
            ValueError: Si la fecha del gasto no está en el rango del viaje
        """
        if not self.validar_fecha(gasto.fecha):
            raise ValueError("La fecha del gasto no está dentro del viaje")
        self.gastos.append(gasto)

    def validar_fecha(self, fecha: date) -> bool:
        """
        Valida si una fecha está dentro del rango del viaje

        Args:
            fecha: Fecha a validar

        Returns:
            bool: True si la fecha es válida, False en caso contrario
        """
        return self.fecha_inicio <= fecha <= self.fecha_fin

    def calcular_gasto_dia(self, fecha: date) -> float:
        """
        Args:
            fecha: Fecha para calcular gastos

        Returns:
            float: Suma de gastos del día en COP

        Raises:
            ValueError: Si la fecha no está en el rango del viaje
        """
        if not self.validar_fecha(fecha):
            raise ValueError("Fecha fuera del rango del viaje")

        return sum(
            gasto.valor_pesos
            for gasto in self.gastos
            if gasto.fecha == fecha
        )

    def calcular_diferencia_presupuesto(self, fecha: date) -> float:
        """
        Calcula la diferencia entre el presupuesto y gastos de un día

        Args:
            fecha: Fecha para calcular diferencia

        Returns:
            float: Diferencia (presupuesto - gastos)
        """
        gasto_total = self.calcular_gasto_dia(fecha)
        return self.presupuesto_diario - gasto_total