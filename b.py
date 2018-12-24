from functools import reduce
from utils import log


def parse_args(args):
    result = []
    for arg in args:
        if isinstance(arg, tuple):
            result.append(arg[1])
        else:
            result.append(arg)
    return result


def reduce_args(func, args):
    args = parse_args(args)
    return reduce(func, args)


def sum(args):
    return reduce_args(lambda x, y: x + y, args)


def cut(args):
    return reduce_args(lambda x, y: x - y, args)


def multiplication(args):
    return reduce_args(lambda x, y: x * y, args)


def division(args):
    return reduce_args(lambda x, y: x / y, args)


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
        parser.env[self.key] = value
        exp_str = ''.join(self.exp)
        log('lambda run, parser env:', parser.env)
        result = parser.parse(exp_str)
        log('lambda result:', result)
        return result


class BilibilispParser:
    def __init__(self):
        self.env_stack = []
        self.env = dict()

        self.exp = []
        self.stack = []
        self.char_list = []

        self.mode_stack = []
        self.mode = ''
        self.current_lambda = None
        self.lambda_stack_deep = 0

    def push_mode(self):
        if self.mode:
            self.mode_stack.append(self.mode)

    def enable_define_mode(self):
        self.push_mode()
        self.mode = 'define'

    def enable_lambda_mode(self):
        self.push_mode()
        self.mode = 'lambda'

    def disable_mode(self):
        if len(self.mode_stack) > 0:
            self.mode = self.mode_stack.pop()
        else:
            self.mode = ''

    def get_val(self, a):
        env_stack_copy = self.env_stack[:]
        env_stack_copy.append(self.env)
        for env in reversed(env_stack_copy):
            value = env.get(a)
            if value:
                return (a, value), True
        else:
            return None, False

    def var(self, args):
        log('args:', args)
        k, v = args
        key_name, _ = k
        self.env[key_name] = v

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
        elif a == 'var':
            self.enable_define_mode()
            return self.var
        elif a == 'lambda':
            self.enable_lambda_mode()
            self.current_lambda = Closure(self.env_stack[:])
            return self.current_lambda
        elif is_num(a):
            return int(a)
        else:
            return (a, a)

    def run_exp(self, op, args):
        if len(args) == 0:
            return op

        elif isinstance(op, Closure):
            log('lambda exp:', op.exp, 'args:', args)
            return op.parse(*args)

        elif isinstance(op, tuple):
            op = op[1]
            return self.run_exp(op, args)

        else:
            return op(args)

    def parse_exp(self):
        log('current exp:', self.exp)
        exp = self.exp
        self.exp = []
        op, *args = exp
        return self.run_exp(op, args)

    def deal_char_list(self):
        if self.char_list:
            word = ''.join(self.char_list)
            obj = self.to_type(word)
            self.exp.append(obj)
            self.char_list = []
            log('current exp add obj:', obj)

    def lambda_parse_char(self, char):
        self.current_lambda.exp.append(char)
        if char == '(':
            self.lambda_stack_deep += 1

        elif char == ')':
            if self.lambda_stack_deep == 1:
                self.disable_mode()
                self.exp = [self.current_lambda]
            else:
                self.lambda_stack_deep -= 1

    def parse_char(self, char):
        if self.mode == 'lambda' and self.lambda_stack_deep > 0:
            return self.lambda_parse_char(char)

        elif char == '(':
            log('(mode:', self.mode, 'mode stack:', self.mode_stack)
            if self.mode == 'define' and len(self.exp) == 3:
                log('exp stack:', self.stack)
                self.parse_exp()
                self.disable_mode()

            elif self.mode == 'lambda' and len(self.exp) == 2:
                self.current_lambda.key = self.exp[1][0]
                self.lambda_parse_char(char)
                log('lambda add key:', self.exp[1])
                return

            log('(push stack:', self.stack)
            self.stack.append(self.exp)
            self.exp = []
            self.env_stack.append(self.env)
            self.env = dict()

        elif char == ')':
            log(')mode:', self.mode, 'mode stack:', self.mode_stack)
            self.deal_char_list()
            log('parse exp:', self.exp)
            result = self.parse_exp()
            self.exp = self.stack.pop()
            self.exp.append(result)

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
        result = self.parse_exp()
        self.disable_mode()
        return result
