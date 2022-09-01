import requests
import glob, os, sys


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

    # request picture from API. Note that we run a GET call.
    r = requests.get(url, headers=headers, cert=(clientCrt, clientKey))

    return url, r