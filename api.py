
import requests
from pprint import pprint



from apiclient.discovery import build

import os
google_vision_api_key = os.environ["GOOGLE_VISION_API_KEY"]


# Use the build() function to create a service object. 
# It takes an API name and API version as arguments.
# See more: https://developers.google.com/api-client-library/python/apis/

picture_service = build('vision', 'v1', developerKey='google_vision_api_key')