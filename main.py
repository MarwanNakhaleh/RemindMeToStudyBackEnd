# # Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import json
from base64 import b64decode
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO)

def lambda_handler(event, context):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    logging.info(event)
    
    try:
        event_body = json.loads(b64decode(event["body"]))
        logging.info(event_body)
        phone_number = event_body["phone_number"]
        message = client.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_="+19138008135",
                        to=phone_number
                    )
        return {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json"
            },
            "statusCode": 200,
            "body": message.sid
        }
    # generic exception, though it might just be a KeyError
    except Exception as e:
        logging.error(str(e))
        return {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json"
            },
            "statusCode": 500,
            "body": str(e)
        }
