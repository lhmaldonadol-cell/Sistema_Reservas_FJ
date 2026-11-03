
# ============================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
#           SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# ARCHIVO: servicio.py
#
# DESCRIPCIÓN:
# Este archivo contiene la clase abstracta Servicio y
# tres clases especializadas:
#
# 1. ServicioSala
# 2. AlquilerEquipo
# 3. AsesoriaEspecializada
#
# Se aplican los conceptos de:
# - Abstracción.
# - Herencia.
# - Polimorfismo.
# - Sobrescritura de métodos.
# - Encapsulación.
# - Parámetros opcionales.
# - Manejo de excepciones personalizadas.
#
# Las tarifas son valores de ejemplo para las pruebas.
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS Y EXCEPCIONES
# ------------------------------------------------------------

# ABC permite crear clases abstractas.
# abstractmethod define métodos obligatorios.
from abc import ABC, abstractmethod

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoCostoError
)


# ------------------------------------------------------------
# 2. CLASE ABSTRACTA SERVICIO
# ------------------------------------------------------------

class Servicio(ABC):

    """
    Representa las características comunes de los servicios.

    Atributos:
    - identificador: código único del servicio.
    - nombre: nombre descriptivo del servicio.
    - tarifa_base: costo por unidad de duración.
    - disponible: indica si se pueden crear reservas.

    Esta clase no puede instanciarse directamente porque
    contiene métodos abstractos.
    """

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_base,
        disponible=True
    ):

        # Validamos el identificador.
        if type(identificador) is not int or identificador <= 0:
            raise DatosInvalidosError(
                "El identificador del servicio debe "
                "ser un entero positivo."
            )

        # Validamos el nombre.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio no puede estar vacío."
            )

        # Validamos que la tarifa sea numérica y positiva.
        # Se rechazan booleanos porque Python los considera
        # subtipos de los números enteros.
        if (
            type(tarifa_base) not in (int, float)
            or not 0 < tarifa_base < float("inf")
        ):
            raise DatosInvalidosError(
                "La tarifa debe ser un número positivo y finito."
            )

        # Validamos que la disponibilidad sea booleana.
        if not isinstance(disponible, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser True o False."
            )

        # Guardamos los atributos de uso interno.
        self._identificador = identificador
        self._nombre = nombre.strip()
        self._tarifa_base = tarifa_base
        self._disponible = disponible

    # --------------------------------------------------------
    # 2.1. PROPIEDADES DE CONSULTA
    # --------------------------------------------------------

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    # --------------------------------------------------------
    # 2.2. CAMBIAR DISPONIBILIDAD
    # --------------------------------------------------------

    def cambiar_disponibilidad(self, disponible):

        # Comprobamos el tipo del valor recibido.
        if not isinstance(disponible, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser True o False."
            )

        # Actualizamos el estado del servicio.
        self._disponible = disponible

    # --------------------------------------------------------
    # 2.3. VALIDAR DISPONIBILIDAD Y DURACIÓN
    # --------------------------------------------------------

    def validar_parametros(self, duracion):

        # No permitimos utilizar un servicio no disponible.
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' "
                "no se encuentra disponible."
            )

        # La duración debe ser un entero positivo.
        if type(duracion) is not int or duracion <= 0:
            raise DatosInvalidosError(
                "La duración debe ser un entero positivo."
            )

        return True

    # --------------------------------------------------------
    # 2.4. CALCULAR COSTO CON PARÁMETROS OPCIONALES
    # --------------------------------------------------------

    def aplicar_ajustes(
        self,
        subtotal,
        descuento=0,
        impuesto=0
    ):

        """
        Aplica descuento e impuesto al subtotal.

        Parámetros:
        - subtotal: costo antes de ajustes.
        - descuento: porcentaje opcional, entre 0 y 100.
        - impuesto: porcentaje opcional, entre 0 y 100.

        Ejemplo:
        subtotal = 100000
        descuento = 10
        impuesto = 19

        Total = 90000 + 17100 = 107100

        El impuesto se aplica después del descuento.
        """

        # Validamos los valores numéricos.
        for nombre, valor in (
            ("subtotal", subtotal),
            ("descuento", descuento),
            ("impuesto", impuesto)
        ):

            if (
                type(valor) not in (int, float)
                or not float("-inf") < valor < float("inf")
            ):
                raise CalculoCostoError(
                    f"El valor de {nombre} debe ser "
                    "un número finito."
                )

        # El subtotal no puede ser negativo.
        if subtotal < 0:
            raise CalculoCostoError(
                "El subtotal no puede ser negativo."
            )

        # Los porcentajes deben estar entre 0 y 100.
        if not 0 <= descuento <= 100:
            raise CalculoCostoError(
                "El descuento debe estar entre 0 y 100."
            )

        if not 0 <= impuesto <= 100:
            raise CalculoCostoError(
                "El impuesto debe estar entre 0 y 100."
            )

        # Calculamos el descuento.
        valor_descuento = subtotal * descuento / 100

        # Obtenemos el valor después del descuento.
        subtotal_descontado = subtotal - valor_descuento

        # Calculamos el impuesto sobre el valor descontado.
        valor_impuesto = subtotal_descontado * impuesto / 100

        # Calculamos el costo final.
        total = subtotal_descontado + valor_impuesto

        # Comprobamos que el resultado sea finito.
        if not float("-inf") < total < float("inf"):
            raise CalculoCostoError(
                "El cálculo produjo un resultado no válido."
            )

        # Redondeamos a dos decimales.
        return round(total, 2)

    # --------------------------------------------------------
    # 2.5. MÉTODOS ABSTRACTOS
    # --------------------------------------------------------

    @abstractmethod
    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        # Cada servicio implementará su propio cálculo.
        pass

    @abstractmethod
    def mostrar_descripcion(self):

        # Cada servicio tendrá su propia descripción.
        pass


# ------------------------------------------------------------
# 3. CLASE SERVICIO DE RESERVA DE SALAS
# ------------------------------------------------------------

class ServicioSala(Servicio):

    """
    Representa el servicio de reserva de salas.

    La duración se expresa en horas.
    El costo se calcula según la tarifa por hora.
    """

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_hora,
        capacidad,
        disponible=True
    ):

        # Inicializamos los atributos comunes.
        super().__init__(
            identificador,
            nombre,
            tarifa_hora,
            disponible
        )

        # Validamos la capacidad de la sala.
        if type(capacidad) is not int or capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad debe ser un entero positivo."
            )

        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    # Sobrescribimos el método de validación.
    def validar_parametros(self, duracion):

        # Ejecutamos las validaciones generales.
        super().validar_parametros(duracion)

        # Regla propuesta: máximo 12 horas por reserva.
        if duracion > 12:
            raise DatosInvalidosError(
                "Una sala puede reservarse por "
                "un máximo de 12 horas."
            )

        return True

    # Sobrescribimos el método de cálculo.
    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        # Validamos la duración y disponibilidad.
        self.validar_parametros(duracion)

        # Calculamos el subtotal por horas.
        subtotal = self.tarifa_base * duracion

        # Aplicamos los ajustes opcionales.
        return self.aplicar_ajustes(
            subtotal,
            descuento,
            impuesto
        )

    # Descripción específica del servicio.
    def mostrar_descripcion(self):

        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Tarifa: ${self.tarifa_base:,.2f}/hora"
        )


# ------------------------------------------------------------
# 4. CLASE ALQUILER DE EQUIPOS
# ------------------------------------------------------------

class AlquilerEquipo(Servicio):

    """
    Representa el alquiler de equipos tecnológicos.

    La duración se expresa en días.
    El costo se calcula según la tarifa diaria.
    """

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_dia,
        tipo_equipo,
        disponible=True
    ):

        # Inicializamos los atributos generales.
        super().__init__(
            identificador,
            nombre,
            tarifa_dia,
            disponible
        )

        # Validamos el tipo de equipo.
        if (
            not isinstance(tipo_equipo, str)
            or not tipo_equipo.strip()
        ):
            raise DatosInvalidosError(
                "El tipo de equipo no puede estar vacío."
            )

        self.__tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    # Validación especializada para alquileres.
    def validar_parametros(self, duracion):

        super().validar_parametros(duracion)

        # Regla propuesta: máximo 30 días.
        if duracion > 30:
            raise DatosInvalidosError(
                "El alquiler no puede superar los 30 días."
            )

        return True

    # Cálculo del costo del alquiler.
    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        self.validar_parametros(duracion)

        # Calculamos el subtotal por días.
        subtotal = self.tarifa_base * duracion

        return self.aplicar_ajustes(
            subtotal,
            descuento,
            impuesto
        )

    # Descripción específica del alquiler.
    def mostrar_descripcion(self):

        return (
            f"Equipo: {self.nombre} | "
            f"Tipo: {self.__tipo_equipo} | "
            f"Tarifa: ${self.tarifa_base:,.2f}/día"
        )


# ------------------------------------------------------------
# 5. CLASE ASESORÍA ESPECIALIZADA
# ------------------------------------------------------------

class AsesoriaEspecializada(Servicio):

    """
    Representa una asesoría profesional.

    La duración se expresa en horas.
    El costo se calcula según la tarifa por hora.
    """

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_hora,
        especialidad,
        disponible=True
    ):

        # Inicializamos los atributos comunes.
        super().__init__(
            identificador,
            nombre,
            tarifa_hora,
            disponible
        )

        # Validamos la especialidad.
        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise DatosInvalidosError(
                "La especialidad no puede estar vacía."
            )

        self.__especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self.__especialidad

    # Validación especializada para asesorías.
    def validar_parametros(self, duracion):

        super().validar_parametros(duracion)

        # Regla propuesta: máximo 8 horas por asesoría.
        if duracion > 8:
            raise DatosInvalidosError(
                "Una asesoría no puede superar las 8 horas."
            )

        return True

    # Cálculo del costo de la asesoría.
    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        self.validar_parametros(duracion)

        # Calculamos el subtotal por horas.
        subtotal = self.tarifa_base * duracion

        return self.aplicar_ajustes(
            subtotal,
            descuento,
            impuesto
        )

    # Descripción específica de la asesoría.
    def mostrar_descripcion(self):

        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self.__especialidad} | "
            f"Tarifa: ${self.tarifa_base:,.2f}/hora"
        )

# ============================================================
# FIN DEL ARCHIVO servicio.py
# ============================================================
