PYTHON=/usr/bin/python
LDIR=$PWD/logs
CDIR=$PWD

start() {
nohup $PYTHON $CDIR/catch_game_logs.py  > $LDIR/err.out 2>&1 &
}

#Main
start
