# DATOS DE DEMO
# Carga áreas y productos de ejemplo SOLO si las tablas están vacías,
# así se puede llamar en cada arranque sin duplicar nada.
import base_datos

AREAS_DEMO = [
    ("Ensamble", "A01", "ensamble@empresa.com"),
    ("Mantenimiento", "A02", "mantenimiento@empresa.com"),
    ("Electrónica", "A03", "electronica@empresa.com"),
    ("Calidad", "A04", "calidad@empresa.com"),
]

# (nombre, contacto, cuit) -- datos inventados, solo para la demo
PROVEEDORES_DEMO = [
    ("Ferretería Industrial S.A.", "ventas@ferreteriaindustrial.com", "30-11111111-1"),
    ("Electro Cables S.R.L.", "pedidos@electrocables.com", "30-22222222-2"),
    ("Rodamientos del Centro", "contacto@rodamientoscentro.com", "30-33333333-3"),
]

# (nombre, stock inicial)
PRODUCTOS_DEMO = [
    ("Tornillo M6", 100),
    ("Tuerca M6", 250),
    ("Placa Base A1", 15),
    ("Soporte Motor", 8),
    ("Espina M8", 60),
    ("Resorte", 40),
    ("Oring", 120),
    ("Cables 1,5mm", 30),
    ("Cable 3mm", 25),
    ("Reguladores de caudal", 12),
]


def cargar_datos_demo():
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM AREA")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO AREA (nombre, legajo, contacto) VALUES (?, ?, ?)",
                AREAS_DEMO
            )

        cursor.execute("SELECT COUNT(*) FROM PROVEEDOR")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES (?, ?, ?)",
                PROVEEDORES_DEMO
            )

        cursor.execute("SELECT COUNT(*) FROM PRODUCTO")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT OR IGNORE INTO MARCA (nombre) VALUES (?)",
                           ("Genérica",))
            cursor.execute("SELECT id_marca FROM MARCA WHERE nombre = ?",
                           ("Genérica",))
            id_marca = cursor.fetchone()[0]
            cursor.executemany(
                "INSERT INTO PRODUCTO (nombre, id_marca, stock_actual) VALUES (?, ?, ?)",
                [(nombre, id_marca, stock) for nombre, stock in PRODUCTOS_DEMO]
            )

        conexion.commit()
    finally:
        conexion.close()
