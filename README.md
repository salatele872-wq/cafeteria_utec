# Sistema de pedidos – Cafetería UTEC

Programa en Python (consola) que administra los pedidos de la cafetería de la UTEC usando **dos filas FIFO**: una para pedidos normales y otra para pedidos prioritarios (clientes con clases próximas).

## Regla de atención

- Dentro de cada fila se respeta el orden de llegada (FIFO).
- Al preparar un pedido, se atiende **primero la fila prioritaria**; si está vacía, se atiende la fila normal.

## Datos de cada pedido

| Dato | Descripción |
|------|-------------|
| Número de pedido | Identificador único |
| Nombre del cliente | Persona que realizó el pedido |
| Producto | Alimento o bebida solicitada |
| Cantidad | Número de unidades |
| Tipo | Normal o Prioritario |
| Tiempo de preparación | Minutos estimados |

## Funciones

1. Registrar pedido
2. Preparar el siguiente pedido
3. Consultar el siguiente pedido
4. Mostrar pedidos pendientes
5. Consultar estadísticas
6. Cancelar pedido

## Estructura de datos

Se usa `collections.deque` para cada fila (`append` al registrar, `popleft` al preparar), lo que da operaciones O(1) y garantiza FIFO.

## Ejecución

Requiere Python 3.8 o superior.

```bash
python cafeteria.py
```

## Autor

Oscar Guerrero Hernández – TICS 41, Universidad Tecnológica de Tulancingo.
