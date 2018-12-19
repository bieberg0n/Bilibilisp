from functools import reduce


def log(*args):
    print(*args)


def cut(args):
    return reduce(lambda x, y: x - y, args)


def multiplication(args):
    return reduce(lambda x, y: x * y, args)


def division(args):
    return reduce(lambda x, y: x / y, args)


def to_type(a):
    if a == '+':
        return sum
    elif a == '-':
        return cut
    elif a == '*':
        return multiplication
    elif a == '/':
        return division
    elif a in [str(i) for i in range(10)]:
        return int(a)


def parse_exp(exp):
    log('exp:', exp)
    if len(exp) == 1:
        return exp[0]
    else:
        return exp[0](exp[1:])


def _parse(exps, exp_list, char_list):
    try:
        char = next(exps)
    except StopIteration:
        if len(char_list) == 1:
            exp_list.append(to_type(''.join(char_list)))
        return parse_exp(exp_list)

    if char == '(':
        exp_in = _parse(exps, [], [])
        log(exp_in)
        exp_list.append(exp_in)
        return _parse(exps, exp_list, [])

    elif char == ')':
        exp_list.append(to_type(''.join(char_list)))
        return parse_exp(exp_list)

    elif char == ' ':
        exp_list.append(to_type(''.join(char_list)))
        return _parse(exps, exp_list, [])

    else:
        char_list.append(char)
        return _parse(exps, exp_list, char_list)


def parse(exp_str):
    exps = iter(list(exp_str))
    return _parse(exps, [], [])


log(parse('5'))
log(parse('(+ 1 2)'))
log(parse('+ 1 2 (* 3 4)'))
log(parse('- 4 1 2'))