# Aporte: Brayan Salazar - Fase 4 Programacion
# Manejo avanzado de excepciones + 10 operaciones + logs + sobrecarga
# Repositorio grupal: Sistema_Reservas_FJ
# CORREGIDO segun guia: salas, equipos y asesorias

import datetime

class ReservaError(Exception):
    pass

class ClienteNoEncontradoError(ReservaError):
    pass

class ServicioNoDisponibleError(ReservaError):
    pass

class FechaInvalidaError(ReservaError):
    pass

class CupoInsuficienteError(ReservaError):
    pass

def guardar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {mensaje}\n")

class Servicio:
    def __init__(self, nombre, precio, cupo):
        self.nombre = nombre
        self.precio = precio
        self.cupo = cupo
    def reservar(self, cantidad):
        raise NotImplementedError

class ReservaSala(Servicio):
    def reservar(self, cantidad):
        if cantidad > self.cupo:
            raise CupoInsuficienteError(f"Sala {self.nombre}: solo hay {self.cupo} cupos")
        self.cupo -= cantidad
        return f"Sala {self.nombre} reservada x{cantidad}"

class AlquilerEquipo(Servicio):
    def reservar(self, cantidad):
        if self.cupo == 0:
            raise ServicioNoDisponibleError(f"Equipo {self.nombre} sin disponibilidad")
        self.cupo -= cantidad
        return f"Equipo {self.nombre} alquilado x{cantidad}"

class AsesoriaEspecializada(Servicio):
    def reservar(self, cantidad):
        if cantidad <= 0:
            raise FechaInvalidaError("Cantidad debe ser mayor a 0")
        self.cupo -= cantidad
        return f"Asesoria {self.nombre} reservada x{cantidad}"

def calcular_costo_total(*args):
    if len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return args[0] - args[1]
    elif len(args) == 3:
        return (args[0] - args[1]) + args[2]
    else:
        raise ReservaError("calcular_costo_total recibe 1 a 3 argumentos")

def ejecutar_10_operaciones():
    servicios = [
        ReservaSala("Sala Reunion FJ", 50000, 5),
        AlquilerEquipo("Proyector + Portatil", 80000, 2),
        AsesoriaEspecializada("Asesoria Python", 60000, 10)
    ]
    clientes = {"123": "Brayan Salazar", "456": "Ana Lopez"}

    operaciones = [
        ("1. Registrar cliente", lambda: clientes.update({"789": "Nuevo Cliente"})),
        ("2. Buscar cliente existente", lambda: clientes["123"]),
        ("3. Buscar cliente NO existente", lambda: clientes["999"]),
        ("4. Reservar Sala", lambda: servicios[0].reservar(2)),
        ("5. Alquilar Equipo sin cupo", lambda: servicios[1].reservar(5)),
        ("6. Reservar Asesoria cantidad invalida", lambda: servicios[2].reservar(0)),
        ("7. Calcular costo 1 arg", lambda: calcular_costo_total(50000)),
        ("8. Calcular costo 2 args", lambda: calcular_costo_total(50000, 5000)),
        ("9. Calcular costo 3 args", lambda: calcular_costo_total(50000, 5000, 9500)),
        ("10. Operacion con encadenamiento", lambda: (_ for _ in ()).throw(ClienteNoEncontradoError("Cliente 999 no existe"))),
    ]

    for nombre, funcion in operaciones:
        try:
            resultado = funcion()
            print(f"{nombre} -> OK: {resultado}")
        except ClienteNoEncontradoError as e:
            print(f"{nombre} -> ERROR CAPTURADO: {e}")
            guardar_log(f"{nombre} - ClienteNoEncontrado: {e}")
        except (ServicioNoDisponibleError, CupoInsuficienteError, FechaInvalidaError) as e:
            print(f"{nombre} -> ERROR CAPTURADO: {e}")
            guardar_log(f"{nombre} - {type(e).__name__}: {e}")
        except KeyError as e:
            print(f"{nombre} -> ERROR CAPTURADO KeyError: {e} - se encadena")
            guardar_log(f"{nombre} - KeyError: {e}")
            try:
                raise ClienteNoEncontradoError(f"Cliente {e} no encontrado en sistema") from e
            except ClienteNoEncontradoError as e2:
                print(f"   Encadenado: {e2} | Causa: {e2.__cause__}")
        except Exception as e:
            print(f"{nombre} -> ERROR GENERAL: {e}")
            guardar_log(f"{nombre} - General: {e}")
        else:
            print(f"   else: {nombre} salio sin errores")
        finally:
            print(f"   finally: {nombre} finalizo, sistema sigue vivo\n")

if __name__ == "__main__":
    print("=== INICIO APORTE BRAYAN - 10 OPERACIONES CORREGIDO ===")
    ejecutar_10_operaciones()
    print("=== FIN: App no se cayo. Revisa logs.txt ===")
