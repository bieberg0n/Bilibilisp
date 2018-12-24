from b import BilibilispParser
from utils import log


def test1():
    parser = BilibilispParser()
    assert(parser.parse('15') == 15)


def test2():
    parser = BilibilispParser()
    assert(parser.parse('(+ 11 2)') == 13)


def test3():
    parser = BilibilispParser()
    assert(parser.parse('''(+ 11
 2)''') == 13)


def test4():
    parser = BilibilispParser()
    assert(parser.parse('+ 1 2 (* 3 4)') == 15)


def test5():
    parser = BilibilispParser()
    assert(parser.parse('- 4 1 2') == 1)


def test6():
    parser = BilibilispParser()
    exp = '''
(var a (+ 2 1)
  (* a 3))
'''
    assert(parser.parse(exp) == 9)

    parser = BilibilispParser()
    exp = '''
(var a 2
  (var b 3
    (var c 4
      (* a b c))))
'''
    assert(parser.parse(exp) == 24)


def test7():
    parser = BilibilispParser()
    exp = '''((lambda x (* x 3)) 2)'''
    assert(parser.parse(exp) == 6)


def test8():
    parser = BilibilispParser()
    exp = '''
(var y 3
  ((lambda (x) (* x y)) 2))
'''
    assert(parser.parse(exp) == 6)


def test9():
    parser = BilibilispParser()
    exp = '''
(var f (lambda (x) (* x 3))
  (f 4))
'''
    assert(parser.parse(exp) == 12)


def test10():
    parser = BilibilispParser()
    exp = '''
(var m 2
  (var f (lambda (n) (* m n))
    (var m 4
      (f 3))))
'''
    assert(parser.parse(exp) == 6)


def test11():
    parser = BilibilispParser()
    exp = '''
(var f (lambda (x) (var y 1 (+ x y)))
  (f 2))
'''
    assert(parser.parse(exp) == 3)


def test():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()


test()
