import boto3

account_id = "XXXXXX"
region = 'eu-central-1'
job_name = 'test_macie'
s3 =  boto3.client('s3',region_name=region)
s3_resp = s3.list_buckets()
if len(s3_resp['Buckets']) != 0:
    s3_list = [each['Name'] for each in s3_resp['Buckets'] if s3.get_bucket_location(Bucket=each['Name'])['LocationConstraint'] == region]
    macie2 = boto3.client('macie2',region_name=region)
    response = macie2.create_classification_job(
        description='Test job',jobType='ONE_TIME',name=job_name,
        s3JobDefinition={'bucketDefinitions':[{'accountId':account_id,'buckets':s3_list}]})
