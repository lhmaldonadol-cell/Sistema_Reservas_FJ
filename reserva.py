
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: reserva.py
#
# DESCRIPCIÓN:
# Este archivo contiene la clase Reserva.
#
# Permite:
# - Asociar clientes con servicios.
# - Validar los datos de una reserva.
# - Confirmar y cancelar reservas.
# - Procesar reservas y calcular sus costos.
# - Controlar operaciones incorrectas.
# - Registrar eventos y errores en un archivo de logs.
#
# CONCEPTOS IMPLEMENTADOS:
# - Programación orientada a objetos.
# - Encapsulación.
# - Composición entre objetos.
# - Excepciones personalizadas.
# - Encadenamiento de excepciones.
# - Manejo try/except/else/finally.
# - Parámetros opcionales.
#
# NOTA:
# Las reglas de estados corresponden a una propuesta
# de implementación para el proyecto académico.
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS Y CLASES
# ------------------------------------------------------------

# Permite registrar eventos y errores del sistema.
import logging

# Permite crear una ruta independiente de la carpeta
# desde la cual se ejecute el programa.
from pathlib import Path

# Importamos las clases que utilizaremos para validar
# los objetos recibidos por cada reserva.
from cliente import Cliente
from servicio import Servicio

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoCostoError
)


# ------------------------------------------------------------
# 2. CONFIGURACIÓN DEL REGISTRO DE EVENTOS
# ------------------------------------------------------------

# Ubicamos el archivo de logs en la carpeta del proyecto.
RUTA_LOG = Path(__file__).resolve().parent / "sistema.log"

# Creamos un registrador específico para las reservas.
# Esto evita depender de la configuración de main.py.
registrador = logging.getLogger("software_fj.reservas")

# Indicamos que registraremos eventos informativos,
# advertencias y errores.
registrador.setLevel(logging.INFO)

# Evitamos que los mensajes se dupliquen en otros
# registradores configurados por la aplicación.
registrador.propagate = False

# Comprobamos si ya existe un manejador para el archivo.
# Así evitamos registrar varias veces el mismo evento.
if not registrador.handlers:

    # El manejador escribe los mensajes en sistema.log.
    manejador = logging.FileHandler(
        RUTA_LOG,
        encoding="utf-8"
    )

    # Definimos el formato de cada registro.
    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    manejador.setFormatter(formato)

    # Asociamos el manejador al registrador.
    registrador.addHandler(manejador)


# ------------------------------------------------------------
# 3. DEFINICIÓN DE LA CLASE RESERVA
# ------------------------------------------------------------

class Reserva:

    """
    Representa una reserva realizada por un cliente.

    Atributos:
    - identificador: código único de la reserva.
    - cliente: objeto de la clase Cliente.
    - servicio: objeto de una clase derivada de Servicio.
    - duracion: horas o días, según el servicio.
    - estado: situación actual de la reserva.
    - costo_total: costo calculado al procesarla.

    Estados:
    - PENDIENTE
    - CONFIRMADA
    - PROCESADA
    - CANCELADA
    """

    # --------------------------------------------------------
    # 3.1. CONSTRUCTOR DE LA CLASE
    # --------------------------------------------------------

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion
    ):

        try:

            # Validamos que el identificador sea
            # un número entero positivo.
            if (
                type(identificador) is not int
                or identificador <= 0
            ):
                raise DatosInvalidosError(
                    "El identificador de la reserva "
                    "debe ser un entero positivo."
                )

            # Comprobamos que el cliente sea un objeto
            # creado mediante la clase Cliente.
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError(
                    "La reserva debe tener un cliente válido."
                )

            # Comprobamos que el servicio sea un objeto
            # perteneciente a una clase derivada de Servicio.
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError(
                    "La reserva debe tener un servicio válido."
                )

            # Utilizamos el método del servicio para validar
            # la duración y su disponibilidad.
            #
            # Cada servicio aplica sus propias reglas:
            # - Salas: máximo 12 horas.
            # - Equipos: máximo 30 días.
            # - Asesorías: máximo 8 horas.
            servicio.validar_parametros(duracion)

        except (
            DatosInvalidosError,
            ServicioNoDisponibleError
        ) as error:

            # Registramos el error antes de propagarlo.
            registrador.error(
                "Error al crear reserva %s: %s",
                identificador,
                error
            )

            # Convertimos el error de validación
            # en una excepción propia de las reservas.
            #
            # 'from error' conserva la causa original
            # para facilitar el diagnóstico.
            raise ReservaInvalidaError(
                f"No fue posible crear la reserva: {error}"
            ) from error

        else:

            # Guardamos los datos como atributos privados.
            self.__identificador = identificador
            self.__cliente = cliente
            self.__servicio = servicio
            self.__duracion = duracion

            # Toda reserva comienza en estado pendiente.
            self.__estado = "PENDIENTE"

            # El costo se calculará al procesar la reserva.
            self.__costo_total = None

            # Registramos la creación exitosa.
            registrador.info(
                "Reserva %s creada para cliente %s "
                "y servicio %s.",
                identificador,
                cliente.identificador,
                servicio.identificador
            )

        finally:

            # Este bloque se ejecuta tanto si la reserva
            # se creó correctamente como si ocurrió un error.
            registrador.info(
                "Finalizado intento de creación "
                "de reserva %s.",
                identificador
            )

    # --------------------------------------------------------
    # 3.2. PROPIEDADES DE CONSULTA
    # --------------------------------------------------------

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # --------------------------------------------------------
    # 3.3. CONFIRMAR RESERVA
    # --------------------------------------------------------

    def confirmar(self):

        """
        Cambia el estado de PENDIENTE a CONFIRMADA.

        No permite confirmar reservas canceladas,
        procesadas o previamente confirmadas.
        """

        try:

            # Solo se pueden confirmar reservas pendientes.
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    "Solo se pueden confirmar "
                    "reservas pendientes."
                )

            # Verificamos nuevamente la disponibilidad.
            self.__servicio.validar_parametros(
                self.__duracion
            )

            # Actualizamos el estado de la reserva.
            self.__estado = "CONFIRMADA"

        except (
            OperacionNoPermitidaError,
            DatosInvalidosError,
            ServicioNoDisponibleError
        ) as error:

            # Guardamos el error en el archivo de logs.
            registrador.error(
                "Error al confirmar reserva %s: %s",
                self.__identificador,
                error
            )

            # Propagamos el error para que el programa
            # principal pueda capturarlo.
            raise

        else:

            # Registramos la confirmación exitosa.
            registrador.info(
                "Reserva %s confirmada.",
                self.__identificador
            )

            return self.__estado

    # --------------------------------------------------------
    # 3.4. CANCELAR RESERVA
    # --------------------------------------------------------

    def cancelar(self):

        """
        Permite cancelar reservas pendientes o confirmadas.

        No permite cancelar reservas que ya fueron
        procesadas o canceladas anteriormente.
        """

        try:

            # Comprobamos si la operación está permitida.
            if self.__estado not in (
                "PENDIENTE",
                "CONFIRMADA"
            ):
                raise OperacionNoPermitidaError(
                    "No se puede cancelar una reserva "
                    "procesada o previamente cancelada."
                )

            # Actualizamos el estado.
            self.__estado = "CANCELADA"

        except OperacionNoPermitidaError as error:

            # Registramos la operación incorrecta.
            registrador.error(
                "Error al cancelar reserva %s: %s",
                self.__identificador,
                error
            )

            raise

        else:

            # Registramos la cancelación exitosa.
            registrador.info(
                "Reserva %s cancelada.",
                self.__identificador
            )

            return self.__estado

    # --------------------------------------------------------
    # 3.5. PROCESAR RESERVA
    # --------------------------------------------------------

    def procesar(
        self,
        descuento=0,
        impuesto=0
    ):

        """
        Calcula el costo final y procesa una reserva.

        Parámetros opcionales:
        - descuento: porcentaje de descuento.
        - impuesto: porcentaje de impuesto.

        Una reserva debe estar confirmada antes
        de ser procesada.

        Si el cálculo es exitoso, el estado cambia
        a PROCESADA.
        """

        try:

            # Solo pueden procesarse reservas confirmadas.
            if self.__estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    "La reserva debe estar confirmada "
                    "antes de ser procesada."
                )

            # Calculamos el costo mediante el servicio.
            #
            # Se aplica polimorfismo porque cada tipo
            # de servicio implementa calcular_costo()
            # de manera especializada.
            total = self.__servicio.calcular_costo(
                self.__duracion,
                descuento=descuento,
                impuesto=impuesto
            )

        except (
            OperacionNoPermitidaError,
            DatosInvalidosError,
            ServicioNoDisponibleError,
            CalculoCostoError
        ) as error:

            # Registramos el error ocurrido.
            registrador.error(
                "Error al procesar reserva %s: %s",
                self.__identificador,
                error
            )

            # Conservamos la causa del error.
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva: {error}"
            ) from error

        else:

            # Solo actualizamos el estado si el cálculo
            # terminó correctamente.
            self.__costo_total = total
            self.__estado = "PROCESADA"

            # Registramos el procesamiento exitoso.
            registrador.info(
                "Reserva %s procesada. Costo: %.2f",
                self.__identificador,
                total
            )

            return total

        finally:

            # Registramos que finalizó el intento
            # de procesamiento, exitoso o fallido.
            registrador.info(
                "Finalizado procesamiento de reserva %s.",
                self.__identificador
            )

    # --------------------------------------------------------
    # 3.6. MOSTRAR INFORMACIÓN DE LA RESERVA
    # --------------------------------------------------------

    def mostrar_informacion(self):

        """
        Devuelve un resumen de los datos de la reserva.
        """

        # Mostramos un texto si todavía no existe costo.
        if self.__costo_total is None:
            costo = "Sin calcular"
        else:
            costo = f"${self.__costo_total:,.2f}"

        return (
            f"Reserva: {self.__identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} | "
            f"Estado: {self.__estado} | "
            f"Costo: {costo}"
        )


# ============================================================
# FIN DEL ARCHIVO reserva.py
# ============================================================
