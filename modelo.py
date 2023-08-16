import sqlite3
import os
import datetime
from decoradores import *
# from observador import Sujeto

class RegistroLogDecoradores:
    """
    La clase RegistroLogError permite registrar los errores en
    el archivo log.txt mediante el uso de Excepciones.
    """

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log_deco.txt")

    def __init__(self, tipolog, nombrelog, especialidadlog, sedelog, fecha):
        self.tipolog = tipolog
        self.nombrelog = nombrelog
        self.especialidadlog = especialidadlog
        self.sedelog = sedelog
        self.fecha = fecha

    def registrar_evento(self):
        log_deco = open(self.ruta, "a")
        print(
            "Se ha generado un cambio:",
            self.tipolog,
            self.nombrelog,
            self.especialidadlog,
            self.sedelog,
            self.fecha,
            file=log_deco,
        )


class Modelo:
    def __init__(self):
        self.dbase = "contrasena.db"
        self.conexion = sqlite3.connect(self.dbase)
        self.cursor = self.conexion.cursor()

    def abrir_conexion(self):
        self.conexion = sqlite3.connect(self.dbase)
        self.cursor = self.conexion.cursor()

    def cerrar_conexion(self):
        self.conexion.commit()
        self.cursor.close()

    def crear_tabla(self):
        self.abrir_conexion()

        sql = (
            "CREATE TABLE IF NOT EXISTS contrasena("
            "id integer PRIMARY KEY AUTOINCREMENT, "
            "app text NOT NULL, "
            "usuario text NOT NULL, "
            "contrasena integer NOT NULL)"
        )

        self.cursor.execute(sql)
        self.cerrar_conexion()

    @decorador_alta
    def alta(self, data):
        self.abrir_conexion()
        sql = "INSERT INTO contrasena(app, usuario, contrasena) VALUES(?, ?, ?)"

        self.cursor.execute(sql, data)
        self.cerrar_conexion()
        return data

    @decorador_borrar
    def borrar(self, data):
        self.abrir_conexion()
        sql = "DELETE FROM contrasena WHERE id = ?;"
        self.cursor.execute(sql, data)
        self.cerrar_conexion()
        return data

    @decorador_editar
    def editar(self, datos):
        self.abrir_conexion()
        sql = "UPDATE contrasena SET app =?, usuario=?, contrasena=? WHERE id =?"
        self.cursor.execute(sql, datos)
        self.cerrar_conexion()
        return datos

    def extraer_registros(self):
        self.abrir_conexion()

        sql = "SELECT * FROM contrasena ORDER BY id ASC"

        datos = self.cursor.execute(sql)
        resultado = datos.fetchall()
        self.cerrar_conexion()

        return resultado
