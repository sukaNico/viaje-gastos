import unittest
from datetime import date
from Modelos.enums import TipoGasto, FormaPago
from Modelos.gasto import Gasto
from Modelos.viaje import Viaje
from Modelos.conversor_moneda import ConversorMoneda

from unittest.mock import patch


class TestSistemaGastos(unittest.TestCase):

    def setUp(self):
        # Viaje activo del 01 al 07 de enero de 2023
        self.viaje = Viaje(
            id="V001",
            destino="Cartagena",
            es_exterior=False,
            fecha_inicio=date(2023, 1, 1),
            fecha_fin=date(2023, 1, 7),
            presupuesto_diario=200000
        )

    def test_01_suma_correcta_de_gastos_diarios(self):
        gasto1 = Gasto("G001", date(2023, 1, 2), 100000, TipoGasto.ALIMENTACION, FormaPago.EFECTIVO, "COP")
        gasto1.convertir_a_pesos(1.0)

        gasto2 = Gasto("G002", date(2023, 1, 2), 50000, TipoGasto.TRANSPORTE, FormaPago.EFECTIVO, "COP")
        gasto2.convertir_a_pesos(1.0)

        self.viaje.agregar_gasto(gasto1)
        self.viaje.agregar_gasto(gasto2)

        total_gastos = self.viaje.calcular_gasto_dia(date(2023, 1, 2))
        self.assertEqual(total_gastos, 150000)

    def test_02_fecha_fuera_del_rango(self):
        gasto_fuera = Gasto("G003", date(2023, 1, 10), 30000, TipoGasto.ENTRETENIMIENTO, FormaPago.TARJETA, "COP")
        with self.assertRaises(ValueError) as context:
            self.viaje.agregar_gasto(gasto_fuera)
        self.assertEqual(str(context.exception), "La fecha del gasto no está dentro del viaje")

    @patch("Modelos.conversor_moneda.requests.get")
    def test_03_conversion_exitosa_usd_a_cop(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "rates": {"COP": 3900}
        }

        conversor = ConversorMoneda()
        tasa = conversor.obtener_tasa_cambio("USD", "COP")
        self.assertEqual(tasa, 3900)

    @patch("Modelos.conversor_moneda.requests.get", side_effect=ConnectionError("Timeout"))
    def test_04_api_no_responde(self, mock_get):
        conversor = ConversorMoneda()
        with self.assertRaises(ConnectionError):
            conversor.obtener_tasa_cambio("EUR", "COP")


if __name__ == "__main__":
    unittest.main()
