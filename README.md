# Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Software FJ

**Curso:** Programación – 213023  
**Actividad:** Fase 4 – Desarrollo del componente práctico  
**Lenguaje:** Python  
**Modalidad:** Trabajo colaborativo

## 1. Descripción del proyecto

El Sistema Integral de Gestión de Clientes, Servicios y Reservas es una aplicación desarrollada en Python para la empresa ficticia Software FJ.

Su propósito es administrar el registro de clientes, la consulta de servicios y la creación, confirmación, cancelación y procesamiento de reservas.

El proyecto aplica los principios de programación orientada a objetos, especialmente herencia, encapsulación, abstracción, polimorfismo y manejo avanzado de excepciones.

## 2. Funcionalidades principales

- Registrar y consultar clientes.
- Validar la información ingresada.
- Consultar los servicios disponibles.
- Crear reservas asociadas a clientes y servicios.
- Confirmar y cancelar reservas.
- Procesar reservas y calcular costos.
- Aplicar descuentos e impuestos.
- Controlar operaciones inválidas mediante excepciones.
- Registrar eventos y errores en un archivo de historial.
- Mantener el programa activo después de errores controlados.

## 3. Servicios disponibles

El sistema contempla tres tipos de servicios:

| Servicio | Tarifa de ejemplo |
|---|---|
| Reserva de salas | $50.000 por hora |
| Alquiler de equipos | $80.000 por día |
| Asesorías especializadas | $60.000 por hora |

Las tarifas son valores simulados para el desarrollo académico.

## 4. Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `entidad.py` | Define la clase abstracta general. |
| `cliente.py` | Implementa la clase Cliente y sus validaciones. |
| `servicio.py` | Define los servicios y sus clases especializadas. |
| `reserva.py` | Administra las reservas y sus estados. |
| `excepciones.py` | Contiene las excepciones personalizadas. |
| `main.py` | Integra los módulos mediante un menú interactivo. |
| `prueba_servicios.py` | Ejecuta pruebas del módulo de servicios. |
| `prueba_reservas.py` | Ejecuta diez pruebas del módulo de reservas. |

## 5. Requisitos para ejecutar

- Python 3 instalado.
- Visual Studio Code u otro editor compatible.
- Terminal de comandos.

El proyecto utiliza módulos de la biblioteca estándar de Python y no requiere una base de datos.

## 6. Instrucciones de ejecución

1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto.
3. Abrir una terminal dentro de esa carpeta.
4. Ejecutar el comando:

```bash
py main.py
```

En sistemas donde no esté disponible el comando `py`, utilizar:

```bash
python main.py
```

## 7. Menú principal

El sistema presenta las siguientes opciones:

1. Registrar cliente.
2. Consultar clientes.
3. Consultar servicios.
4. Crear reserva.
5. Consultar reservas.
6. Confirmar reserva.
7. Cancelar reserva.
8. Procesar reserva.
9. Consultar historial de eventos.
0. Salir.

## 8. Pruebas del sistema

Para ejecutar las pruebas de servicios:

```bash
py prueba_servicios.py
```

Para ejecutar las pruebas de reservas:

```bash
py prueba_reservas.py
```

En las pruebas realizadas del módulo de reservas se obtuvieron los siguientes resultados:

- Pruebas ejecutadas: 10.
- Pruebas correctas: 10.
- Pruebas fallidas: 0.

También se verificaron desde el menú principal el registro de clientes, la creación y procesamiento de reservas, el cálculo de costos y el manejo de operaciones inválidas.

## 9. Manejo de excepciones

El proyecto utiliza excepciones personalizadas para controlar situaciones como:

- Datos incorrectos.
- Clientes duplicados.
- Servicios no disponibles.
- Reservas inválidas.
- Operaciones no permitidas.
- Errores en los cálculos.

Se emplean estructuras `try`, `except`, `else` y `finally`, así como encadenamiento de excepciones en las operaciones correspondientes.

## 10. Registro de eventos

El sistema genera un archivo `sistema.log` que registra eventos relevantes y errores durante su ejecución.

Este archivo se utiliza únicamente para el seguimiento de operaciones y errores.

Los datos de clientes, servicios y reservas se mantienen temporalmente en memoria, sin utilizar bases de datos.

## 11. Trabajo colaborativo

El repositorio está destinado al desarrollo colaborativo de la actividad académica.

Los integrantes del equipo podrán revisar el código, ejecutar las pruebas, documentar mejoras, proponer correcciones y registrar sus contribuciones mediante GitHub.

Se recomienda mantener los comentarios del código en español, documentar las modificaciones y comprobar que las funcionalidades existentes continúen operando correctamente.

## 12. Estado del proyecto

El proyecto cuenta con los módulos principales implementados, pruebas funcionales de servicios y reservas, un menú interactivo y registro de eventos.

Se encuentra en preparación para su publicación y revisión colaborativa.