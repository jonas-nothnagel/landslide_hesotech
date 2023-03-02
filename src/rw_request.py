import requests
import copy
import pandas as pd 
from datetime import datetime
import json 

# Constants
CLIENT_CRT = "../certificates/rw.crt"
CLIENT_KEY = "../certificates/rw.key"
HEADERS = {'content-type': 'application/json'}

def return_data(start_date: str = '2022-01-01T00:00:00.000Z', 
                end_date: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                site: str = "CameraOne", scene: str = "HospitalView", 
                all_coordinates: bool = True) -> pd.DataFrame:

    """
    Returns image data as list of hyperlinks and measurements with appropriate labels as a pandas dataframe.

    Args:
        start_date (str): Begin date of data collection in ISO 8601 format. Default is '2022-01-01T00:00:00.000Z'.
        end_date (str): End date of data collection in ISO 8601 format. Default is current datetime in UTC.
        site (str): Name of the site from which data shall be returned. Possible values: 'CameraOne', 'CameraTwo'.
            Default is 'CameraOne'.
        scene (str): Name of the scene from which data shall be returned. Possible values depend on site:
            CameraOne: 'HospitalView'.
            CameraTwo: 'SmallStreetSlide', 'StreetSlide', 'SchoolView'.
            Default is 'HospitalView'.
        all_coordinates (bool): Whether to return data for all available coordinates or only specific ones.
            Default is True.

    Returns:
        A pandas dataframe containing image data as a list of hyperlinks and measurements with appropriate labels.

    Raises:
        ValueError: If site and scene parameters do not match.
    """
        
    clientCrt = CLIENT_CRT
    clientKey = CLIENT_KEY
    apiBaseUrl = f"https://docucamrw.hesotech.eu/DocuCam/{site}/api/v1"
    headers = HEADERS
    
    # Check if site and scene match
    if site == "CameraOne" and scene != "HospitalView":
        raise ValueError("Invalid scene parameter for site 'CameraOne'. Possible values: 'HospitalView'.")
    elif site == "CameraTwo" and scene not in ["SmallStreetSlide", "StreetSlide", "SchoolView"]:
        raise ValueError("Invalid scene parameter for site 'CameraTwo'. Possible values: 'SmallStreetSlide', 'StreetSlide', 'SchoolView'.")
    
    requestData = {
        'SiteName': site,
        'SceneName': scene,
        'TimeRange': {
            'Minimum': start_date,
            'Maximum': end_date
        }
    }
    
    if not all_coordinates:
        requestData['Coordinates'] = [{'Layer': 0, 'Row': 1, 'Col': 0}, {'Layer': 0, 'Row': 1, 'Col': 1}]
    
    channelInfoUrl = f"{apiBaseUrl}/Data/ChannelInfo"
    imageApiUrl = f"{apiBaseUrl}/Data/ImageAndMeasurements"

    channelResponse = requests.get(channelInfoUrl, headers=headers, cert=(clientCrt, clientKey))
    response = requests.post(imageApiUrl, headers=headers, cert=(clientCrt, clientKey), data=json.dumps(requestData))
    
    channelInfoData = channelResponse.json()
    data = response.json()
    
    measurement_labels = [v for i, item in enumerate(channelInfoData) for j, (k, v) in enumerate(item.items()) if j % 2 == 0]
    df = pd.DataFrame(data).drop(columns=['Values'])
    
    for i, label in enumerate(measurement_labels):
        df[label] = df['Values'].apply(lambda x: x[i])
        
    df['Site_Scence'] = f"{site}_{scene}"
    
    return df

    

                         




