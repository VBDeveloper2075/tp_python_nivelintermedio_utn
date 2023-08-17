from datetime import datetime


class Sujeto:
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self, *args, **kwargs):
        for observador in self.observadores:
            observador.update(*args, **kwargs)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, *args, **kwargs):
        archivo = open("log_from_observerA.txt", "a")
        print(args)

        archivo.write(  # ACA PONES O QUE QUIERAAS QUE DIGA EL OBSERVADOR
            str(args[0]) + "  ,  " + str(args[1][1]) + "  ,  " + str(datetime.now())
        )
        archivo.close()
