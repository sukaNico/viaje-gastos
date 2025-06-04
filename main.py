"""
Módulo principal con ejemplo de uso del sistema
"""

from datetime import date
from Modelos.viaje import Viaje
from Modelos.gasto import Gasto
from Modelos.enums import TipoGasto, FormaPago
from Modelos.conversor_moneda import ConversorMoneda


def main():
    # Configuración inicial
    conversor = ConversorMoneda()

    # Crear un viaje a Nueva York
    viaje = Viaje(
        id="nyc-2023",
        destino="Nueva York",
        es_exterior=True,
        fecha_inicio=date(2023, 6, 1),
        fecha_fin=date(2023, 6, 7),
        presupuesto_diario=300000  # 300,000 COP por día
    )

    try:
        # Registrar un gasto en USD
        tasa = conversor.obtener_tasa_cambio("USD", "COP")
        gasto_comida = Gasto(
            id="g1",
            fecha=date(2023, 6, 2),
            valor_original=25.50,  # USD
            tipo=TipoGasto.ALIMENTACION,
            forma_pago=FormaPago.TARJETA,
            moneda_original="USD"
        )
        gasto_comida.convertir_a_pesos(tasa)

        viaje.agregar_gasto(gasto_comida)

        # Calcular diferencia
        diferencia = viaje.calcular_diferencia_presupuesto(date(2023, 6, 2))
        print(f"Diferencia con presupuesto: {diferencia:,.2f} COP")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()