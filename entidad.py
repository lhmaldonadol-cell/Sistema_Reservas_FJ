
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: entidad.py
# DESCRIPCIÓN:
# Este archivo contiene la clase abstracta Entidad.
#
# Su propósito es establecer una estructura general
# para las entidades del sistema, permitiendo aplicar
# los principios de abstracción, herencia y encapsulación
# de la programación orientada a objetos.
# ============================================================

# ------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# ------------------------------------------------------------

# ABC permite definir clases abstractas.
# abstractmethod permite declarar métodos obligatorios
# que deberán implementar las clases que hereden de Entidad.

from abc import ABC, abstractmethod

# ------------------------------------------------------------
# 2. DEFINICIÓN DE LA CLASE ABSTRACTA ENTIDAD
# ------------------------------------------------------------

# La clase Entidad hereda de ABC.
# Esto significa que no se pueden crear objetos directamente
# de esta clase mientras tenga métodos abstractos pendientes.

class Entidad(ABC):

    # --------------------------------------------------------
    # 2.1. CONSTRUCTOR DE LA CLASE
    # --------------------------------------------------------

    def __init__(self, identificador):

        # El constructor recibe un identificador que permite
        # diferenciar cada entidad dentro del sistema.
        #
        # Se utiliza un guion bajo (_) para indicar que
        # el atributo es de uso interno de la clase.

        self._identificador = identificador

    # --------------------------------------------------------
    # 2.2. MÉTODO PARA CONSULTAR EL IDENTIFICADOR
    # --------------------------------------------------------

    @property
    def identificador(self):

        # La propiedad permite consultar el identificador
        # sin acceder directamente al atributo interno.
        # Ejemplo: cliente.identificador

        return self._identificador

    # --------------------------------------------------------
    # 2.3. MÉTODO ABSTRACTO
    # --------------------------------------------------------

    @abstractmethod
    def mostrar_informacion(self):

        """
        # Este método establece una obligación para
        # las clases que hereden de Entidad.
        #
        # Cada clase hija deberá implementar su propia
        # versión de mostrar_informacion().
        #
        # Por ejemplo, la clase Cliente podrá mostrar:
        # - Identificador
        # - Nombre
        # - Correo electrónico
        # - Teléfono
        #
        # La instrucción pass indica que este método
        # no tiene implementación en la clase base."""

        pass

# ============================================================
# FIN DEL ARCHIVO entidad.py
# ============================================================