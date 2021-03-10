import boto3
import datetime
import dateutil.relativedelta
import pandas  as pd
import json


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

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
next_month_year = next_month_.year
next_month_month = '{:02}'.format(next_month_.month)
next_month_day_st = f"{next_month_year}-{next_month_month}-01"
next_month_day_ed = str(last_day_of_month(next_month_))[:10]

# replace the map
FILE_PATH = "cred.json"
with open(FILE_PATH) as fp:
    myacc_map = json.load(fp)['myacc_map']

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
        response_f = client.get_cost_forecast(TimePeriod={'Start': next_month_day_st, 'End': next_month_day_ed }, Granularity='DAILY',Metric='UNBLENDED_COST')
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


