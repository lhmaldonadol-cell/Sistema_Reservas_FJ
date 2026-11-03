
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: excepciones.py
#
# DESCRIPCIÓN:
# Este archivo contiene las excepciones personalizadas
# utilizadas para controlar los errores del sistema.
#
# Las excepciones permiten identificar situaciones
# incorrectas durante el registro de clientes,
# la creación de servicios y la gestión de reservas.
#
# Su implementación contribuye a mantener el programa
# organizado, estable y fácil de mantener.
# ============================================================


# ------------------------------------------------------------
# 1. EXCEPCIÓN PARA DATOS INVÁLIDOS
# ------------------------------------------------------------

class DatosInvalidosError(Exception):

    """
    Se utiliza cuando los datos ingresados no cumplen
    las condiciones de validación establecidas.

    Ejemplos:
    - Nombre vacío.
    - Correo electrónico incorrecto.
    - Número de teléfono inválido.
    - Identificador incorrecto.
    """

    pass


# ------------------------------------------------------------
# 2. EXCEPCIÓN PARA CLIENTES DUPLICADOS
# ------------------------------------------------------------

class ClienteDuplicadoError(Exception):

    """
    Se utiliza cuando se intenta registrar un cliente
    cuyo identificador ya existe en el sistema.

    Permite evitar registros duplicados.
    """

    pass


# ------------------------------------------------------------
# 3. EXCEPCIÓN PARA SERVICIOS NO DISPONIBLES
# ------------------------------------------------------------

class ServicioNoDisponibleError(Exception):

    """
    Se utiliza cuando un cliente intenta reservar
    un servicio que no se encuentra disponible.

    Ejemplo:
    Intentar reservar una sala que ya está ocupada.
    """

    pass

# ------------------------------------------------------------
# 4. EXCEPCIÓN PARA RESERVAS INVÁLIDAS
# ------------------------------------------------------------

class ReservaInvalidaError(Exception):

    """
    Se utiliza cuando una reserva no cumple
    las condiciones necesarias para ser procesada.

    Ejemplos:
    - Duración igual a cero.
    - Duración negativa.
    - Cliente inexistente.
    - Servicio incorrecto.
    """
    pass

# ------------------------------------------------------------
# 5. EXCEPCIÓN PARA OPERACIONES NO PERMITIDAS
# ------------------------------------------------------------

class OperacionNoPermitidaError(Exception):

    """
    Se utiliza cuando se intenta realizar
    una operación que no está permitida.

    Ejemplos:
    - Cancelar una reserva que ya fue cancelada.
    - Confirmar una reserva que no puede confirmarse.
    """
    pass

# ------------------------------------------------------------
# 6. EXCEPCIÓN PARA ERRORES EN EL CÁLCULO DE COSTOS
# ------------------------------------------------------------

class CalculoCostoError(Exception):

    """
    Se utiliza cuando ocurre un problema durante
    el cálculo del costo de un servicio.

    Ejemplos:
    - Tarifa negativa.
    - Descuento fuera del rango permitido.
    - Impuesto incorrecto.
    """

    pass

# ============================================================
# FIN DEL ARCHIVO excepciones.py
# ============================================================