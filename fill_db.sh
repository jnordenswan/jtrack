#!/bin/bash
rm -rfv data/johan.db &&
sqlite3 data/johan.db < dbdump.sql &&
echo \'data/johan.db\' reinitialized with 'dbdump' ||
echo Something went wrong :\(
