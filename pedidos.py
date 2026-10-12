# ACCESO A DATOS: PEDIDOS
import base_datos


class StockInsuficiente(Exception):
    """Se intentó sacar más cantidad de la que hay en el depósito."""

    def __init__(self, producto, disponible, pedida):
        self.producto = producto
        self.disponible = disponible
        self.pedida = pedida
        super().__init__(
            f"Stock insuficiente de '{producto}': hay {disponible} y se piden {pedida}.")


def obtener_areas():
    """Devuelve [(id_area, nombre), ...] ordenadas por nombre."""
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_area, nombre FROM AREA ORDER BY nombre")
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_productos():
    """Devuelve [(id_producto, nombre, stock_actual), ...] ordenados por nombre."""
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_producto, nombre, stock_actual FROM PRODUCTO ORDER BY nombre")
        return cursor.fetchall()
    finally:
        conexion.close()


def ejecutar_pedido(id_area, id_empleado, items):
    """Registra un pedido de un área y descuenta el stock.

    items: lista de (id_producto, cantidad).

    Todo se hace en UNA transacción: si un producto no tiene stock suficiente
    (o falla cualquier cosa) no se guarda nada, ni pedido ni descuentos.
    Devuelve el id del pedido creado.
    """
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()

        # 1) Cabecera del pedido (como lo ejecuta el depósito, nace "Ejecutado")
        cursor.execute(
            "INSERT INTO PEDIDO (estado, id_area, id_empleado) VALUES (?, ?, ?)",
            ("Ejecutado", id_area, id_empleado)
        )
        id_pedido = cursor.lastrowid

        for id_producto, cantidad in items:
            # 2) Descontar stock. La condición stock_actual >= ? evita que quede
            #    negativo, aunque otro usuario haya movido stock en el medio.
            cursor.execute(
                "UPDATE PRODUCTO SET stock_actual = stock_actual - ? "
                "WHERE id_producto = ? AND stock_actual >= ?",
                (cantidad, id_producto, cantidad)
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT nombre, stock_actual FROM PRODUCTO WHERE id_producto = ?",
                    (id_producto,)
                )
                nombre, disponible = cursor.fetchone()
                raise StockInsuficiente(nombre, disponible, cantidad)

            # 3) Detalle del pedido
            cursor.execute(
                "INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) "
                "VALUES (?, ?, ?)",
                (id_pedido, id_producto, cantidad)
            )

            # 4) Trazabilidad: queda el movimiento de egreso ligado al pedido
            cursor.execute(
                "INSERT INTO STOCK_MOVIMIENTO "
                "(tipo_movimiento, cantidad, id_producto, id_pedido) "
                "VALUES (?, ?, ?, ?)",
                ("EGRESO", cantidad, id_producto, id_pedido)
            )

        conexion.commit()
        return id_pedido
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_historial():
    """Devuelve los pedidos, del más nuevo al más viejo:
    [(id_pedido, fecha, area, empleado, estado, total_unidades), ...]
    """
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT p.id_pedido, p.fecha_pedido, a.nombre, e.nombre, p.estado, "
            "       COALESCE(SUM(d.cantidad), 0) "
            "FROM PEDIDO p "
            "JOIN AREA a ON a.id_area = p.id_area "
            "JOIN EMPLEADO_DEPOSITO e ON e.id_empleado = p.id_empleado "
            "LEFT JOIN DETALLE_PEDIDO d ON d.id_pedido = p.id_pedido "
            "GROUP BY p.id_pedido "
            "ORDER BY p.fecha_pedido DESC, p.id_pedido DESC"
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_detalle(id_pedido):
    """Devuelve los productos de un pedido: [(producto, cantidad), ...]"""
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT pr.nombre, d.cantidad "
            "FROM DETALLE_PEDIDO d "
            "JOIN PRODUCTO pr ON pr.id_producto = d.id_producto "
            "WHERE d.id_pedido = ? "
            "ORDER BY pr.nombre",
            (id_pedido,)
        )
        return cursor.fetchall()
    finally:
        conexion.close()
