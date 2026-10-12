# ACCESO A DATOS: INGRESO DE MERCADERÍA (COMPRAS)
import base_datos


def obtener_proveedores():
    """Devuelve [(id_proveedor, nombre), ...] ordenados por nombre."""
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_proveedor, nombre FROM PROVEEDOR ORDER BY nombre")
        return cursor.fetchall()
    finally:
        conexion.close()


def registrar_ingreso(id_proveedor, numero_remito, id_empleado, items):
    """Registra una compra/ingreso de mercadería y suma el stock.

    items: lista de (id_producto, cantidad).

    Igual que en los pedidos, todo va en UNA transacción: si algo falla
    no queda guardada ninguna parte. Devuelve el id de la compra creada.
    """
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()

        # 1) Cabecera de la compra
        cursor.execute(
            "INSERT INTO COMPRA (numero_remito, id_proveedor, id_empleado) "
            "VALUES (?, ?, ?)",
            (numero_remito, id_proveedor, id_empleado)
        )
        id_compra = cursor.lastrowid

        for id_producto, cantidad in items:
            # 2) Detalle de la compra
            cursor.execute(
                "INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) "
                "VALUES (?, ?, ?)",
                (id_compra, id_producto, cantidad)
            )

            # 3) Sumar al stock actual
            cursor.execute(
                "UPDATE PRODUCTO SET stock_actual = stock_actual + ? "
                "WHERE id_producto = ?",
                (cantidad, id_producto)
            )

            # 4) Trazabilidad: movimiento de ingreso (sin pedido asociado)
            cursor.execute(
                "INSERT INTO STOCK_MOVIMIENTO "
                "(tipo_movimiento, cantidad, id_producto, id_pedido) "
                "VALUES (?, ?, ?, NULL)",
                ("INGRESO", cantidad, id_producto)
            )

        conexion.commit()
        return id_compra
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
