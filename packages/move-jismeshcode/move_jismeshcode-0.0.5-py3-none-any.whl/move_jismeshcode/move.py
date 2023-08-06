# -*- coding: utf-8 -*-
from typing import List, Union

# 5次メッシュ(250m) を(x, y)移動させる
def move(meshCode: Union[int, str], x: int, y: int) -> int:
    ls = _listDigit(meshCode)
    ls = _move(ls, x, y)

    # 文字列に直す
    ret = ''
    for l in ls:
      ret += '{}'.format(l)

    return int(ret)

def _move(ls: List[int], x: int, y: int) -> List[int]:
    for i, l in enumerate(reversed(ls)):
      digit = len(ls) - i
      if digit >= 9: # 4次メッシュ以下(分割地域メッシュ)
        if x != 0:
          ls[digit-1], x = _moveXBelow9Iter(ls[digit-1], x)
        if y != 0:
          ls[digit-1], y = _moveYBelow9Iter(ls[digit-1], y)
      elif digit == 6: # 2次メッシュx
        if x != 0:
          ls[digit-1], x = _calcWithBase(ls[digit-1], x, 7)
      elif digit == 5: # 2次メッシュy
        if y != 0:
          ls[digit-1], y = _calcWithBase(ls[digit-1], y, 7)
      elif digit in [3,4,8]: #  1次メッシュ,3次メッシュX
        if x != 0:
          ls[digit-1], x = _calcWithBase(ls[digit-1], x)
      else: # [1,2,7] 1次メッシュ,3次メッシュY
        if y != 0:
          ls[digit-1], y = _calcWithBase(ls[digit-1], y)
    return ls

def _listDigit(meshCode: Union[int, str]) -> List[int]:
    ls = []
    meshCode = '{}'.format(meshCode)
    for ch in meshCode:
      ls.append(int(ch))
    return ls

def _moveXBelow9Iter(num, add=1):
  xkuriage = 0
  if add > 0:
    for i in range(add):
      num, b = _moveXBelow9(num)
      xkuriage += b
  else:
    for i in range(-add):
      num, b = _moveXBelow9(num, False)
      xkuriage += b
  return num, xkuriage, 

def _moveXBelow9(num, positive=True):
  if num % 2 == 0:
    if positive:
      return num - 1, 1 # 繰り上がり
    else:
      return num - 1, 0
  else:
    if positive:
      return num + 1, 0
    else:
      return num + 1, -1 # 繰り下がり

def _moveYBelow9Iter(num, add=1):
  ykuriage = 0
  if add > 0:
    for i in range(add):
      num, b = _moveYBelow9(num)
      ykuriage += b
  else:
    for i in range(-add):
      num, b = _moveYBelow9(num, False)
      ykuriage += b
  return num, ykuriage, 

def _moveYBelow9(num, positive=True):
  if num >= 3:
    if positive:
      return num - 2, 1 # 繰り上がり
    else:
      return num - 2, 0
  else:
    if positive:
      return num + 2, 0
    else:
      return num + 2, -1 # 繰り下がり

def _calcWithBase(num, add, base=10): # 3, -7 base=10
  num += add
  if num >= 0:
    return num % base, int(num / base)
  else:
    return num % base, int((num + 1) / base) - 1
