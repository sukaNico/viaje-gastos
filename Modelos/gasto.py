from datetime import date
from Modelos.enums import TipoGasto, FormaPago


class Gasto:
    """
    Clase que representa un gasto realizado durante un viaje

    Atributos:
        id (str): Identificador único
        fecha (date): Fecha del gasto
        valor_original (float): Valor en moneda original
        valor_pesos (float): Valor convertido a pesos
        tipo (TipoGasto): Categoría del gasto
        forma_pago (FormaPago): Método de pago utilizado
        moneda_original (str): Código de moneda (ej. 'USD')
    """

    def __init__(self, id: str, fecha: date, valor_original: float,
                 tipo: TipoGasto, forma_pago: FormaPago, moneda_original: str):
        """
        Constructor de la clase Gasto

        Args:
            id: Identificador único del gasto
            fecha: Fecha cuando se realizó el gasto
            valor_original: Monto en la moneda original
            tipo: Categorización del gasto
            forma_pago: Método de pago utilizado
            moneda_original: Código ISO de la moneda
        """
        self.id = id
        self.fecha = fecha
        self.valor_original = valor_original
        self.valor_pesos = 0.0  # Se calcula posteriormente
        self.tipo = tipo
        self.forma_pago = forma_pago
        self.moneda_original = moneda_original

    def convertir_a_pesos(self, tasa_cambio: float):
        """
        Args:
            tasa_cambio: Tasa de conversión de la moneda original a COP
        """
        if tasa_cambio <= 0:
            raise ValueError("La tasa de cambio debe ser positiva")
        self.valor_pesos = self.valor_original * tasa_cambio