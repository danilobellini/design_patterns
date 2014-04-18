#!/usr/bin/env python3

strategies = {
  "+": lambda a, b: a + b,
  "-": lambda a, b: a - b,
  "*": lambda a, b: a * b,
}

for key, value in strategies.items():
  print("2 %c 3 = %d" % (key, value(2, 3)))
  print("7 %c 5 = %d" % (key, value(7, 5)))
