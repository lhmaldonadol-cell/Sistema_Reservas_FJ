
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: cliente.py
#
# DESCRIPCIÓN:
# Este archivo contiene la clase Cliente.
#
# Su función es representar a los clientes del sistema,
# almacenar sus datos y comprobar que la información
# ingresada cumpla las condiciones establecidas.
#
# Se aplican los siguientes conceptos:
# - Programación orientada a objetos.
# - Herencia.
# - Encapsulación.
# - Validación de datos.
# - Manejo de excepciones personalizadas.
# - Sobrescritura de métodos.
# ============================================================

# ------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS Y CLASES
# ------------------------------------------------------------

# La librería re permite comprobar el formato del correo
# electrónico mediante expresiones regulares.
import re

# Importamos la clase abstracta Entidad.
from entidad import Entidad

# Importamos la excepción para controlar datos incorrectos.
from excepciones import DatosInvalidosError

# ------------------------------------------------------------
# 2. DEFINICIÓN DE LA CLASE CLIENTE
# ------------------------------------------------------------

# Cliente hereda de Entidad y utiliza su identificador.
class Cliente(Entidad):

    """
    Representa un cliente registrado en Software FJ.

    Atributos:
    - identificador: número único del cliente.
    - nombre: nombre completo.
    - correo: dirección de correo electrónico.
    - telefono: número de contacto.

    Los datos personales se almacenan mediante
    atributos privados para proteger su acceso.
    """

    # --------------------------------------------------------
    # 2.1. CONSTRUCTOR DE LA CLASE
    # --------------------------------------------------------

    def __init__(self, identificador, nombre, correo, telefono):

        # Validamos que el identificador sea un número
        # entero positivo. No se aceptan valores booleanos.
        if type(identificador) is not int or identificador <= 0:
            raise DatosInvalidosError(
                "El identificador debe ser un entero positivo."
            )

        # Verificamos que el nombre sea una cadena de texto
        # y que no esté vacío ni contenga solo espacios.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del cliente no puede estar vacío."
            )

        # Comprobamos que el correo sea una cadena de texto.
        if not isinstance(correo, str):
            raise DatosInvalidosError(
                "El correo electrónico debe ser texto."
            )

        # Eliminamos espacios al inicio y al final.
        correo = correo.strip().lower()

        # Validamos el formato básico del correo electrónico.
        # Esta comprobación no garantiza que el correo exista.
        patron_correo = r"[^@\s]+@[^@\s]+\.[^@\s]+"

        if not re.fullmatch(patron_correo, correo):
            raise DatosInvalidosError(
                "El correo electrónico no es válido."
            )

        # El teléfono puede recibirse como texto o entero.
        # Se rechazan otros tipos para evitar conversiones
        # inesperadas, como números decimales.
        if isinstance(telefono, bool) or not isinstance(
            telefono, (str, int)
        ):
            raise DatosInvalidosError(
                "El teléfono debe contener únicamente dígitos."
            )

        # Convertimos el teléfono a texto para conservarlo
        # como dato de contacto, no como cantidad numérica.
        telefono = str(telefono).strip()

        # Comprobamos que tenga entre 7 y 15 dígitos.
        if (
            not telefono.isascii()
            or not telefono.isdecimal()
            or not 7 <= len(telefono) <= 15
        ):
            raise DatosInvalidosError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        # Inicializamos el identificador mediante
        # el constructor de la clase padre Entidad.
        super().__init__(identificador)

        # Guardamos los datos personales como atributos
        # privados utilizando doble guion bajo (__).
        self.__nombre = nombre.strip()
        self.__correo = correo
        self.__telefono = telefono

    # --------------------------------------------------------
    # 2.2. PROPIEDAD PARA CONSULTAR EL NOMBRE
    # --------------------------------------------------------

    @property
    def nombre(self):

        # Permite consultar el nombre del cliente
        # sin acceder directamente al atributo privado.
        return self.__nombre

    # --------------------------------------------------------
    # 2.3. PROPIEDAD PARA CONSULTAR EL CORREO
    # --------------------------------------------------------

    @property
    def correo(self):

        # Devuelve el correo electrónico registrado.
        return self.__correo

    # --------------------------------------------------------
    # 2.4. PROPIEDAD PARA CONSULTAR EL TELÉFONO
    # --------------------------------------------------------

    @property
    def telefono(self):

        # Devuelve el número telefónico del cliente.
        return self.__telefono

    # --------------------------------------------------------
    # 2.5. MÉTODO PARA MOSTRAR INFORMACIÓN
    # --------------------------------------------------------

    def mostrar_informacion(self):

        # Implementamos el método abstracto definido
        # en la clase padre Entidad.
        #
        # Este método devuelve una cadena de texto
        # con los datos principales del cliente.
        #
        # Se utilizará para mostrar registros en
        # las pruebas y consultas del sistema.

        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )

# ============================================================
# FIN DEL ARCHIVO cliente.py
# ============================================================
