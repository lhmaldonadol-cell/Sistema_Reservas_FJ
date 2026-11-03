
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: prueba_reservas.py
#
# DESCRIPCIÓN:
# Este archivo contiene las pruebas del módulo de reservas.
#
# OBJETIVOS:
# - Comprobar la creación de reservas.
# - Validar la confirmación y cancelación.
# - Verificar el cálculo de costos.
# - Detectar operaciones incorrectas.
# - Comprobar el encadenamiento de excepciones.
# - Verificar la continuidad después de los errores.
# - Generar registros en el archivo sistema.log.
#
# Las pruebas utilizan datos simulados.
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTACIÓN DE CLASES Y EXCEPCIONES
# ------------------------------------------------------------

# Importamos la clase Cliente.
from cliente import Cliente

# Importamos las clases especializadas de servicios.
from servicio import (
    ServicioSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

# Importamos la clase que administra las reservas.
from reserva import Reserva

# Importamos las excepciones que controlaremos.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoCostoError
)


# ------------------------------------------------------------
# 2. FUNCIÓN GENERAL PARA EJECUTAR PRUEBAS
# ------------------------------------------------------------

def ejecutar_prueba(numero, descripcion, operacion, error_esperado=False):

    """
    Ejecuta una operación y comprueba su resultado.

    Parámetros:
    - numero: número de la prueba.
    - descripcion: descripción de la operación.
    - operacion: función que contiene la prueba.
    - error_esperado: indica si esperamos una excepción.

    Retorna:
    - True si el resultado coincide con lo esperado.
    - False si ocurre un resultado inesperado.
    """

    print("\n" + "=" * 60)
    print(f"PRUEBA {numero}: {descripcion}")
    print("=" * 60)

    try:

        # Ejecutamos la función de prueba.
        resultado = operacion()

    except (
        DatosInvalidosError,
        ServicioNoDisponibleError,
        ReservaInvalidaError,
        OperacionNoPermitidaError,
        CalculoCostoError
    ) as error:

        # Mostramos el error capturado.
        print(f"ERROR CONTROLADO: {error}")

        # Mostramos la causa original cuando existe
        # encadenamiento mediante raise ... from ...
        if error.__cause__ is not None:
            print(f"CAUSA ORIGINAL: {error.__cause__}")

        # Si el error era esperado, la prueba es correcta.
        if error_esperado:
            print("RESULTADO: PRUEBA CORRECTA")
            return True

        # Si no esperábamos un error, la prueba falla.
        print("RESULTADO: PRUEBA FALLIDA")
        return False

    except Exception as error:

        # Detectamos cualquier error inesperado.
        # Esta captura se utiliza únicamente para
        # evitar que se interrumpa el conjunto de pruebas.
        print(
            f"ERROR INESPERADO: "
            f"{type(error).__name__}: {error}"
        )

        print("RESULTADO: PRUEBA FALLIDA")
        return False

    else:

        # Si esperábamos un error y no ocurrió,
        # la prueba no cumple el resultado esperado.
        if error_esperado:
            print("ERROR: Se esperaba una excepción.")
            print("RESULTADO: PRUEBA FALLIDA")
            return False

        # Mostramos el resultado de la operación.
        if resultado is not None:
            print(f"Resultado: {resultado}")

        print("RESULTADO: PRUEBA CORRECTA")
        return True

    finally:

        # Este bloque se ejecuta siempre.
        print("Prueba finalizada.")


# ------------------------------------------------------------
# 3. PREPARACIÓN DE LOS DATOS DE PRUEBA
# ------------------------------------------------------------

# Creamos un cliente válido.
cliente = Cliente(
    1,
    "Carlos Pérez",
    "carlos@gmail.com",
    "3001234567"
)

# Creamos un servicio de reserva de salas.
sala = ServicioSala(
    101,
    "Sala de conferencias",
    50000,
    20
)

# Creamos un servicio de alquiler de equipos.
equipo = AlquilerEquipo(
    102,
    "Computador portátil",
    80000,
    "Portátil"
)

# Creamos una asesoría que no está disponible.
asesoria_no_disponible = AsesoriaEspecializada(
    103,
    "Asesoría en redes",
    70000,
    "Redes informáticas",
    disponible=False
)


# ------------------------------------------------------------
# 4. OPERACIONES DE PRUEBA
# ------------------------------------------------------------

# Diccionario que conserva las reservas creadas
# durante la ejecución de las pruebas.
reservas = {}


def prueba_1():

    # Creamos una reserva de sala por dos horas.
    reserva = Reserva(
        201,
        cliente,
        sala,
        2
    )

    # Guardamos la reserva para utilizarla después.
    reservas[201] = reserva

    # Comprobamos que el estado inicial sea pendiente.
    assert reserva.estado == "PENDIENTE"

    return reserva.mostrar_informacion()


def prueba_2():

    # Confirmamos la reserva creada en la prueba 1.
    reserva = reservas[201]

    reserva.confirmar()

    # Verificamos el cambio de estado.
    assert reserva.estado == "CONFIRMADA"

    return reserva.mostrar_informacion()


def prueba_3():

    # Procesamos la reserva confirmada.
    reserva = reservas[201]

    # Aplicamos 10% de descuento y 19% de impuesto.
    total = reserva.procesar(
        descuento=10,
        impuesto=19
    )

    # El costo esperado es 107100.
    assert total == 107100.0
    assert reserva.estado == "PROCESADA"

    return reserva.mostrar_informacion()


def prueba_4():

    # Creamos una reserva de alquiler por tres días.
    reserva = Reserva(
        202,
        cliente,
        equipo,
        3
    )

    reservas[202] = reserva

    # Cancelamos la reserva mientras está pendiente.
    reserva.cancelar()

    assert reserva.estado == "CANCELADA"

    return reserva.mostrar_informacion()


def prueba_5():

    # Intentamos crear una reserva con duración cero.
    # Debe producir ReservaInvalidaError.
    Reserva(
        203,
        cliente,
        sala,
        0
    )


def prueba_6():

    # Intentamos reservar una asesoría no disponible.
    # Debe producir ReservaInvalidaError.
    Reserva(
        204,
        cliente,
        asesoria_no_disponible,
        2
    )


def prueba_7():

    # Intentamos confirmar la reserva cancelada.
    # Debe producir OperacionNoPermitidaError.
    reservas[202].confirmar()


def prueba_8():

    # Creamos una nueva reserva de alquiler.
    reserva = Reserva(
        205,
        cliente,
        equipo,
        2
    )

    reservas[205] = reserva

    # Intentamos procesarla sin confirmar.
    # Debe producir ReservaInvalidaError.
    reserva.procesar()


def prueba_9():

    # Confirmamos la reserva creada en la prueba 8.
    reserva = reservas[205]

    reserva.confirmar()

    # Intentamos aplicar un descuento inválido.
    # Debe producir ReservaInvalidaError.
    reserva.procesar(descuento=150)


def prueba_10():

    # Después del error anterior, la reserva
    # debe continuar en estado CONFIRMADA.
    reserva = reservas[205]

    assert reserva.estado == "CONFIRMADA"

    # Procesamos nuevamente con valores correctos.
    total = reserva.procesar(
        descuento=0,
        impuesto=0
    )

    # Dos días a 80000 por día.
    assert total == 160000.0
    assert reserva.estado == "PROCESADA"

    return reserva.mostrar_informacion()


# ------------------------------------------------------------
# 5. EJECUCIÓN DE LAS DIEZ PRUEBAS
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print(" SOFTWARE FJ - PRUEBAS DEL MÓDULO DE RESERVAS")
    print("=" * 60)

    # Cada registro contiene:
    # número, descripción, función y error esperado.
    pruebas = [
        (1, "Crear reserva válida", prueba_1, False),
        (2, "Confirmar reserva", prueba_2, False),
        (3, "Procesar reserva", prueba_3, False),
        (4, "Cancelar reserva", prueba_4, False),
        (5, "Duración igual a cero", prueba_5, True),
        (6, "Servicio no disponible", prueba_6, True),
        (7, "Confirmar reserva cancelada", prueba_7, True),
        (8, "Procesar sin confirmar", prueba_8, True),
        (9, "Descuento incorrecto", prueba_9, True),
        (10, "Procesar después de un error", prueba_10, False)
    ]

    # Contador de pruebas correctas.
    correctas = 0

    # Ejecutamos las operaciones en el orden definido.
    for numero, descripcion, operacion, error_esperado in pruebas:

        resultado = ejecutar_prueba(
            numero,
            descripcion,
            operacion,
            error_esperado
        )

        if resultado:
            correctas += 1

    # --------------------------------------------------------
    # 6. RESUMEN FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print(" RESUMEN DE PRUEBAS")
    print("=" * 60)

    print(f"Pruebas ejecutadas: {len(pruebas)}")
    print(f"Pruebas correctas: {correctas}")
    print(f"Pruebas fallidas: {len(pruebas) - correctas}")

    print("=" * 60)


# ------------------------------------------------------------
# 7. PUNTO DE ENTRADA DEL PROGRAMA
# ------------------------------------------------------------

# Evitamos ejecutar automáticamente las pruebas
# cuando otro módulo importe este archivo.
if __name__ == "__main__":
    main()

# ============================================================
# FIN DEL ARCHIVO prueba_reservas.py
# ============================================================