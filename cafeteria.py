"""
Sistema de pedidos de la Cafetería UTEC
Estructura de datos: dos filas (colas) FIFO -> normal y prioritaria.

Regla de atención: al preparar un pedido se atiende primero la fila
prioritaria; si está vacía, se atiende la fila normal.
"""

from collections import deque
from dataclasses import dataclass

NORMAL = "Normal"
PRIORITARIO = "Prioritario"


@dataclass
class Pedido:
    numero: int
    cliente: str
    producto: str
    cantidad: int
    tipo: str
    tiempo_preparacion: int  # minutos

    def __str__(self):
        return (f"#{self.numero} | {self.cliente} | {self.producto} x{self.cantidad} "
                f"| {self.tipo} | {self.tiempo_preparacion} min")


class Cafeteria:
    def __init__(self):
        self.fila_normal = deque()
        self.fila_prioritaria = deque()
        self.atendidos = []       # pedidos ya preparados
        self.cancelados = []      # pedidos cancelados
        self._numeros_usados = set()

    # 1. Registrar pedido
    def registrar(self, pedido):
        if pedido.numero in self._numeros_usados:
            return False
        self._numeros_usados.add(pedido.numero)
        if pedido.tipo == PRIORITARIO:
            self.fila_prioritaria.append(pedido)
        else:
            self.fila_normal.append(pedido)
        return True

    # 3. Consultar el siguiente pedido (sin sacarlo)
    def siguiente(self):
        if self.fila_prioritaria:
            return self.fila_prioritaria[0]
        if self.fila_normal:
            return self.fila_normal[0]
        return None

    # 2. Preparar el siguiente pedido
    def preparar(self):
        if self.fila_prioritaria:
            pedido = self.fila_prioritaria.popleft()
        elif self.fila_normal:
            pedido = self.fila_normal.popleft()
        else:
            return None
        self.atendidos.append(pedido)
        return pedido

    # 4. Mostrar pedidos pendientes
    def pendientes(self):
        return list(self.fila_prioritaria), list(self.fila_normal)

    # 6. Cancelar pedido
    def cancelar(self, numero):
        for fila in (self.fila_prioritaria, self.fila_normal):
            for pedido in fila:
                if pedido.numero == numero:
                    fila.remove(pedido)
                    self.cancelados.append(pedido)
                    return pedido
        return None

    # 5. Estadísticas
    def estadisticas(self):
        pend_p, pend_n = self.pendientes()
        pendientes = pend_p + pend_n
        tiempo_pend = sum(p.tiempo_preparacion for p in pendientes)
        tiempo_atend = sum(p.tiempo_preparacion for p in self.atendidos)
        return {
            "pendientes_prioritarios": len(pend_p),
            "pendientes_normales": len(pend_n),
            "total_pendientes": len(pendientes),
            "atendidos": len(self.atendidos),
            "cancelados": len(self.cancelados),
            "tiempo_estimado_pendientes": tiempo_pend,
            "tiempo_total_atendidos": tiempo_atend,
            "promedio_preparacion": (
                tiempo_atend / len(self.atendidos) if self.atendidos else 0
            ),
        }


# ---------------------- Interfaz de consola ----------------------

def leer_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"  Ingresa un número mayor o igual a {minimo}.")
        except ValueError:
            print("  Ingresa un número entero válido.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  Este campo no puede estar vacío.")


def opcion_registrar(cafe):
    print("\n--- Registrar pedido ---")
    numero = leer_entero("Número de pedido: ")
    if numero in cafe._numeros_usados:
        print("  Ese número de pedido ya existe.")
        return
    cliente = leer_texto("Nombre del cliente: ")
    producto = leer_texto("Producto: ")
    cantidad = leer_entero("Cantidad: ")
    while True:
        tipo = input("Tipo (1=Normal, 2=Prioritario): ").strip()
        if tipo in ("1", "2"):
            break
        print("  Opción inválida.")
    tipo = NORMAL if tipo == "1" else PRIORITARIO
    tiempo = leer_entero("Tiempo de preparación (minutos): ")
    cafe.registrar(Pedido(numero, cliente, producto, cantidad, tipo, tiempo))
    print(f"  Pedido #{numero} registrado en la fila {tipo.lower()}.")


def opcion_preparar(cafe):
    print("\n--- Preparar siguiente pedido ---")
    pedido = cafe.preparar()
    print(f"  Preparando: {pedido}" if pedido else "  No hay pedidos pendientes.")


def opcion_siguiente(cafe):
    print("\n--- Siguiente pedido ---")
    pedido = cafe.siguiente()
    print(f"  {pedido}" if pedido else "  No hay pedidos pendientes.")


def opcion_pendientes(cafe):
    prioritarios, normales = cafe.pendientes()
    print("\n--- Pedidos pendientes ---")
    print(f"Fila prioritaria ({len(prioritarios)}):")
    for p in prioritarios:
        print(f"  {p}")
    if not prioritarios:
        print("  (vacía)")
    print(f"Fila normal ({len(normales)}):")
    for p in normales:
        print(f"  {p}")
    if not normales:
        print("  (vacía)")


def opcion_estadisticas(cafe):
    e = cafe.estadisticas()
    print("\n--- Estadísticas ---")
    print(f"Pendientes prioritarios: {e['pendientes_prioritarios']}")
    print(f"Pendientes normales:     {e['pendientes_normales']}")
    print(f"Total pendientes:        {e['total_pendientes']}")
    print(f"Pedidos atendidos:       {e['atendidos']}")
    print(f"Pedidos cancelados:      {e['cancelados']}")
    print(f"Tiempo estimado de pendientes: {e['tiempo_estimado_pendientes']} min")
    print(f"Tiempo total de atendidos:     {e['tiempo_total_atendidos']} min")
    print(f"Promedio de preparación:       {e['promedio_preparacion']:.1f} min")


def opcion_cancelar(cafe):
    print("\n--- Cancelar pedido ---")
    numero = leer_entero("Número de pedido a cancelar: ")
    pedido = cafe.cancelar(numero)
    print(f"  Cancelado: {pedido}" if pedido
          else "  No se encontró un pedido pendiente con ese número.")


def menu():
    cafe = Cafeteria()
    acciones = {
        "1": opcion_registrar,
        "2": opcion_preparar,
        "3": opcion_siguiente,
        "4": opcion_pendientes,
        "5": opcion_estadisticas,
        "6": opcion_cancelar,
    }
    while True:
        print("\n===== CAFETERÍA UTEC =====")
        print("1. Registrar pedido")
        print("2. Preparar el siguiente pedido")
        print("3. Consultar el siguiente pedido")
        print("4. Mostrar pedidos pendientes")
        print("5. Consultar estadísticas")
        print("6. Cancelar pedido")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "0":
            print("¡Hasta luego!")
            break
        accion = acciones.get(opcion)
        if accion:
            accion(cafe)
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
