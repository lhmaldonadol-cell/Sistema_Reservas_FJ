
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: prueba_servicios.py
#
# DESCRIPCIÓN:
# Este archivo comprueba el funcionamiento de los servicios.
#
# Se realizan pruebas de:
# - Reserva de salas.
# - Alquiler de equipos.
# - Asesorías especializadas.
# - Cálculo de descuentos e impuestos.
# - Validación de datos incorrectos.
# - Disponibilidad de los servicios.
# - Continuidad del programa después de errores.
#
# Las tarifas son valores simulados para el ejercicio.
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTACIÓN DE CLASES Y EXCEPCIONES
# ------------------------------------------------------------

# Importamos las tres clases especializadas de servicios.
from servicio import (
    ServicioSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

# Importamos las excepciones que queremos controlar.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoCostoError
)


# ------------------------------------------------------------
# 2. FUNCIÓN PARA EJECUTAR UNA PRUEBA
# ------------------------------------------------------------

def ejecutar_prueba(numero, descripcion, operacion):

    """
    Ejecuta una operación de prueba de manera controlada.

    Parámetros:
    - numero: identificador de la prueba.
    - descripcion: explicación de lo que se evaluará.
    - operacion: función que contiene la operación.

    Si ocurre una excepción conocida, se muestra el error
    y el programa continúa con la siguiente prueba.
    """

    print("\n" + "=" * 55)
    print(f"PRUEBA {numero}: {descripcion}")
    print("=" * 55)

    try:

        # Ejecutamos la operación recibida.
        resultado = operacion()

    except (
        DatosInvalidosError,
        ServicioNoDisponibleError,
        CalculoCostoError
    ) as error:

        # Mostramos el error sin detener las demás pruebas.
        print(f"ERROR CONTROLADO: {error}")

    else:

        # Este bloque se ejecuta si no hubo excepciones.
        print("OPERACIÓN EXITOSA")

        # Mostramos el resultado si la operación lo devuelve.
        if resultado is not None:
            print(f"Resultado: {resultado}")

    finally:

        # Este mensaje aparece independientemente del resultado.
        print("Prueba finalizada.")


# ------------------------------------------------------------
# 3. CREACIÓN DE SERVICIOS PARA LAS PRUEBAS
# ------------------------------------------------------------

# Creamos una sala con capacidad para 20 personas.
# Tarifa propuesta: $50000 por hora.
sala = ServicioSala(
    101,
    "Sala de conferencias",
    50000,
    20
)

# Creamos un servicio de alquiler de computadores.
# Tarifa propuesta: $80000 por día.
equipo = AlquilerEquipo(
    102,
    "Computador portátil",
    80000,
    "Portátil"
)

# Creamos un servicio de asesoría en programación.
# Tarifa propuesta: $60000 por hora.
asesoria = AsesoriaEspecializada(
    103,
    "Asesoría en Python",
    60000,
    "Programación"
)


# ------------------------------------------------------------
# 4. DEFINICIÓN DE LAS OPERACIONES DE PRUEBA
# ------------------------------------------------------------

def prueba_1():

    # Calculamos una reserva de sala por dos horas.
    print(sala.mostrar_descripcion())
    return sala.calcular_costo(2)


def prueba_2():

    # Calculamos el alquiler de un equipo por tres días.
    print(equipo.mostrar_descripcion())
    return equipo.calcular_costo(3)


def prueba_3():

    # Calculamos una asesoría de dos horas.
    print(asesoria.mostrar_descripcion())
    return asesoria.calcular_costo(2)


def prueba_4():

    # Aplicamos 10% de descuento y 19% de impuesto.
    # El impuesto se calcula después del descuento.
    return sala.calcular_costo(
        2,
        descuento=10,
        impuesto=19
    )


def prueba_5():

    # Intentamos reservar una sala por cero horas.
    # Debe generar una excepción de datos inválidos.
    return sala.calcular_costo(0)


def prueba_6():

    # Intentamos alquilar un equipo durante 40 días.
    # El máximo propuesto para el alquiler es 30 días.
    return equipo.calcular_costo(40)


def prueba_7():

    # Creamos una asesoría no disponible.
    asesoria_no_disponible = AsesoriaEspecializada(
        104,
        "Asesoría en redes",
        70000,
        "Redes informáticas",
        disponible=False
    )

    # Intentamos calcular su costo.
    return asesoria_no_disponible.calcular_costo(2)


def prueba_8():

    # Intentamos aplicar un descuento del 150%.
    # El sistema debe rechazar el porcentaje.
    return sala.calcular_costo(
        2,
        descuento=150
    )


# ------------------------------------------------------------
# 5. EJECUCIÓN DE LAS OCHO PRUEBAS
# ------------------------------------------------------------

def main():

    print("=" * 55)
    print(" SOFTWARE FJ - PRUEBAS DEL MÓDULO DE SERVICIOS")
    print("=" * 55)

    # Agrupamos las operaciones en una lista.
    # Esto permite ejecutarlas de forma ordenada.
    pruebas = [
        (1, "Reserva de sala válida", prueba_1),
        (2, "Alquiler de equipo válido", prueba_2),
        (3, "Asesoría especializada válida", prueba_3),
        (4, "Descuento e impuesto", prueba_4),
        (5, "Duración igual a cero", prueba_5),
        (6, "Alquiler superior a 30 días", prueba_6),
        (7, "Servicio no disponible", prueba_7),
        (8, "Descuento fuera del rango", prueba_8)
    ]

    # Ejecutamos cada prueba sin detener el programa.
    for numero, descripcion, operacion in pruebas:

        ejecutar_prueba(
            numero,
            descripcion,
            operacion
        )

    print("\n" + "=" * 55)
    print(" TODAS LAS PRUEBAS FUERON EJECUTADAS")
    print("=" * 55)


# ------------------------------------------------------------
# 6. PUNTO DE ENTRADA
# ------------------------------------------------------------

# Ejecutamos las pruebas únicamente cuando este archivo
# se inicia directamente desde Python.
if __name__ == "__main__":
    main()


# ============================================================
# FIN DEL ARCHIVO prueba_servicios.py
# ============================================================
