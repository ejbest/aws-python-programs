#!/bin/bash
set +x
rm -Rf ej_lambda.zip
rm -Rf foo
echo "******************************************"
echo "*** iam role ej_lambda  ******************"
echo "******************************************"
echo "aws iam create-role --role-name ej_lambda --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' "
aws iam create-role --role-name ej_lambda --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' > foo
set +x
myarn=`cat foo|perl -lne 'print if s/\|\|\s+(Arn)\s+\|(.*)\|\|/\2/' |tr -d ' '` && echo "myarn....$myarn..."
#arn="arn:aws:iam::362863965643:role/ej_lambda"
echo "******************************************"
echo "myarn.....$myarn....."
#echo "arn.......$arn....."
echo "******************************************"
echo "*** iam policy ***************************"
echo "******************************************"
echo "aws iam attach-role-policy --role-name ej_lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
aws iam attach-role-policy --role-name ej_lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
sleep 10
echo "******************************************"
echo "******************************************"
echo "******************************************"
zip ej_lambda.zip ej_lambda.py
echo "******************************************"
echo "******************************************"
echo "******************************************"
echo "aws lambda create-function --function-name ej_lambda --runtime python3.8 --zip-file fileb://ej_lambda.zip --handler ej_lambda.handler --role $myarn" 
aws lambda create-function --function-name ej_lambda --runtime python3.8 --zip-file fileb://ej_lambda.zip --handler ej_lambda.ej_lambda --role $myarn
echo "******************************************"
echo "*** invoke lambda to run python **********"
echo "******************************************"
aws lambda invoke --function-name ej_lambda response.json
echo "******************************************"
echo "*** event in cloudwatch ******************"
echo "******************************************"
# #create cloudwatch rule
aws events put-rule \
    --name event5 \
    --schedule-expression 'cron(04 01 * * ? *)'
echo "******************************************"
echo "*** permission in lambda *****************"
echo "******************************************"
aws lambda add-permission \
    --function-name ej_lambda \
    --statement-id event5 \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:us-east-1:362863965643:rule/event5

