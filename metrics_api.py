import requests
from requests.auth import HTTPBasicAuth
import json

# this is a cloud API key
auth = HTTPBasicAuth('<Cloud Key>', '<Cloud Secret>')
header = {"Content-Type": "application/json"}
data = {
  "aggregations": [
    {
      "metric": "io.confluent.kafka.server/consumer_lag_offsets"
    }
  ],
  "filter": {
    "op": "AND",
    "filters": [
      {
           "field": "resource.kafka.id",
            "op": "EQ",
            "value": "lkc-wzz05"
      },
      {
        "field": "metric.topic",
        "op": "EQ",
        "value": "james-test"
      }
    ]
  },
  "granularity": "PT1M",
  "group_by": [
    "metric.consumer_group_id",
    "metric.topic",
    "metric.partition"
  ],
  "intervals": [
    "PT1H/now"
  ],
  "limit": 25
}

api_url = 'https://api.telemetry.confluent.cloud/v2/metrics/cloud/query'

response = requests.post(api_url, json=data, auth=auth, headers=header)

# Prints response code
print(f"{response}")

# Optional fancy print, feel free to uncomment if needed.
# try:
#    [print(i) for k, v in response.json().items() for i in response.json()[k] if i['value'] == 0]
# except:
#    print("Fancy print didn't work")
#    print(f"{response}\n{response.json()}")

for k, v in response.json().items():
    for i in response.json()[k]:
        print(i)
