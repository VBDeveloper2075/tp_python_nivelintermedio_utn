import os
import datetime


class Registro_decoradores:
    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log_deco.txt")

    def __init__(self, aplicacionlog, usuariolog, contrasenalog, fechalog):
        self.aplicacionlog = aplicacionlog
        self.usuariolog = usuariolog
        self.contrasenalog = contrasenalog
        self.fechalog = fechalog

    def registrar_evento(self):
        log_deco = open(self.ruta, "a")
        print(
            "Se ha generado un cambio:",
            self.aplicacionlog,
            self.usuariolog,
            self.contrasenalog,
            file=log_deco,
        )


def decorador_alta(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = Registro_decoradores(
            "Aplicacion:" + retorno[0],
            "Usuario:" + retorno[1],
            "Contrasena:" + retorno[2],
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner


def decorador_editar(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = Registro_decoradores(
            "Registro Modificado",
            "Aplicacion:" + retorno[0],
            "Usuario:" + retorno[1],
            "Contrasena:" + retorno[2],
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner


def decorador_borrar(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = Registro_decoradores(
            "Registro Eliminado",
            "Id elimnado :" + str(retorno[0]),
            datetime.datetime.now(),
            "",
        )
        log_deco.registrar_evento()
        return retorno

    return inner
