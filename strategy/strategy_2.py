#!/usr/bin/env python3

def soma(a, b):
    return a + b
def subtração(a, b):
    return a - b
def multiplicação(a, b):
    return a * b

class Contexto:
    def __init__(self, estratégia, símbolo):
        self.estratégia = estratégia
        self.símbolo = símbolo

    def tarefa(self, a, b):
        resultado = self.estratégia(a, b)
        args = (a, self.símbolo, b, resultado)
        print("{} {} {} = {}".format(*args))

if __name__ == "__main__":
    Contexto(soma, "+").tarefa(22, 3)

    ctx = Contexto(subtração, "-")
    ctx.tarefa(22, 3)

    ctx.estratégia = multiplicação
    ctx.símbolo = "*"
    ctx.tarefa(22, 3)