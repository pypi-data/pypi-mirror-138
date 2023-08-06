move_jismeshcode
================

与えられた地域メッシュコードを(x, y)動かした時のメッシュコードを返す

install
=======

::

   pip install move_jismeshcode

Usage
=====

::

   import move_jismeshcode as mj

   # 与えれたメッシュコードを (5, 3) 動かした時のメッシュコードを返す
   newmeshcode = mj.move(5438234312, 5, 3)
   print(newmeshcode)
   5438235342

   # メッシュコード(5438235342) - メッシュコード(5438234312) の座標を返す
   x, y = mj.sub(5438235342, 5438234312)
   print(x, y)
   5, 3

Todo
====

-  ☐ 定義外のメッシュコードのときに例外を返す

Reference
=========

-  `第１章
   地域メッシュ統計の特質・沿革 <http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf>`__
