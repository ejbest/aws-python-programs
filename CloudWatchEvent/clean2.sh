#!/bin/bash
set -x
# How to clean up the mess 
aws iam list-attached-role-policies --role-name lambda-pol > foo
mystr=$(grep """arn:aws""" foo) | echo $mystr
echo "mystr.....$mystr"
mymid="""""$(echo $mystr | awk -F '|' '{print $4}')"""""
echo $mymid
# myarn=`echo $mymid` | echo $myarn 
# echo "mystr.....$mystr"
# echo "mymid.....$mymid"
# echo "myarn.....$myarn"
# aws lambda delete-function --function-name myfunction 