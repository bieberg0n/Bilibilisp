# Bilibilisp

Python实现的LISP子集.

---

## Usage
```
>>> from b import BilibilispParser
>>> pr = BilibilispParser()
>>> exp = '(* 3 (+ 4 5))'
>>> pr.parse(exp)
27
>>> exp = '(var a 9 (* a a))'
>>> pr.parse(exp)
81
>>> exp = '((lambda x (* x 3)) 2)'
>>> pr.parse(exp)
6
>>> exp = '(var y 4 ((lambda x (* x y)) 2))'
>>> pr.parse(exp)
8
```

更多用例见[test.py](test.py).

## Reference
[怎样写一个解释器](https://www.yinwang.org/blog-cn/2012/08/01/interpreter) by 王垠
