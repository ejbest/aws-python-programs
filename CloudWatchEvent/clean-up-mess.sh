set -x
# How to clean up the mess 
aws iam list-attached-role-policies --role-name lambda-pol > foo
mystr="$(grep 'arn:aws' foo)" | echo $mystr
mymid=$(echo $x | awk -F '|' '{print $3}') | echo $mymid
myarn="$(tr -d $mymid)" | echo $myarn
aws iam detach-role-policy --role-name lambda-pol --policy-arn $myarn
aws iam delete-role --role-name lambda-pol        
aws lambda delete-function --function-name myfunction 