#!/bin/bash
set -x
echo mystr=`grep "arn:aws" foo` 
echo "mystr....$mystr"
echo myarn=`echo $mystr | cut -d ":" -f 2-6 | cut -d " " -f 1`
echo "mymid.....$mymid"
myarn=`echo $mymid` | echo $myarn 
echo "mystr.....$mystr"
echo "mymid.....$mymid"
echo "myarn.....$myarn"
