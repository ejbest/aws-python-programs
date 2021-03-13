import boto3

s3 = boto3.client("s3")

buckets = {}
for bucket in s3.list_buckets()["Buckets"]:
    buckets[bucket["Name"]]= s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']

regions = set(buckets.values())
print("number of regions:", len(regions))


regions = {}
for bucket, region in buckets.items():
	if not regions.get(region):
		regions[region] = []
	regions[region].append(bucket)

print("available regions:")
for region in regions:
	print(region)

print("available buckets:")
for region in regions:
	print(region,':')
	for bucket in regions[region]:
		print('---------------', bucket)
