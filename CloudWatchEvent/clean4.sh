#!/bin/bash
set -x
rm -Rf foo
aws iam list-attached-role-policies --role-name lambda-pol > foo
set +x
mystr="`grep "arn:aws" foo`"
mymid=`echo $mystr | cut -d ":" -f 2-6 | cut -d " " -f 1`
myarn=`echo $mymid`
echo "mystr.....$mystr"
echo "mymid.....$mymid"
echo "myarn.....$myarn"
aws iam detach-role-policy --role-name lambda-pol --policy-arn $myarn
aws iam delete-role --role-name lambda-pol        
aws lambda delete-function --function-name myfunction 