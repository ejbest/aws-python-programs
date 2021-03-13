import boto3
#########################################################################################
# aws-list-s3.py                                                                        #
#                                                                                       #
#  Function......List s3 buckets indivdually and list regions beside eash               #
#  Requires......https://aws.amazon.com/sdk-for-python/                                 #
#  Released......March 11, 2021                                                         #
#  Scripter......TBD                                                                    #
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
        FetchRegionList=[]
        FetchRegionList=self.GetRegions()
        for Region in range(len(FetchRegionList)):
            print ("Region : --> {}".format(FetchRegionList[Region]))
           
            # fetch all buckets
            s3 = boto3.client('s3', region_name=FetchRegionList[Region])
            s3_resp = s3.list_buckets()
            if len(s3_resp['Buckets'])!=0:
                for each in s3_resp['Buckets']:
                    print("S3 --> BucketName : {}. CreationDate: {}".format(each['Name'],each['CreationDate']))
            else:
                print("No S3 bucket present in this Region")
                

if __name__ == '__main__':
    RunQuery = myList()
    RunQuery.ListEc2Instance()
