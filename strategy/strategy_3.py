#!/usr/bin/env python3
# @author: Danilo J. S. Bellini

from collections import namedtuple

Strategy = namedtuple("Strategy", ["func", "symbol"])

sum = lambda a, b: a + b
sub = lambda a, b: a - b
mul = lambda a, b: a * b

apply = lambda st, a, b: st.func(a, b)

strategies = [Strategy(sum, "+"), Strategy(sub, "-"), Strategy(mul, "*")]

for st in strategies:
  print("2 %c 3 = %d" % (st.symbol, apply(st, 2, 3)))
  print("7 %c 5 = %d" % (st.symbol, apply(st, 7, 5)))
