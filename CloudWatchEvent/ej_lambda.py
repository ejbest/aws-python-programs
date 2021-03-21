import json

def ej_lambda(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda that was triggered to run!')
    }
