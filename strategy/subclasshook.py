#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod

class Estratégia(metaclass=ABCMeta):
    @abstractmethod
    def executar(self, a, b):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        return any("executar" in vars(B) for B in C.mro()) or NotImplemented

class Soma:
    def executar(self, a, b):
        return a + b

print(isinstance(Soma(), Estratégia)) # True
print(issubclass(Soma, Estratégia)) # True
