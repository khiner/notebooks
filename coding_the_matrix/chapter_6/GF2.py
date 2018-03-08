# Copyright 2013 Philip N. Klein
from numbers import Number

class One:
    def __add__(self, other): return self if other == 0 else 0
    __sub__ = __add__
    def __mul__(self, other):
        if isinstance(other, Number):
            return 0 if other == 0 else self
        return other
    def __div__(self, other):
        if other == 0: raise ZeroDivisionError
        return self
    __truediv__ = __div__
    def __rdiv__(self,other): return other
    __rtruediv__ = __rdiv__
    __radd__ = __add__
    __rsub__ = __add__
    __rmul__ = __mul__
    #hack to ensure not (one < 1e-16) by ensuring not (one < x) for every x
    def __lt__(self,other): return False
    def __eq__(self, other):
        if isinstance(other, self.__class__) or other==0:
            return other != 0
        else:
            raise TypeError
    def __hash__(self): return 1
    def __str__(self): return 'one'
    __repr__ = __str__
    def __neg__(self): return self
    def __bool__(self): return True
    def __format__(self, format_spec): return format(str(self),format_spec)

one = One()
zero = 0
