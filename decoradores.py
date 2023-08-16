def decorador_alta(f):
    def inner(*args):
        retorno = f(*args)
        print(retorno)
        log_deco = RegistroLogDecoradores(
            "Nueva Alta",
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
        log_deco = RegistroLogDecoradores(
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
        log_deco = RegistroLogDecoradores(
            "Registro Eliminado",
            "Id elimnado :" + str(retorno[0]),
            "",
            "",
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner
