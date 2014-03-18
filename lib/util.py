from time import mktime, strptime, localtime, strftime


def datify(secs):
    struct = localtime(secs)
    return strftime("%y%m%d-%H%M", struct)


def secify(date):
    return int(mktime(strptime(str(date), "%y%m%d-%H%M")))


def spanify(secs):
    pass


def int_to_str(encodable, sym_set="0123456789abcdefghijklmnopqrstuvwxyz".upper()):
    sign = ''
    if encodable < 0: sign = '-'
    encodable = abs(encodable)
    l = len(sym_set)
    if encodable < l: return sign + sym_set[encodable]
    else:
        res = sign + int_to_str(encodable//l, sym_set)
        res = res + int_to_str(encodable % l, sym_set)
        return res


def str_to_int(decodable, sym_set="0123456789abcdefghijklmnopqrstuvwxyz"):
    decodable = decodable.lower()
    negative = False
    if decodable[0] == '-':
        negative = True
        decodable = decodable.lstrip('-')
    res = 0
    for i in range(len(decodable)):
        res += sym_set.index(decodable[len(decodable)-1-i])*len(sym_set)**i
    if negative: res = -res
    return res


