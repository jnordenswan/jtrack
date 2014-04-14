#!/bin/bash
python -ic "

from lib import controller as c
from sqlite3 import connect
c.conn = connect('data/johan.db')

"
