import requests
import copy
import pandas as pd 
from datetime import datetime
import json 

def return_data(start_date = '2022-01-01T00:00:00.000Z', end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                site = "CameraOne", scene = "HospitalView", all_coordinates = True):
    """
    Returns image data as list of hyperlinks and measurements with appropriate labels as a pandas dataframe.

    takes following parameter as input:
    - start_date; end_date --> Beginn and End Date of Data Collection, if left empty will return all available data.
    - site --> specify the Site from which data shall be returned: Possible parameters: [CameraOne, CameraTwo]. Default is CameraOne
    - scene ---> specify Scene from which data shall be returned. Possible parameteres depending on SiteName:  
                            [CameraOne [HospitalView]], [CameraTwo [SmallStreetSlide, StreetSlide, SchoolView]]. Default is HospitalView

    - coordinates: Specify what specific tiles shall be returned of the scenes - if left empty returns all available tiles.
                Possible parameters: 'Coordinates': [ { 'Layer': 0, 'Row': 1, 'Col': 0 }, { 'Layer': 0, 'Row': 1, 'Col': 1 } ] 
    """
    # set variables
    clientCrt = "../certificates/rw.crt"
    clientKey = "../certificates/rw.key"

    if site == "CameraOne":
        apiBaseUrl = "https://docucamrw.hesotech.eu/DocuCam/CameraOne/api/v1"
    if site == "CameraTwo":
        apiBaseUrl = "https://docucamrw.hesotech.eu/DocuCam/CameraTwo/api/v1"

    channelInfoUrl = apiBaseUrl + "/Data/ChannelInfo" 
    imageApiUrl = apiBaseUrl + "/Data/ImageAndMeasurements"  # measurements are averages during scan time (scan time 5-30min)

    headers = {'content-type': 'application/json'}

    #request Image and Measurement Data
    if all_coordinates == True: 
        requestData = {
    
        'SiteName': site,
        'SceneName': scene,
        'TimeRange': {
            'Minimum': start_date,
            'Maximum': end_date
        }}
    else: 
        requestData = {
    
        'SiteName': site,
        'SceneName': scene,
        'TimeRange': {
            'Minimum': start_date,
            'Maximum': end_date
        },
        # note that coordinates start at index 0 here opposed to the GUI where index starts at 1. 
        'Coordinates': [ { 'Layer': 1, 'Row': 3, 'Col': 1} ]  # how to adjust this???
        }

    #get labels 
    channelResponse = requests.get(channelInfoUrl, headers=headers, cert=(clientCrt, clientKey), allow_redirects=True)

    #get Iamge and Measurement Data
    response = requests.post(
    imageApiUrl,
    headers=headers,
    cert=(clientCrt, clientKey),
    allow_redirects=True,
    data=json.dumps(requestData)
    )

    #call APIs
    channelInfoData = channelResponse.json()
    data = response.json()
    
    # obtain measurement labels
    skip_rate = 2
    measurement_labels = []
    for item in channelInfoData:
        for index, (key, value) in enumerate(item.items()):
            if index % skip_rate == 0:
                measurement_labels.append(value)

    # map labels with measurements and drop redundant columns
    df = pd.DataFrame(data)
    count = 0
    for i in measurement_labels:
        df[i] =df['Values'].apply(lambda x: x[count] )
        count = count + 1
    df = df.drop(columns=['Values'])

    # add identifier for camera and scence
    df["Site_Scence"] = site+"_"+scene 

    return df 

def query_image(scence, layer, column, row, timestamp = "latest"):

    # import key and certificate
    clientCrt = "../certificates/pilot-users.crt"
    clientKey = "../certificates/pilot-users.key"

    # tranform input variables to strings
    spacing = "/"
    scence = str(scence) + spacing
    layer = str(layer) + spacing
    column = str(column) + spacing
    row = str(row) + spacing
    timestamp = str(timestamp)
    
    # append parameters to base url and construct the request query
    request_url_base = "https://langenthal.hesotech.eu/DocuCam/Image/"
    url = request_url_base + scence + layer + column + row + timestamp
    
    # set content as image/jpeg to obtain image
    headers = {'content-type': 'image/jpeg'}

    # request picture from API. Note that we run a GET Request since we do not need to specify parameters for request.
    r = requests.get(url, headers=headers, cert=(clientCrt, clientKey))

    return url, r

def strip_scans(d, query):

    # import json with timestamps
    df = pd.read_json("../data/scene_0_scans.json")
    d = df.to_dict(orient = 'records')

    # copy dict
    d_copy = copy.deepcopy(d)

    query = str(query)
    temp_val = [value for value in d_copy if query in value["ScanName"]]

    values = [i['ScanName'] for i in temp_val]
    
    return values, d