from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests_oauthlib import OAuth1
from io import BytesIO
import requests

# Twitter credentials
API_KEY = 'y7AwQ05joG0FMXD1P4EThPqPH'
API_SECRET = 'WFw9hm6jfNwTmEY2tTayzT0FP7aP5ch78N9g140gn49W1KMUF5'
ACCESS_TOKEN = '1893569243918278657-79yI1AvxSO4pizLEFxhMsSTxYqukmz'
ACCESS_SECRET = 'vGgLHV3rgxsGPuAUGPm95pYWtTKCvBjkgqDHod0fzWQF5'

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

app = FastAPI()

class ImageUploadRequest(BaseModel):
    image_url: str

@app.post("/upload-image")
def upload_image(request: ImageUploadRequest):
    try:
        # Download image
        response = requests.get(request.image_url)
        response.raise_for_status()
        img_bytes = BytesIO(response.content)

        # Upload to Twitter
        upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
        files = {'media': ('image.jpg', img_bytes)}
        twitter_response = requests.post(upload_url, auth=auth, files=files)
        twitter_response.raise_for_status()

        data = twitter_response.json()
        return {
            "status": "success",
            "media_id": data.get("media_id_string")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
