# CONEXIÓN A LA BASE DE DATOS (SQLite)
# Acá está todo lo que tiene que ver con abrir la base y crear las tablas.
# El resto de los archivos solo piden la conexión con conectar().
import os
import sqlite3

# La base y el script.sql se buscan en la misma carpeta que este archivo,
# así funciona sin importar desde dónde se ejecute la app.
CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(CARPETA, "stock.db")
RUTA_SCRIPT = os.path.join(CARPETA, "script.sql")


def conectar():
    """Devuelve una conexión a la base de datos (el archivo se crea solo si no existe).

    Quien la pida es responsable de cerrarla con conexion.close().
    """
    conexion = sqlite3.connect(RUTA_DB)

    # SQLite por defecto NO controla las claves foraneas (FOREIGN KEY),
    # hay que activarlas en cada conexión.
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    """Crea las tablas ejecutando script.sql, pero solo si todavía no existen.

    Se llama una vez al iniciar la app, así la primera vez que alguien
    corre la base queda armada sola.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    # Preguntamos si ya existe una de las tablas
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'PRODUCTO'"
    )
    existe = cursor.fetchone()

    if existe is None:
        with open(RUTA_SCRIPT, "r", encoding="utf-8") as archivo:
            conexion.executescript(archivo.read())
        print("Base de datos creada: stock.db")
    else:
        print("Base de datos encontrada: stock.db")

    conexion.close()
