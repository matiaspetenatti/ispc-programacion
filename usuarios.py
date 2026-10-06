import hashlib
import hmac
import os

import base_datos


def _hashear(clave, salt):
    return hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), salt, 100000)


def encriptar_clave(clave):
    # valor al azar, distinto por empleado
    salt = os.urandom(16)
    return salt.hex() + "$" + _hashear(clave, salt).hex()


def clave_correcta(clave, clave_guardada):
    try:
        salt_hex, hash_hex = clave_guardada.split("$")
        hash_nuevo = _hashear(clave, bytes.fromhex(salt_hex))
        return hmac.compare_digest(hash_nuevo, bytes.fromhex(hash_hex))
    except ValueError:
        return False


def crear_empleado(nombre, legajo, clave):
    conexion = base_datos.conectar()
    try:
        conexion.execute(
            "INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES (?, ?, ?)",
            (nombre, legajo, encriptar_clave(clave))
        )
        conexion.commit()
    finally:
        conexion.close()


def validar_login(legajo, clave):
    conexion = base_datos.conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_empleado, nombre, clave FROM EMPLEADO_DEPOSITO WHERE legajo = ?",
            (legajo,)
        )
        fila = cursor.fetchone()
    finally:
        conexion.close()

    if fila is None:
        return None                              # no existe ese legajo

    id_empleado, nombre, clave_guardada = fila
    if clave_correcta(clave, clave_guardada):
        return (id_empleado, nombre)             # login correcto
    return None                                  # clave incorrecta


def crear_usuario_demo():
    crear_empleado("Administrador", "admin", "admin123")
