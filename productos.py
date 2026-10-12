# ACCESO A DATOS: PRODUCTOS
import base_datos


def obtener_stock():
    """Devuelve el stock de todos los productos:
    [(nombre, marca, ubicacion, stock_actual), ...] ordenados por nombre.
    """
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT p.nombre, m.nombre, COALESCE(p.ubicacion, '-'), p.stock_actual "
            "FROM PRODUCTO p "
            "JOIN MARCA m ON m.id_marca = p.id_marca "
            "ORDER BY p.nombre"
        )
        return cursor.fetchall()
    finally:
        conexion.close()


class ProductoDuplicado(Exception):
    """Ya existe un producto con ese nombre."""

    def __init__(self, nombre):
        self.nombre = nombre
        super().__init__(f"Ya existe un producto llamado '{nombre}'.")


def obtener_marcas():
    """Devuelve la lista de nombres de marcas, ordenada."""
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM MARCA ORDER BY nombre")
        return [fila[0] for fila in cursor.fetchall()]
    finally:
        conexion.close()


def crear_producto(nombre, marca, ubicacion, descripcion, stock_inicial):
    """Da de alta un producto nuevo. Devuelve su id_producto.

    - Si la marca no existe, se crea.
    - Si hay stock inicial, queda registrado como movimiento "STOCK_INICIAL"
      para que el stock siempre se pueda justificar con movimientos.
    - Todo en una transacción: si algo falla no se guarda nada.
    """
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()

        # No permitir dos productos con el mismo nombre (sin importar mayúsculas):
        # en los combos de pedidos e ingresos se elige por nombre.
        cursor.execute("SELECT nombre FROM PRODUCTO")
        for (existente,) in cursor.fetchall():
            if existente.casefold() == nombre.casefold():
                raise ProductoDuplicado(existente)

        # Buscar la marca (sin distinguir mayúsculas) o crearla
        cursor.execute("SELECT id_marca, nombre FROM MARCA")
        id_marca = None
        for id_existente, nombre_existente in cursor.fetchall():
            if nombre_existente.casefold() == marca.casefold():
                id_marca = id_existente
                break
        if id_marca is None:
            cursor.execute("INSERT INTO MARCA (nombre) VALUES (?)", (marca,))
            id_marca = cursor.lastrowid

        cursor.execute(
            "INSERT INTO PRODUCTO (nombre, descripcion, id_marca, ubicacion, stock_actual) "
            "VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion or None, id_marca,
             ubicacion or None, stock_inicial)
        )
        id_producto = cursor.lastrowid

        if stock_inicial > 0:
            cursor.execute(
                "INSERT INTO STOCK_MOVIMIENTO "
                "(tipo_movimiento, cantidad, id_producto, id_pedido) "
                "VALUES (?, ?, ?, NULL)",
                ("STOCK_INICIAL", stock_inicial, id_producto)
            )

        conexion.commit()
        return id_producto
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
