#!/bin/bash
python -ic "from lib import model, view, controller
c = controller.Controller('data/johan.db')"
