#!/bin/sh
/bin/sleep 3

loop_again=1


while (( loop_again )); do
    history | tail -2 | head -n 1 > geek.txt
   
    
done
