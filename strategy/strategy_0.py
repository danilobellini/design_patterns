#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod

class Estratégia(metaclass=ABCMeta):
    @abstractmethod
    def executar(self, a, b):
        pass

class Soma(Estratégia):
    def executar(self, a, b):
        return a + b
class Subtração(Estratégia):
    def executar(self, a, b):
        return a - b
class Multiplicação(Estratégia):
    def executar(self, a, b):
        return a * b

class Contexto:
    def __init__(self, estratégia, símbolo):
        self.estratégia = estratégia
        self.símbolo = símbolo

    def tarefa(self, a, b):
        resultado = self.estratégia.executar(a, b)
        args = (a, self.símbolo, b, resultado)
        print("{} {} {} = {}".format(*args))

if __name__ == "__main__":
    Contexto(Soma(), "+").tarefa(22, 3)

    ctx = Contexto(Subtração(), "-")
    ctx.tarefa(22, 3)

    ctx.estratégia = Multiplicação()
    ctx.símbolo = "*"
    ctx.tarefa(22, 3)
