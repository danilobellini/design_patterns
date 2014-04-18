#!/usr/bin/env python3
# @author: Danilo J. S. Bellini
from operator import itemgetter
from audiolazy import StrategyDict

sort = StrategyDict("sort")

@sort.strategy("slow", "bad") # Slow sorting by getting min value
def sort(data):
  for idx, el in enumerate(data):
    idx_min, el_min = min(enumerate(data[idx:], idx), key=itemgetter(1))
    data[idx], data[idx_min] = el_min, el

@sort.strategy("bubble") # Alone bubble sort
def sort(data):
  idx = 1
  while idx < len(data):
    if data[idx - 1] > data[idx]:
      data[idx - 1], data[idx] = data[idx], data[idx - 1]
      idx = max(1, idx - 1)
    else:
      idx += 1

@sort.strategy("merge") # Merge sort
def sort(data):
  def recursive_merge(blk):
    size = len(blk)
    if size <= 1:
      return blk
    half = size // 2
    first = recursive_merge(blk[:half])
    second = recursive_merge(blk[half:])
    result = []
    while first and second:
      part_idx = max((second[-1], 0), (first[-1], 1))[1]
      result.append([second, first][part_idx].pop())
    return first + second + result[::-1]
  data[:] = recursive_merge(data)

if __name__ == "__main__":
  from random import shuffle
  data = list(range(30))

  print(sort.default.__name__) # slow (primeira)
  print()
  print(sort.bubble is sort["bubble"]) # True
  print()
  print(sort) # As 3 estratégias

  for st in sort:
    print()
    shuffle(data)
    print(data) # Scrambled
    st(data)
    print(data) # [0, 1, 2, ...]
