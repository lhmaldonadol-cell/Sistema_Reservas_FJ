
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: main.py
#
# DESCRIPCIÓN:
# Programa principal que integra los módulos del sistema.
#
# FUNCIONES:
# 1. Registrar clientes.
# 2. Consultar clientes.
# 3. Consultar servicios.
# 4. Crear reservas.
# 5. Consultar reservas.
# 6. Confirmar reservas.
# 7. Cancelar reservas.
# 8. Procesar reservas.
# 9. Consultar eventos registrados.
#
# CONCEPTOS:
# - Programación orientada a objetos.
# - Herencia y polimorfismo.
# - Manejo avanzado de excepciones.
# - Validación de entradas.
# - Registro de eventos y errores.
# - Almacenamiento temporal en memoria.
#
# NOTA:
# Los datos se pierden al cerrar la aplicación.
# No se utiliza ninguna base de datos.
# ============================================================

import logging
from pathlib import Path

# Importamos las clases desarrolladas anteriormente.
from cliente import Cliente

from servicio import (
    ServicioSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from reserva import Reserva

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ClienteDuplicadoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoCostoError
)


# ------------------------------------------------------------
# 1. CONFIGURACIÓN DEL ARCHIVO DE EVENTOS
# ------------------------------------------------------------

# Ruta del archivo que almacena eventos y errores.
RUTA_LOG = Path(__file__).resolve().parent / "sistema.log"

# Configuramos un registrador para el programa principal.
logger = logging.getLogger("software_fj.main")
logger.setLevel(logging.INFO)
logger.propagate = False

# Evitamos agregar manejadores duplicados.
if not logger.handlers:

    manejador = logging.FileHandler(
        RUTA_LOG,
        encoding="utf-8"
    )

    manejador.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
    )

    logger.addHandler(manejador)


# ------------------------------------------------------------
# 2. CLASE PRINCIPAL DEL SISTEMA
# ------------------------------------------------------------

class SistemaReservas:

    """
    Administra los clientes, servicios y reservas.

    Utiliza diccionarios para almacenar temporalmente
    los objetos durante la ejecución del programa.
    """

    def __init__(self):

        # Diccionario de clientes:
        # clave = identificador del cliente.
        self.clientes = {}

        # Diccionario de servicios:
        # clave = identificador del servicio.
        self.servicios = {}

        # Diccionario de reservas:
        # clave = identificador de la reserva.
        self.reservas = {}

        # Registramos los servicios iniciales.
        self.cargar_servicios()

        logger.info("Sistema de reservas iniciado.")

    # --------------------------------------------------------
    # 2.1. SERVICIOS INICIALES
    # --------------------------------------------------------

    def cargar_servicios(self):

        """
        Crea los servicios de ejemplo de Software FJ.

        Las tarifas son valores simulados para el
        desarrollo de la actividad académica.
        """

        servicios_iniciales = [
            ServicioSala(
                101,
                "Sala de conferencias",
                50000,
                20
            ),

            AlquilerEquipo(
                102,
                "Computador portátil",
                80000,
                "Portátil"
            ),

            AsesoriaEspecializada(
                103,
                "Asesoría en Python",
                60000,
                "Programación"
            )
        ]

        # Registramos los objetos mediante su identificador.
        for servicio in servicios_iniciales:
            self.servicios[servicio.identificador] = servicio

        logger.info("Servicios iniciales cargados.")

    # --------------------------------------------------------
    # 2.2. REGISTRAR CLIENTE
    # --------------------------------------------------------

    def registrar_cliente(self):

        """
        Solicita los datos de un cliente, valida su
        identificador y crea el objeto correspondiente.
        """

        try:

            print("\n--- REGISTRAR CLIENTE ---")

            identificador = int(
                input("Identificador del cliente: ")
            )

            # No permitimos identificadores duplicados.
            if identificador in self.clientes:
                raise ClienteDuplicadoError(
                    "Ya existe un cliente con ese identificador."
                )

            nombre = input("Nombre completo: ")
            correo = input("Correo electrónico: ")
            telefono = input("Teléfono: ")

            # La clase Cliente realiza sus propias
            # validaciones de los datos recibidos.
            cliente = Cliente(
                identificador,
                nombre,
                correo,
                telefono
            )

            # Guardamos el objeto en memoria.
            self.clientes[identificador] = cliente

        except ValueError as error:

            print("ERROR: El identificador debe ser numérico.")
            logger.error("Error numérico al registrar cliente: %s", error)

        except (
            DatosInvalidosError,
            ClienteDuplicadoError
        ) as error:

            print(f"ERROR CONTROLADO: {error}")
            logger.error("Error al registrar cliente: %s", error)

        else:

            print("Cliente registrado correctamente.")

            logger.info(
                "Cliente %s registrado: %s",
                identificador,
                nombre
            )

        finally:

            print("Operación de registro finalizada.")

    # --------------------------------------------------------
    # 2.3. CONSULTAR CLIENTES
    # --------------------------------------------------------

    def consultar_clientes(self):

        print("\n--- CLIENTES REGISTRADOS ---")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for cliente in self.clientes.values():

            # Consultamos las propiedades del objeto.
            print(
                f"ID: {cliente.identificador} | "
                f"Nombre: {cliente.nombre} | "
                f"Correo: {cliente.correo} | "
                f"Teléfono: {cliente.telefono}"
            )

    # --------------------------------------------------------
    # 2.4. CONSULTAR SERVICIOS
    # --------------------------------------------------------

    def consultar_servicios(self):

        print("\n--- SERVICIOS DISPONIBLES ---")

        for servicio in self.servicios.values():

            # Polimorfismo:
            # cada servicio genera su propia descripción.
            print(servicio.mostrar_descripcion())

            # Mostramos también su identificador y estado.
            estado = (
                "DISPONIBLE"
                if servicio.disponible
                else "NO DISPONIBLE"
            )

            print(
                f"ID: {servicio.identificador} | "
                f"Estado: {estado}"
            )

            print("-" * 50)

    # --------------------------------------------------------
    # 2.5. CREAR RESERVA
    # --------------------------------------------------------

    def crear_reserva(self):

        """
        Relaciona un cliente existente con un servicio.

        Si los datos son válidos, crea una reserva
        en estado PENDIENTE.
        """

        try:

            print("\n--- CREAR RESERVA ---")

            identificador = int(
                input("Identificador de la reserva: ")
            )

            # Evitamos registrar dos reservas con el mismo ID.
            if identificador in self.reservas:
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese identificador."
                )

            id_cliente = int(
                input("Identificador del cliente: ")
            )

            id_servicio = int(
                input("Identificador del servicio: ")
            )

            duracion = int(
                input("Duración en horas o días: ")
            )

            # Buscamos el cliente en memoria.
            cliente = self.clientes.get(id_cliente)

            if cliente is None:
                raise ReservaInvalidaError(
                    "El cliente indicado no está registrado."
                )

            # Buscamos el servicio solicitado.
            servicio = self.servicios.get(id_servicio)

            if servicio is None:
                raise ReservaInvalidaError(
                    "El servicio indicado no existe."
                )

            # Creamos la reserva.
            # Su constructor valida disponibilidad y duración.
            reserva = Reserva(
                identificador,
                cliente,
                servicio,
                duracion
            )

            # Almacenamos la reserva.
            self.reservas[identificador] = reserva

        except ValueError as error:

            print("ERROR: Debes ingresar valores numéricos.")
            logger.error("Error numérico al crear reserva: %s", error)

        except (
            ReservaInvalidaError,
            DatosInvalidosError,
            ServicioNoDisponibleError
        ) as error:

            print(f"ERROR CONTROLADO: {error}")
            logger.error("Error al crear reserva: %s", error)

        else:

            print("Reserva creada correctamente.")
            print(reserva.mostrar_informacion())

            logger.info(
                "Reserva %s creada desde el menú principal.",
                identificador
            )

        finally:

            print("Operación de creación finalizada.")

    # --------------------------------------------------------
    # 2.6. CONSULTAR RESERVAS
    # --------------------------------------------------------

    def consultar_reservas(self):

        print("\n--- RESERVAS REGISTRADAS ---")

        if not self.reservas:
            print("No hay reservas registradas.")
            return

        for reserva in self.reservas.values():

            print(reserva.mostrar_informacion())
            print("-" * 50)

    # --------------------------------------------------------
    # 2.7. BUSCAR UNA RESERVA
    # --------------------------------------------------------

    def buscar_reserva(self):

        """
        Solicita un identificador y devuelve la reserva.

        Este método centraliza la búsqueda para evitar
        repetir código en varias operaciones.
        """

        identificador = int(
            input("Identificador de la reserva: ")
        )

        reserva = self.reservas.get(identificador)

        if reserva is None:
            raise ReservaInvalidaError(
                "No existe una reserva con ese identificador."
            )

        return reserva

    # --------------------------------------------------------
    # 2.8. CONFIRMAR RESERVA
    # --------------------------------------------------------

    def confirmar_reserva(self):

        try:

            print("\n--- CONFIRMAR RESERVA ---")

            reserva = self.buscar_reserva()

            # La clase Reserva valida el estado actual.
            reserva.confirmar()

        except (
            ValueError,
            ReservaInvalidaError,
            OperacionNoPermitidaError,
            ServicioNoDisponibleError,
            DatosInvalidosError
        ) as error:

            print(f"ERROR CONTROLADO: {error}")
            logger.error("Error al confirmar reserva: %s", error)

        else:

            print("Reserva confirmada correctamente.")
            print(reserva.mostrar_informacion())

    # --------------------------------------------------------
    # 2.9. CANCELAR RESERVA
    # --------------------------------------------------------

    def cancelar_reserva(self):

        try:

            print("\n--- CANCELAR RESERVA ---")

            reserva = self.buscar_reserva()

            # Cancelamos la reserva si su estado lo permite.
            reserva.cancelar()

        except (
            ValueError,
            ReservaInvalidaError,
            OperacionNoPermitidaError
        ) as error:

            print(f"ERROR CONTROLADO: {error}")
            logger.error("Error al cancelar reserva: %s", error)

        else:

            print("Reserva cancelada correctamente.")
            print(reserva.mostrar_informacion())

    # --------------------------------------------------------
    # 2.10. PROCESAR RESERVA
    # --------------------------------------------------------

    def procesar_reserva(self):

        try:

            print("\n--- PROCESAR RESERVA ---")

            reserva = self.buscar_reserva()

            # Los porcentajes son opcionales.
            # Si se deja el campo vacío, utilizamos cero.
            texto_descuento = input(
                "Descuento (%), Enter para 0: "
            ).strip()

            texto_impuesto = input(
                "Impuesto (%), Enter para 0: "
            ).strip()

            descuento = (
                float(texto_descuento)
                if texto_descuento
                else 0
            )

            impuesto = (
                float(texto_impuesto)
                if texto_impuesto
                else 0
            )

            # Procesamos la reserva mediante su método.
            total = reserva.procesar(
                descuento=descuento,
                impuesto=impuesto
            )

        except (
            ValueError,
            ReservaInvalidaError,
            OperacionNoPermitidaError,
            DatosInvalidosError,
            ServicioNoDisponibleError,
            CalculoCostoError
        ) as error:

            print(f"ERROR CONTROLADO: {error}")
            logger.error("Error al procesar reserva: %s", error)

        else:

            print("Reserva procesada correctamente.")
            print(f"Costo total: ${total:,.2f}")
            print(reserva.mostrar_informacion())

    # --------------------------------------------------------
    # 2.11. CONSULTAR HISTORIAL DE EVENTOS
    # --------------------------------------------------------

    def consultar_historial(self):

        """
        Muestra los últimos 20 registros del archivo log.

        El archivo se utiliza únicamente para registrar
        eventos y errores, no para almacenar los clientes
        o las reservas del sistema.
        """

        print("\n--- HISTORIAL DE EVENTOS ---")

        try:

            # Abrimos el archivo con codificación UTF-8.
            with open(RUTA_LOG, "r", encoding="utf-8") as archivo:

                # Leemos los registros existentes.
                lineas = archivo.readlines()

            if not lineas:
                print("No hay eventos registrados.")
                return

            # Mostramos los últimos 20 registros.
            for linea in lineas[-20:]:
                print(linea.rstrip())

        except OSError as error:

            print(f"No fue posible leer el historial: {error}")
            logger.error("Error al consultar historial: %s", error)

    # --------------------------------------------------------
    # 2.12. MOSTRAR MENÚ
    # --------------------------------------------------------

    def mostrar_menu(self):

        print("\n" + "=" * 55)
        print(" SOFTWARE FJ - SISTEMA DE GESTIÓN")
        print("=" * 55)

        print("1. Registrar cliente")
        print("2. Consultar clientes")
        print("3. Consultar servicios")
        print("4. Crear reserva")
        print("5. Consultar reservas")
        print("6. Confirmar reserva")
        print("7. Cancelar reserva")
        print("8. Procesar reserva")
        print("9. Consultar historial de eventos")
        print("0. Salir")

        print("=" * 55)

    # --------------------------------------------------------
    # 2.13. EJECUTAR EL SISTEMA
    # --------------------------------------------------------

    def ejecutar(self):

        """
        Mantiene el menú activo hasta que el usuario
        seleccione la opción de salir.

        Los errores de entrada no deben detener
        la ejecución del programa.
        """

        # Asociamos cada opción con su método.
        operaciones = {
            "1": self.registrar_cliente,
            "2": self.consultar_clientes,
            "3": self.consultar_servicios,
            "4": self.crear_reserva,
            "5": self.consultar_reservas,
            "6": self.confirmar_reserva,
            "7": self.cancelar_reserva,
            "8": self.procesar_reserva,
            "9": self.consultar_historial
        }

        while True:

            self.mostrar_menu()

            try:

                opcion = input(
                    "Seleccione una opción: "
                ).strip()

                # La opción cero finaliza el programa.
                if opcion == "0":

                    logger.info("Sistema cerrado por el usuario.")

                    print("\nGracias por utilizar Software FJ.")
                    break

                # Buscamos la función correspondiente.
                operacion = operaciones.get(opcion)

                if operacion is None:
                    print("Opción inválida. Intente nuevamente.")
                    logger.warning(
                        "Opción de menú no válida: %s",
                        opcion
                    )
                    continue

                # Ejecutamos la operación seleccionada.
                operacion()

            except (KeyboardInterrupt, EOFError):

                # Permite finalizar limpiamente si se
                # interrumpe la entrada de la terminal.
                print("\nEjecución interrumpida.")

                logger.warning(
                    "Programa interrumpido desde la terminal."
                )

                break

            except Exception:

                # Captura de seguridad para errores no
                # previstos por los métodos del menú.
                # Conservamos el traceback en sistema.log.
                print(
                    "Ocurrió un error inesperado. "
                    "Consulta el archivo sistema.log."
                )

                logger.exception(
                    "Error inesperado en el menú principal."
                )

                # El ciclo continúa en lugar de cerrar
                # completamente la aplicación.


# ------------------------------------------------------------
# 3. PUNTO DE ENTRADA DEL PROGRAMA
# ------------------------------------------------------------

def main():

    """
    Crea una instancia del sistema e inicia su menú.
    """

    try:

        sistema = SistemaReservas()
        sistema.ejecutar()

    except Exception:

        # Registramos cualquier fallo grave de inicio.
        logger.exception(
            "No fue posible iniciar el sistema."
        )

        print(
            "No fue posible iniciar el sistema. "
            "Consulta sistema.log."
        )


# El menú se ejecuta únicamente cuando iniciamos main.py.
if __name__ == "__main__":
    main()


# ============================================================
# FIN DEL ARCHIVO main.py
# ============================================================
