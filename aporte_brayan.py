
# ============================================================
# APORTE COLABORATIVO - FASE 4 PROGRAMACIÓN
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Proyecto: Software FJ
#
# Aporte original: Brayan Salazar
# Correcciones e integración: Equipo de trabajo
#
# Funcionalidades:
# - Manejo avanzado de excepciones.
# - Herencia y polimorfismo.
# - Validación de cantidades y disponibilidad.
# - Diez operaciones de prueba.
# - Registro de errores en archivo de texto.
# - Uso de try, except, else y finally.
# - Encadenamiento de excepciones.
# - Cálculo de costos con argumentos variables.
# ============================================================

import datetime


# ============================================================
# 1. EXCEPCIONES PERSONALIZADAS
# ============================================================

# Excepción general para errores relacionados con reservas.
class ReservaError(Exception):
    pass


# Excepción para clientes que no existen en el sistema.
class ClienteNoEncontradoError(ReservaError):
    pass


# Excepción para servicios que no están disponibles.
class ServicioNoDisponibleError(ReservaError):
    pass


# Excepción para cantidades inválidas.
class CantidadInvalidaError(ReservaError):
    pass


# Excepción para reservas que superan los cupos disponibles.
class CupoInsuficienteError(ReservaError):
    pass


# ============================================================
# 2. REGISTRO DE EVENTOS Y ERRORES
# ============================================================

def guardar_log(mensaje):
    """
    Guarda un mensaje en el archivo logs.txt.

    Cada registro incluye la fecha y hora de la operación.
    El archivo se crea automáticamente si no existe.
    """

    # Abrir el archivo en modo de escritura acumulativa.
    with open("logs.txt", "a", encoding="utf-8") as archivo:

        # Obtener la fecha y hora actuales.
        fecha_hora = datetime.datetime.now()

        # Guardar el mensaje con su fecha y hora.
        archivo.write(f"{fecha_hora} - {mensaje}\n")


# ============================================================
# 3. CLASE BASE SERVICIO
# ============================================================

class Servicio:
    """
    Clase base para representar los servicios de Software FJ.
    """

    def __init__(self, nombre, precio, cupo):

        # Validar el precio del servicio.
        if precio < 0:
            raise ReservaError(
                "El precio del servicio no puede ser negativo"
            )

        # Validar la disponibilidad inicial.
        if not isinstance(cupo, int) or isinstance(cupo, bool) or cupo < 0:
            raise CantidadInvalidaError(
                "Los cupos iniciales deben ser enteros no negativos"
            )

        # Guardar los datos del servicio.
        self.nombre = nombre
        self.precio = precio
        self.cupo = cupo

    def validar_cantidad(self, cantidad):
        """
        Comprueba que la cantidad solicitada sea válida
        y que exista disponibilidad suficiente.
        """

        # Impedir cantidades negativas, cero o no enteras.
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise CantidadInvalidaError(
                "La cantidad solicitada debe ser un entero mayor que cero"
            )

        # Comprobar si el servicio está agotado.
        if self.cupo == 0:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no tiene disponibilidad"
            )

        # Evitar reservas superiores a los cupos disponibles.
        if cantidad > self.cupo:
            raise CupoInsuficienteError(
                f"Servicio {self.nombre}: "
                f"solo hay {self.cupo} cupos disponibles"
            )

    def reservar(self, cantidad):
        """
        Método que deben implementar las clases especializadas.
        """

        raise NotImplementedError(
            "Cada servicio debe implementar su método reservar"
        )


# ============================================================
# 4. SERVICIO DE RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    def reservar(self, cantidad):

        # Validar cantidad y disponibilidad.
        self.validar_cantidad(cantidad)

        # Descontar los cupos utilizados.
        self.cupo -= cantidad

        # Retornar la confirmación.
        return (
            f"Sala {self.nombre} reservada "
            f"para {cantidad} cupo(s)"
        )


# ============================================================
# 5. SERVICIO DE ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipo(Servicio):

    def reservar(self, cantidad):

        # Verificar que la cantidad sea válida.
        self.validar_cantidad(cantidad)

        # Descontar los equipos alquilados.
        self.cupo -= cantidad

        # Confirmar el alquiler.
        return (
            f"Equipo {self.nombre} alquilado "
            f"x{cantidad}"
        )


# ============================================================
# 6. SERVICIO DE ASESORÍAS ESPECIALIZADAS
# ============================================================

class AsesoriaEspecializada(Servicio):

    def reservar(self, cantidad):

        # Verificar la cantidad y los cupos disponibles.
        self.validar_cantidad(cantidad)

        # Descontar los cupos reservados.
        self.cupo -= cantidad

        # Confirmar la reserva de asesoría.
        return (
            f"Asesoría {self.nombre} reservada "
            f"para {cantidad} persona(s)"
        )


# ============================================================
# 7. CÁLCULO DE COSTOS
# ============================================================

def calcular_costo_total(*args):
    """
    Calcula el costo total utilizando argumentos variables.

    Un argumento:
        Precio base.

    Dos argumentos:
        Precio base y descuento.

    Tres argumentos:
        Precio base, descuento e impuesto.

    Los descuentos e impuestos se expresan en dinero.
    """

    # Validar la cantidad de argumentos.
    if not 1 <= len(args) <= 3:
        raise ReservaError(
            "calcular_costo_total recibe de 1 a 3 argumentos"
        )

    # Verificar que los valores sean numéricos.
    for valor in args:
        if isinstance(valor, bool) or not isinstance(
            valor, (int, float)
        ):
            raise ReservaError(
                "Los valores del cálculo deben ser numéricos"
            )

        # Impedir valores negativos.
        if valor < 0:
            raise ReservaError(
                "Los valores del cálculo no pueden ser negativos"
            )

    # Obtener el precio base.
    precio = args[0]

    # Obtener el descuento si fue proporcionado.
    descuento = args[1] if len(args) >= 2 else 0

    # Obtener el impuesto si fue proporcionado.
    impuesto = args[2] if len(args) == 3 else 0

    # Evitar descuentos superiores al precio.
    if descuento > precio:
        raise ReservaError(
            "El descuento no puede superar el precio base"
        )

    # Calcular y retornar el costo total.
    return precio - descuento + impuesto


# ============================================================
# 8. BÚSQUEDA DE CLIENTES
# ============================================================

def buscar_cliente(clientes, identificacion):
    """
    Busca un cliente por identificación.

    Si el cliente no existe, convierte el error original
    KeyError en una excepción personalizada.
    """

    try:

        # Buscar el cliente en el diccionario.
        return clientes[identificacion]

    except KeyError as error:

        # Encadenar la excepción personalizada
        # con la excepción original.
        raise ClienteNoEncontradoError(
            f"Cliente {identificacion} no encontrado"
        ) from error


# ============================================================
# 9. EJECUCIÓN DE DIEZ OPERACIONES
# ============================================================

def ejecutar_10_operaciones():
    """
    Ejecuta diez operaciones para comprobar:

    - Registro y consulta de clientes.
    - Manejo de clientes inexistentes.
    - Reservas válidas.
    - Validación de disponibilidad.
    - Validación de cantidades.
    - Cálculo de costos.
    - Encadenamiento de excepciones.
    - Continuidad del sistema después de errores.
    """

    # Crear los servicios disponibles.
    servicios = [
        ReservaSala("Sala Reunion FJ", 50000, 5),
        AlquilerEquipo("Proyector + Portatil", 80000, 2),
        AsesoriaEspecializada("Asesoria Python", 60000, 10)
    ]

    # Crear clientes iniciales.
    clientes = {
        "123": "Brayan Salazar",
        "456": "Ana Lopez"
    }

    # Definir las diez operaciones de prueba.
    operaciones = [

        # Operación 1: registrar un cliente.
        (
            "1. Registrar cliente",
            lambda: clientes.update(
                {"789": "Nuevo Cliente"}
            )
        ),

        # Operación 2: buscar un cliente existente.
        (
            "2. Buscar cliente existente",
            lambda: buscar_cliente(clientes, "123")
        ),

        # Operación 3: buscar un cliente inexistente.
        (
            "3. Buscar cliente NO existente",
            lambda: buscar_cliente(clientes, "999")
        ),

        # Operación 4: reservar una sala correctamente.
        (
            "4. Reservar Sala",
            lambda: servicios[0].reservar(2)
        ),

        # Operación 5: solicitar más equipos de los disponibles.
        (
            "5. Alquilar Equipo sin cupo suficiente",
            lambda: servicios[1].reservar(5)
        ),

        # Operación 6: intentar reservar una asesoría
        # con cantidad inválida.
        (
            "6. Reservar Asesoria cantidad invalida",
            lambda: servicios[2].reservar(0)
        ),

        # Operación 7: calcular un costo sin descuento.
        (
            "7. Calcular costo 1 argumento",
            lambda: calcular_costo_total(50000)
        ),

        # Operación 8: calcular un costo con descuento.
        (
            "8. Calcular costo 2 argumentos",
            lambda: calcular_costo_total(50000, 5000)
        ),

        # Operación 9: calcular costo con descuento
        # e impuesto.
        (
            "9. Calcular costo 3 argumentos",
            lambda: calcular_costo_total(50000, 5000, 9500)
        ),

        # Operación 10: comprobar nuevamente
        # el encadenamiento de excepciones.
        (
            "10. Operacion con encadenamiento",
            lambda: buscar_cliente(clientes, "999")
        )
    ]

    # Contadores para resumir los resultados.
    operaciones_exitosas = 0
    errores_controlados = 0
    errores_inesperados = 0

    # Ejecutar cada operación de forma independiente.
    for nombre, funcion in operaciones:

        print(f"\n--- {nombre} ---")

        try:

            # Ejecutar la operación correspondiente.
            resultado = funcion()

        except ClienteNoEncontradoError as error:

            # Controlar errores relacionados con clientes.
            errores_controlados += 1

            print(f"ERROR CONTROLADO: {error}")

            # Registrar el error en el archivo.
            guardar_log(
                f"{nombre} - ClienteNoEncontradoError: {error}"
            )

            # Mostrar la causa original si existe.
            if error.__cause__ is not None:
                print(
                    f"Excepcion original: {error.__cause__}"
                )

        except (
            ServicioNoDisponibleError,
            CupoInsuficienteError,
            CantidadInvalidaError
        ) as error:

            # Controlar errores de disponibilidad y cantidad.
            errores_controlados += 1

            print(f"ERROR CONTROLADO: {error}")

            # Registrar el tipo de excepción.
            guardar_log(
                f"{nombre} - {type(error).__name__}: {error}"
            )

        except ReservaError as error:

            # Capturar otros errores de reserva.
            errores_controlados += 1

            print(f"ERROR CONTROLADO: {error}")

            guardar_log(
                f"{nombre} - ReservaError: {error}"
            )

        except Exception as error:

            # Capturar errores inesperados sin detener
            # inmediatamente la ejecución de las pruebas.
            errores_inesperados += 1

            print(f"ERROR INESPERADO: {error}")

            guardar_log(
                f"{nombre} - Error inesperado: {error}"
            )

        else:

            # Este bloque se ejecuta cuando la operación
            # termina sin producir excepciones.
            operaciones_exitosas += 1

            print(f"OPERACION EXITOSA: {resultado}")

            print(
                "ELSE: La operacion finalizo sin errores"
            )

        finally:

            # Este bloque se ejecuta siempre,
            # tanto si hubo errores como si no.
            print(
                "FINALLY: Operacion finalizada. "
                "El sistema continua funcionando."
            )

    # ========================================================
    # 10. RESUMEN DE RESULTADOS
    # ========================================================

    print("\n========================================")
    print("RESUMEN DE LAS DIEZ OPERACIONES")
    print("========================================")

    print(f"Operaciones ejecutadas: {len(operaciones)}")
    print(f"Operaciones exitosas: {operaciones_exitosas}")
    print(f"Errores controlados: {errores_controlados}")
    print(f"Errores inesperados: {errores_inesperados}")

    print("========================================")

    # Mostrar la disponibilidad final de los servicios.
    print("\nDISPONIBILIDAD FINAL:")

    for servicio in servicios:
        print(
            f"{servicio.nombre}: {servicio.cupo} cupo(s)"
        )

    # Confirmar si las pruebas terminaron sin errores inesperados.
    if errores_inesperados == 0:
        print(
            "\nRESULTADO: Las diez operaciones finalizaron "
            "sin errores inesperados."
        )
    else:
        print(
            "\nRESULTADO: Se detectaron errores inesperados "
            "que requieren revision."
        )


# ============================================================
# 11. PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    # Mostrar el encabezado del programa.
    print("========================================")
    print("APORTE COLABORATIVO - SOFTWARE FJ")
    print("FASE 4 - PROGRAMACION")
    print("========================================")

    # Ejecutar las diez operaciones de prueba.
    ejecutar_10_operaciones()

    # Informar que la ejecución terminó.
    print("\n========================================")
    print("FIN DE LAS PRUEBAS")
    print("Consultar archivo logs.txt")
    print("========================================")
