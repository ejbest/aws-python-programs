#!/bin/bash
set +x
rm -Rf foo2
echo "aws iam list-attached-role-policies --role-name ej_lambda > foo2"
aws iam list-attached-role-policies --role-name ej_lambda > foo2
myarn=` cat foo2 | grep 'Arn' |cut -d'|' -f4  | tr -d ' '` && echo "myarn...$myarn..."
echo "aws iam detach-role-policy --role-name ej_lambda --policy-arn $myarn"
aws iam detach-role-policy --role-name ej_lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
echo "aws iam delete-role --role-name ej_lambda"        
aws iam delete-role --role-name ej_lambda        
echo "aws lambda delete-function --function-name ej_lambda" 
aws lambda delete-function --function-name ej_lambda 
echo "aws events delete-rule --name "event5""
aws events delete-rule --name "event5"
