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
        parser.env[self.key] = value
        for o in self.exp:
            if isinstance(o, str):
                parser.exp.append(parser.to_type(o))
            else:
                parser.exp.append(o)
        log('lambda run, exp:', parser.exp, 'env stack:', parser.env_stack)
        result = parser.parse_exp()
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
        self.mode = ['', 0]
        self.current_lambda = None

    def push_mode(self):
        if self.mode[0]:
            self.mode_stack.append(self.mode)

    def enable_define_mode(self):
        self.push_mode()
        self.mode = ['define', 1]

    def enable_lambda_mode(self):
        self.push_mode()
        self.mode = ['lambda', 2]

    def disable_mode(self):
        name, lv = self.mode
        if lv >= 1:
            self.mode[1] -= 1
        elif len(self.mode_stack) > 0:
            self.mode = self.mode_stack.pop()
        else:
            self.mode = ['', 0]

    def get_val(self, a):
        current = self.env.get(a)
        if current is not None:
            return current, True
        else:
            for env in reversed(self.env_stack):
                value = env.get(a)
                if value:
                    return value, True
            else:
                return None, False

    def var(self, args):
        log('args:', args)
        k, v = args
        self.env[k] = v
        log('env:', self.env, self.env_stack)

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
            self.current_lambda = Closure(self.env_stack)
            return self.current_lambda
        elif is_num(a):
            return int(a)
        else:
            return a

    def parse_exp(self):
        exp = self.exp
        log('current exp:', self.exp)
        self.exp = []
        if len(exp) == 1:
            return exp[0]

        elif isinstance(exp[0], Closure):
            return exp[0].parse(exp[1])

        else:
            return exp[0](exp[1:])

    def deal_char_list(self):
        if self.char_list:
            word = ''.join(self.char_list)
            mode, lv = self.mode
            if mode == 'define' and lv == 1:
                obj = word
                self.disable_mode()
            else:
                obj = self.to_type(word)
            self.exp.append(obj)
            self.char_list = []
            log('current exp add obj:', obj)

    def parse_char(self, char):
        mode_name, lv = self.mode
        if char == '(':
            log('(mode:', mode_name, 'mode stack:', self.mode_stack, 'mode lv:', lv)
            if self.mode[0] == 'lambda':
                return
            else:
                self.stack.append(self.exp)
                log('push stack:', self.stack)
                self.exp = []
                self.env_stack.append(self.env)
                self.env = dict()

        elif char == ')':
            log(')mode:', mode_name, 'mode stack:', self.mode_stack, 'mode lv:', lv)
            self.deal_char_list()
            if mode_name == 'define':
                log('exp stack:', self.stack)
                self.parse_exp()
                self.disable_mode()

            elif mode_name == 'lambda' and lv == 2:
                self.current_lambda.key = self.exp.pop()
                log('lambda add key:', self.current_lambda.key)
                self.exp = []
                self.disable_mode()

            elif mode_name == 'lambda' and lv == 1:
                self.current_lambda.exp = self.exp
                log('lambda add exp:', self.exp)
                self.disable_mode()

            elif mode_name == 'lambda' and lv == 0:
                self.exp = self.stack.pop()
                self.exp.append(self.current_lambda)
                self.disable_mode()

            else:
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
