# -*- coding: utf-8 -*-
from typing import Tuple, Union, List
from move_jismeshcode.move import _listDigit, _move

def sub(minuend: Union[int, str], subtrahend: Union[int, str]) -> Tuple[int, int]:
    if len(str(minuend)) != len(str(subtrahend)):
        raise ValueError('length of minuend and subtrahend must be equal')

    x, y = 0, 0
    if minuend == subtrahend:
        return x, y

    lsMinuend = _listDigit(minuend)
    lsSubtrahend = _listDigit(subtrahend)

    signX = _extractX(lsMinuend) > _extractX(lsSubtrahend)
    walkX = -1 if signX else 1

    while True:
      if _equalX(lsMinuend, lsSubtrahend):
        break
      lsMinuend = _move(lsMinuend, walkX, 0)
      x -= walkX

    signY = _extractY(lsMinuend) > _extractY(lsSubtrahend)
    walkY = -1 if signY else 1

    while True:
      if _equalY(lsMinuend, lsSubtrahend):
        break
      lsMinuend = _move(lsMinuend, 0, walkY)
      y -= walkY
    
    return x, y

def _equalX(ls1: List[int], ls2: List[int]) -> bool:
    flg = True
    for i in range(0, len(ls1)):
      if i >= 8:
        flg &= _equalXBelow9(ls1[i], ls2[i])
      elif i in [2,3,5,7]:
        flg &= ls1[i] == ls2[i]
    return flg

def _equalY(ls1: List[int], ls2: List[int]) -> bool:
    flg = True
    for i in range(0, len(ls1)):
      if i >= 8:
        flg &= _equalYBelow9(ls1[i], ls2[i])
      elif i in [0,1,4,6]:
        flg &= ls1[i] == ls2[i]
    return flg

def _equalXBelow9(a :int, b :int) -> bool:
    return int(a % 2) == int(b % 2)

def _equalYBelow9(a :int, b :int) -> bool:
    _a = a - 1
    _b = b - 1
    return int(_a / 2) == int(_b / 2)

def _extractX(ls1: List[int]) -> int:
    x = ''
    for i in range(0, len(ls1)):
      if i >= 8:
        x += str(ls1[i])
      elif i in [2,3,5,7]:
        x += str(ls1[i])
    return int(x)

def _extractY(ls1: List[int]) -> int:
    x = ''
    for i in range(0, len(ls1)):
      if i >= 8:
        x += str(ls1[i])
      elif i in [0,1,4,6]:
        x += str(ls1[i])
    return int(x)
