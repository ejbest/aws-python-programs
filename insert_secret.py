import boto3
#########################################################################################
# insert_secret.py                                                                      #
#                                                                                       #
#  Function......Setups up a secret called "mybilling" fill in each by your email root  #
#  Requires......https://aws.amazon.com/sdk-for-python/                                 #
#  Released......March 11, 2021                                                         #
#  Scripter......                                                                       #
#  Invoke........python3 aws-list-services.py                                           #
#                                                                                       #
#########################################################################################
region = 'us-east-1'
#
# You need to haave a key and secret for each environment
# 
dic = {
  "myacc_map":{
<<<<<<< HEAD
	'erich.ej.best@me.com': {
		'access': 'AKIA56GTQVIWL4DVFFFU', 
		'secret': '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'
	}, 'erich@bronzedrum.com': {
		'access': 'AKIAVI7DAWXF6PLOUFGN', 
		'secret': '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'
	}, 'ejbest@alumni.rutgers.edu': {
		'access': 'AKIAVBINT6IXWUDLKBUC', 
		'secret': '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'
	}, 'erich.ej.best.fl@gmail.com': {
		'access': 'AKIA2OTKR7D4SZ2OR6JX', 
		'secret': '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'
	}

  }
}
=======
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
>>>>>>> 7e77aa7959122eec101550b2cf28cebf0d661439
client = boto3.client('secretsmanager')
response = client.create_secret(
    Name='mybilling',
    SecretString=str(dic)
)
