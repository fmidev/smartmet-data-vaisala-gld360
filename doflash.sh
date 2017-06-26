#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2016)
#
# SmartMet Data Ingestion Module for Vaisala GLD360
#

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/vaisala-gld360
OUT=$BASE/data/vaisala-gld360/world/lightning/querydata/
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/vaisala-gld360
TIMESTAMP=`date +%Y%m%d%H%M`
OUTFILE=$TMP/${TIMESTAMP}_gld360_world_lightning.sqd
TMPFILE=$TMP/vaisala-gld360-$$.txt

mkdir -p $TMP
mkdir -p $OUT

echo "IN:  $IN" 
echo "OUT: $OUT" 
echo "TMP: $TMP" 
echo "TMP File: $TMPFILE"
echo "OUT File: $OUTFILE"

# Do SYNOP stations
cat $IN/*.dat > $TMPFILE
flash2qd $TMPFILE > $OUTFILE
rm -rf $TMPFILE

if [ -s $OUTFILE ]; then
    bzip2 -k $OUTFILE
    mv -f $OUTFILE $OUT
    mv -f ${OUTFILE}.bz2 $EDITOR
fi

rm -f $TMP/*.sqd*
