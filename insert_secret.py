import boto3
region = 'us-east-1'
#
# You need to haave a key and secret for each environment
# 
dic = {
  "myacc_map":{
  "email1@me.com": {
    "access": " ",
    "secret": " "
  },
  "eamil2@mail.com": {
    "access": " ",
    "secret": " "
  },
  "email3@yahoo.com": {
    "access": " ",
    "secret": " "
  },
  "email4@gmail.com": {
    "access": " ",
    "secret": " "
  }
}
}
client = boto3.client('secretsmanager')
response = client.create_secret(
    Name='mybilling',
    SecretString=str(dic)
)
