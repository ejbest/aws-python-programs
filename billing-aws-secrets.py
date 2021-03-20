import boto3
import datetime
import dateutil.relativedelta
import pandas  as pd
import json
import ast
#########################################################################################
# billing.py                                                                            #
#                                                                                       #
#  Function......Git Bill Details from ~/.aws/credentials with other commented keys     #
#  Secrets.......https://github.com/ejbest/aws-python-utils/blob/main/insert_secret.py  #
#  Requires......https://aws.amazon.com/sdk-for-python/                                 #
#  Released......March 11, 2021                                                         #
#  Scripter......                                                                       #
#  Invoke........python3 aws-list-services.py                                           #
#                                                                                       #
#########################################################################################

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def get_secret(sec_name,region):
    secret_name = sec_name
    region_name = region
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response['SecretString']
    except Exception as e:
        raise e


# get today's date
today = datetime.datetime.today()
current_year = today.year
current_month = '{:02}'.format(today.month)
current_day ='{:02}'.format(today.day)
start_day= f"{current_year}-{current_month}-01"
current_day = f"{current_year}-{current_month}-{current_day}"

# get last month's first date
last_month = today + dateutil.relativedelta.relativedelta(months=-1)
last_month_year = last_month.year
last_month_month = '{:02}'.format(last_month.month)
last_month_st = f"{last_month_year}-{last_month_month}-01"
last_month_day_ed = str(last_day_of_month(last_month))[:10]

# get next month date
next_month_ = today + dateutil.relativedelta.relativedelta(months=1)
next2_month_= today + dateutil.relativedelta.relativedelta(months=2)
next_month_year = next_month_.year
next_month_month = '{:02}'.format(next_month_.month)
next_month_day_st = f"{next_month_year}-{next_month_month}-01"
next2_month_year = next2_month_.year
next2_month_month = '{:02}'.format(next2_month_.month)
next_month_day_ed = f"{next2_month_year}-{next2_month_month}-01"

myacc_map= get_secret(sec_name='mybilling',region='us-east-1')
myacc_map = ast.literal_eval(myacc_map)['myacc_map']

account = []
email = []
previous = []
current = []
forecast = []
rec_lis = []
# fetch cost
for each in myacc_map.keys():
    client = boto3.client('ce', aws_access_key_id=myacc_map[each]['access'], aws_secret_access_key=myacc_map[each]['secret'])
    # current month
    response_c = client.get_cost_and_usage(TimePeriod={ 'Start': start_day,'End': current_day }, Granularity='MONTHLY', Metrics=["UNBLENDED_COST"], )
    this_month_cost=sum([float(each['Total']['UnblendedCost']['Amount']) for each in response_c['ResultsByTime'] ])
    # last month
    try:
        response_l = client.get_cost_and_usage(TimePeriod={'Start': last_month_st, 'End': start_day }, Granularity='MONTHLY', Metrics=["UNBLENDED_COST"]    )
        last_month_cost = sum([float(each['Total']['UnblendedCost']['Amount']) for each in response_l['ResultsByTime'] ])
    except Exception as e:
        last_month_cost=0
    # forecast
    try:
        response_f = client.get_cost_forecast(TimePeriod={'Start': next_month_day_st, 'End': next_month_day_ed}, Granularity='MONTHLY',Metric='NET_UNBLENDED_COST')
        next_month_cost = sum([float(each['MeanValue']) for each in response_f['ForecastResultsByTime'] ])
    except Exception as e:
        next_month_cost=0
#     # fetch account
    client = boto3.client("sts", aws_access_key_id=myacc_map[each]['access'], aws_secret_access_key=myacc_map[each]['secret'])
    account_id = client.get_caller_identity()["Account"]
    rec = {"account_id":account_id,"email":each,"previous":last_month_cost,"current":this_month_cost,"forecast":next_month_cost}
    print(rec)
    rec_lis.append(rec)
df = pd.DataFrame(rec_lis)
df.to_csv("cost.csv", index=False)


