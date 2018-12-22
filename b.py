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


class Closure:
    def __init__(self, env_stack):
        self.env_stack = env_stack
        self.key = ''
        self.exp = []

    def parse(self, value):
        parser = BilibilispParser()
        parser.env_stack = self.env_stack
        parser.current_env[self.key] = value
        for o in self.exp:
            if isinstance(o, str):
                parser.current_exp.append(parser.to_type(o))
            else:
                parser.current_exp.append(o)
        log('lambda run, exp:', parser.current_exp, 'env stack:', parser.env_stack)
        result = parser.parse_exp()
        log('lambda result:', result)
        return result


class BilibilispParser:
    def __init__(self):
        self.env_stack = []
        self.current_env = dict()
        self.current_exp = []
        self.stack = []
        self.char_list = []
        self.define_mode = False

        self.lambda_mode = 0
        self.current_lambda = None

    def get_val(self, a):
        current = self.current_env.get(a)
        if current is not None:
            return current, True
        else:
            for env in reversed(self.env_stack):
                value = env.get(a)
                if value:
                    return value, True
            else:
                return None, False

    def let(self, args):
        log('args:', args)
        k, v = args
        self.current_env[k] = v

    def to_type(self, a):
        value, ok = self.get_val(a)
        if ok:
            return value
        elif a == '+':
            return sum
        elif a == '-':
            return cut
        elif a == '*':
            return multiplication
        elif a == '/':
            return division
        elif a == 'let':
            self.define_mode = True
            return self.let
        elif a == 'lambda':
            self.current_lambda = Closure(self.env_stack)
            self.lambda_mode = 2
            return self.current_lambda
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

        elif isinstance(exp[0], Closure):
            return exp[0].parse(exp[1])

        else:
            return exp[0](exp[1:])

    def deal_char_list(self):
        if self.char_list:
            obj = self.to_type(''.join(self.char_list))
            self.char_list = []
            self.current_exp.append(obj)
            log('current exp add obj:', obj)

    def current_exp_has_key(self, key):
        if self.current_exp:
            op = self.current_exp[0]
            if hasattr(op, '__call__') and op.__name__ == key:
                return True
            elif isinstance(op, Closure) and key == 'lambda':
                return True
        else:
            return False

    def parse_char(self, char):
        if char == '(':
            if self.current_exp_has_key('let') or self.current_exp_has_key('lambda'):
                return
            #     self.define_mode = True

            # elif self.current_exp_has_key('lambda'):
            #     self.current_lambda = Closure(self.env_stack)
            #     self.lambda_mode = 2

            else:
                self.stack.append(self.current_exp)
                self.current_exp = []
                self.env_stack.append(self.current_env)
                self.current_env = dict()

        elif char == ')':
            self.deal_char_list()
            if self.define_mode:
                self.parse_exp()
                self.define_mode = False

            elif self.lambda_mode == 2:
                self.current_lambda.key = self.current_exp.pop()
                self.current_exp = []
                self.lambda_mode -= 1

            elif self.lambda_mode == 1:
                self.current_lambda.exp = self.current_exp
                self.current_exp = [self.current_lambda]
                self.lambda_mode -= 1

            else:
                log('parse exp:', self.current_exp)
                result = self.parse_exp()
                self.current_exp = self.stack.pop()
                self.current_exp.append(result)

        elif char == ' ':
            self.deal_char_list()

        else:
            self.char_list.append(char)

    def parse(self, exp_str):
        log('exp:', exp_str)
        for char in exp_str:
            if char not in ('\r', '\n'):
                self.parse_char(char)

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
    (let (c 4)
      (* a b c)
    )
  )
)
'''
    assert(parser.parse(exp) == 24)

    exp = '''
(let (y 3)
     ((lambda (x) (* x y)) 2)
)
'''
    log(parser.parse(exp))


test()
