#%%
import requests
from pathlib import Path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))
#%%
clientCrt = "../certificates/pilot-users.crt"
clientKey = "../certificates/pilot-users.key"
#%%
url = "https://langenthal.hesotech.eu/imaster/api/v1/TestRunReportingService/GetMeasurementSetList"

headers = {'content-type': 'application/json'}
payload = {
  'chartQuery': {
    'chartId': '02a96b64-7792-a940-4fe5-edace24deeb0',
    'from': '2021-09-17T09:29:54.252178+00:00',
    'till': '',
    'maxNumberOfPoints': 1
  }
}
r = requests.post(url, headers=headers, cert=(clientCrt, clientKey), json=payload)

print(r.status_code)
print(r.json())
# %%
