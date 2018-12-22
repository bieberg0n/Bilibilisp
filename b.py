from functools import reduce


def log(*args):
    print(*args)


def cut(args):
    return reduce(lambda x, y: x - y, args)


def multiplication(args):
    return reduce(lambda x, y: x * y, args)


def division(args):
    return reduce(lambda x, y: x / y, args)


def is_num(a):
    nums = {str(i) for i in range(10)}
    for char in a:
        if char not in nums:
            return False
    else:
        return True


class BilibilispParser:
    def __init__(self):
        self.env = dict()
        self.current_exp = []
        self.stack = []
        self.char_list = []
        self.define_mode = False

    def is_var(self, a):
        return self.env.get(a) is not None

    def let(self, args):
        log('args:', args)
        k, v = args
        self.env[k] = v

    def to_type(self, a):
        if self.is_var(a):
            return self.env[a]
        elif a == '+':
            return sum
        elif a == '-':
            return cut
        elif a == '*':
            return multiplication
        elif a == '/':
            return division
        elif a == 'let':
            return self.let
        elif is_num(a):
            return int(a)
        else:
            return a

    def parse_exp(self):
        exp = self.current_exp
        log('current exp:', self.current_exp)
        self.current_exp = []
        if len(exp) == 1:
            return exp[0]
        else:
            return exp[0](exp[1:])

    def deal_char_list(self):
        if self.char_list:
            obj = self.to_type(''.join(self.char_list))
            self.char_list = []
            self.current_exp.append(obj)

    def parse_char(self, char):
        if char == '(':
            if self.current_exp and self.current_exp[0].__name__ == 'let':
                self.define_mode = True
            else:
                self.stack.append(self.current_exp[:])
                self.current_exp = []

        elif char == ')':
            self.deal_char_list()
            result = self.parse_exp()
            if self.define_mode:
                self.define_mode = False
            else:
                self.current_exp = self.stack.pop()
                self.current_exp.append(result)

        elif char == ' ':
            self.deal_char_list()

        else:
            self.char_list.append(char)

    def parse(self, exp_str):
        [self.parse_char(char) for char in exp_str if char not in ('\r', '\n')]
        self.deal_char_list()
        return self.parse_exp()


def test():
    parser = BilibilispParser()
    assert(parser.parse('15') == 15)
    assert(parser.parse('(+ 11 2)') == 13)
    assert(parser.parse('''(+ 11
  2)''') == 13)
    assert(parser.parse('+ 1 2 (* 3 4)') == 15)
    assert(parser.parse('- 4 1 2') == 1)

    exp = '''
(let (a 2)
  (let (b 3)
    (* a b)
  )
)
'''
    log(parser.parse(exp))


test()
