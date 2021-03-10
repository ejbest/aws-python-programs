import boto3
#########################################################################################
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html  #
#                                                                                       #
# aws-list-services                                                                     #
#                                                                                       #
# List Instances,LaodBalancer, Lambda Security Groups                                   #
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
            #Find all Ec2 instance in Region.
            Ec2 = boto3.client('ec2', region_name=FetchRegionList[Region])
            GetInstance = Ec2.describe_instances()
            if len(GetInstance['Reservations']) != 0:
                for InstanceCount in range(len(GetInstance['Reservations'])):
                    InstID=GetInstance['Reservations'][InstanceCount]['Instances'][0]['InstanceId']
                    InstType=GetInstance['Reservations'][InstanceCount]['Instances'][0]['InstanceType']
                    InstState=GetInstance['Reservations'][InstanceCount]['Instances'][0]['State']['Name']
                    print ("Instance --> id : {}. InstanceType: {}. Status : {}.".format(InstID,InstType,InstState))
            else:
                print ("No Instance(s) running in Region.")

            #Find all volumes used in Region:
            GetVolume = Ec2.describe_volumes()
            if len(GetVolume['Volumes']) !=0:
                for VolumeCount in range(len(GetVolume['Volumes'])):
                    GetVolumeID=GetVolume['Volumes'][VolumeCount]['VolumeId']
                    GetDiskState=GetVolume['Volumes'][VolumeCount]['State']
                    GetVolumeType=GetVolume['Volumes'][VolumeCount]['VolumeType']
                    GetVolumeSize = GetVolume['Volumes'][VolumeCount]['Size']
                    print ("Disk --> Volumeid : {}. VolumeState: {}. VolumeType: {}. VolumeSize {}".format(GetVolumeID,GetDiskState, \
                        GetVolumeType,GetVolumeSize))
            else:
                print ("No Volumes found in Region.")

            #Find all ELBv2 loadbalancer running in Region.
            ELBLoad = boto3.client('elbv2', region_name=FetchRegionList[Region])
            ELBv2 = ELBLoad.describe_load_balancers()
            if len(ELBv2['LoadBalancers']) != 0:
                for ElbCount in range(len(ELBv2['LoadBalancers'])):
                    LBname = ELBv2['LoadBalancers'][ElbCount]['LoadBalancerName']
                    LBState = ELBv2['LoadBalancers'][ElbCount]['State']['Code']
                    print ("Loadbalancer --> LBName : {}. LBState : {}.".format(LBname,LBState))
            else:
                print ("No LoadBalancer found in Region.")

            #Find all Lambda functions running in Region.
            Lmbda = boto3.client('lambda',region_name=FetchRegionList[Region])
            LambdaLst = Lmbda.list_functions()
            if len(LambdaLst['Functions']) != 0:
                for FncCount in range(len(LambdaLst['Functions'])):
                    FncName = LambdaLst['Functions'][FncCount]['FunctionName']
                    FncMem = LambdaLst['Functions'][FncCount]['MemorySize']
                    FncCodeSize = LambdaLst['Functions'][FncCount]['CodeSize']
                    FncRuntime = LambdaLst['Functions'][FncCount]['Runtime']
                    print ("Lambda Function --> Name : {}. Memory : {}. CodeSize : {}. Runtime : {}.".format(FncName, \
                        FncMem,FncCodeSize,FncRuntime))
            else:
                print ("No Lambda function available in Region.")


            #Fetch security groups used in Region
            GetSecurityGroup = Ec2.describe_security_groups()
            if len(GetSecurityGroup['SecurityGroups']) !=0:
                for SecurityGroupCount in range(len(GetSecurityGroup['SecurityGroups'])):
                    GroupId = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['GroupId']
                    VpcId = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['VpcId']
                    GroupName = GetSecurityGroup['SecurityGroups'][SecurityGroupCount]['GroupName']
                    print ("Security --> Groupid : {}. VpcId : {}. GroupName : {}.".format(GroupId,VpcId,GroupName))
            else:
                print ("No security group available for this region.")

            print("**********************************")


if __name__ == '__main__':
    RunQuery = myList()
    RunQuery.ListEc2Instance()
