#!/bin/bash
set -x
rm -Rf foo
#create everything now 
aws iam create-role --role-name lambda-pol --assume-role-policy-document file://trust-policy.json > foo
set +x
mystr="`grep "arn:aws" foo`"
mymid=`echo $mystr | cut -d ":" -f 2-6 | cut -d " " -f 1`
myarn=`echo $mymid`
echo "mystr.....$mystr"
echo "mymid.....$mymid"
echo "myarn.....$myarn"
aws iam attach-role-policy --role-name lambda-pol --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
zip script.zip myfunction.py
echo "******************************************"
echo "******************************************"
echo "******************************************"
aws lambda create-function --function-name myfunction --zip-file fileb://script.zip --handler myfunction --runtime python3.8 --role $myarn
echo "******************************************"
echo "******************************************"
echo "******************************************"
echo "******************************************"
# #create cloudwatch rule
# aws events put-rule \
#     --name event5 \
#     --schedule-expression 'cron(04 01 * * ? *)'

# aws lambda add-permission \
#     --function-name myfunction \
#     --statement-id event5 \
#     --action 'lambda:InvokeFunction' \
#     --principal events.amazonaws.com \
#     --source-arn arn:aws:events:us-east-1:362863965643:rule/event5

# aws events put-targets --rule event5 --targets file://target.json

# ===================================================================
# First run
# #aws iam create-role --role-name lambda-pol --assume-role-policy-document file://trust-policy.json
# It will present you a ARN like this:
# "Arn": "arn:aws:iam::214639533279:role/CreateRole",
# Now run
# aws iam attach-role-policy --role-name lambda-pol --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
# zip script.zip myfunction.py
# aws lambda create-function --function-name myfunction \
# --zip-file fileb://script.zip --handler myfunction.myfunction --runtime python3.8 \
# --role arn:aws:iam::214639533279:role/lambda-pol

# aws events put-rule \
# --name my-weekly-event \
# --schedule-expression 'cron(0 9 * * ? *)'

# aws lambda add-permission \
# --function-name myfunction \
# --statement-id my-weekly-event \
# --action 'lambda:InvokeFunction' \
# --principal events.amazonaws.com \
# --source-arn arn:aws:events:us-west-2:214639533279:rule/my-weekly-event

# aws events put-targets --rule event1 --targets file://target.json
# i changed line 9