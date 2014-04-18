#!/usr/bin/env python3
# @author: Danilo J. S. Bellini

op = {
  "+": lambda a, b: a + b,
  "-": lambda a, b: a - b,
  "*": lambda a, b: a * b,
}

class MeuDicionário(dict):
  def __missing__(self, chave):
    if chave[0] in op:
      b = int(chave[1:])
      func = op[chave[0]]
      resultado = lambda a: func(a, b)
    else:
      a = int(chave[:-1])
      func = op[chave[-1]]
      resultado = lambda b: func(a, b)
    self[chave] = resultado
    return resultado

estratégias = MeuDicionário()

for símbolo in ["+2", "5-", "-3", "4*", "+2"]:
  função = estratégias[símbolo]
  print("2,  %s -> %d" % (símbolo, função(2)))
  print("-1, %s -> %d" % (símbolo, função(-1)))
  print("7,  %s -> %d" % (símbolo, função(7)))
