import boto3
#########################################################################################
# aws-list-s3.py                                                                        #
#                                                                                       #
#  Function......List s3 buckets indivdually and list regions beside eash               #
#  Requires......https://aws.amazon.com/sdk-for-python/                                 #
#  Released......March 11, 2021                                                         #
#  Scripter......                                                                       #
#  Invoke........python3 aws-list-s3.py                                                 #
#                                                                                       #
#########################################################################################



class myList:
    def GetRegions(self):
        RegionList = []
        region=boto3.client('ec2')
        Response=region.describe_regions()
        for RegionCount in range(len(Response['Regions'])):
            RegionList.append(Response['Regions'][RegionCount]['RegionName'])
        print("Number of Regions {}".format(len(RegionList)))
        print("Regions::")
        print (RegionList)
        print("**********************************")
        return RegionList

    def ListEc2Instance(self):
        FetchRegionList = self.GetRegions()

        s3 = boto3.client('s3')
        s3_resp = s3.list_buckets()
        ExceptList = []
        regional_buckets = { each : [] for each in FetchRegionList}
        for idx,bucket in enumerate(s3_resp["Buckets"]):
            try:
                loc = s3.head_bucket(Bucket=bucket['Name'])['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']
                regional_buckets[loc].append(bucket)
            except Exception as e:
                ExceptList.append(bucket["Name"])
        for key, val in regional_buckets.items():
            print("Region: {}".format(key))
            for each in val:
                print("S3 Bucket --> Name: {}  CreationDate :{}  Ownerid : {}".format(each['Name'],each['CreationDate'],s3_resp['Owner']['ID']))
            print("--------------------------------------------------------------------")
        if (len(ExceptList)):
            print("Following bucket region couldnt be extracted :")
            for each in ExceptList:
                print("S3 Bucket --> Name: {}",format(each))


if __name__ == '__main__':
    RunQuery = myList()
    RunQuery.ListEc2Instance()

