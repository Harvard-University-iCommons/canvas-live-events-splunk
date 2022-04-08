import json
import os
from datetime import datetime

import requests

env = os.environ['ENV']

splunk_hec_token = os.environ['SPLUNK_HEC_TOKEN']
splunk_hec_url = os.environ["SPLUNK_HEC_URL"]

def lambda_handler(event, context):

    records = event["Records"]

    event_batch = []

    for rec in records:
        body = json.loads(rec['body'])

        # convert the event timestamp into epoch seconds
        timestamp_string = body['metadata']['event_time']
        timestamp = datetime.fromisoformat(timestamp_string.replace('Z', '+00:00'))
        unix_timestamp = timestamp.strftime('%s.%f')

        # set the host parameter based on the hostname from event metadata
        host = body['metadata'].get('hostname', 'unknown')

        # format the event and add it to the batch
        event = {
            "sourcetype": "_json",
            "host": host,
            "time": unix_timestamp,
            "source": "canvas-live-events",
            "event": body
        }
        event_batch.append(json.dumps(event))

    # send the batch of events to Splunk
    headers = {"Authorization": f"Splunk {splunk_hec_token}"}
    res = requests.post(splunk_hec_url, headers=headers, data='\n'.join(event_batch))

    print(f"[INFO] lambda invocation handled {len(event_batch)} events")
    print(f'[INFO] splunk response: {res.text}')

    return {"statusCode": 200, "splunk_response": res.text}
