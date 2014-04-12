import os
from lib import model, util

try:
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    columns = int(columns)
except Exception:
    rows = 100
    columns = 80


def print_subtree(nodelist, depth=1):
    indent = 2 * (depth - 1)
    header = "%s%s-%s: %s"
    for e in nodelist:
        if e.ntype in "PSR":
            first_comment = e.get_first_comment()
            name = util.int_to_str(e.name).zfill(3)
            print(header % (indent*" ", e.ntype, name, e.data))
            if first_comment:
                print(("%s" + first_comment) % (indent*" ",))
        print_subtree(e.get_children(), depth+1)


def print_agenda(nodelist, start_date, end_date=None):
    start_secs = util.secify(start_date)
    if end_date:
        end_secs = util.secify(end_date)
    else:
        end_secs = start_secs + 86400
    filtered = []
    for n in nodelist:
