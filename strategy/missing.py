#!/usr/bin/env python3

class MeuDicionário(dict):
  def __missing__(self, chave):
    if chave.strip() != chave:
      valor = self[chave.strip()]
      self[chave] = valor
      return valor
    raise KeyError("Not Found")

estratégias = MeuDicionário([
  ("+", lambda a, b: a + b),
  ("-", lambda a, b: a - b),
  ("*", lambda a, b: a * b),
])

for símbolo in ["+", " +", " -  ", "\n* \n"]:
  função = estratégias[símbolo]
  print("2 %s 3 = %d" % (símbolo, função(2, 3)))
  print("7 %s 5 = %d" % (símbolo, função(7, 5)))

print(estratégias["/"])
