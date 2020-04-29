#!/bin/bash

echo "Working diretory: $PWD"
MESSAGE=${1:-No message}
MAXSLEEP=${2:-15}
x=1
while [ $x -le $MAXSLEEP ]
do
  echo "$MESSAGE: Sleep cycle no. $x"
  x=$(( $x + 1 ))
  sleep 1
done
