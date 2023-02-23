import requests
import json

clientCrt = "../certificates/rw.crt"
clientKey = "../certificates/rw.key"

apiBaseUrl = "https://docucamrw.hesotech.eu/DocuCam/CameraOne/api/v1"
channelInfoUrl = apiBaseUrl + "/Data/ChannelInfo"
imageApiUrl = apiBaseUrl + "/Data/ImageAndMeasurements"

headers = {'content-type': 'application/json'}

requestData = {
    'SiteName': 'CameraTwo',
    'SceneName': 'SmallFieldSlide',
    'TimeRange': {
        'Minimum': '2022-08-01T00:00:00.000Z',
        'Maximum': '2023-02-01T00:00:00.000Z'
    },
    'Coordinates': [ { 'Layer': 0, 'Row': 1, 'Col': 0 } ]
}

channelResponse = requests.get(channelInfoUrl, headers=headers, cert=(clientCrt, clientKey), allow_redirects=True)

if (channelResponse.status_code != 200):
    print('Something went wrong!')
    exit(-1)

response = requests.post(
    imageApiUrl,
    headers=headers,
    cert=(clientCrt, clientKey),
    allow_redirects=True,
    data=json.dumps(requestData)
)

if (response.status_code != 200):
    print('Something went wrong!')
    exit(-1)

channelInfoData = channelResponse.json()
data = response.json()

for record in data:
    print(record['Timestamp'], ' -> ', record['Values'], ' -> ', record['ImageUrls'])

