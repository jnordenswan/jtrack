#!/bin/bash
python -ic "from lib import model as m; m.connect_db('data/johan.db'); from lib import util as u; from lib import view as v"
