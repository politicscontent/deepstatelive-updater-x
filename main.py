import json
import time
import requests
import re

import tweepy

json_file = open('tokens.json', 'r+')
json_content = json.loads(json_file.read())

json_file.close()

tclient = tweepy.Client(consumer_key            =   json_content['api_key'],
                        consumer_secret         =   json_content['api_key_secret'],
                        access_token            =   json_content['access_token'],
                        access_token_secret     =   json_content['access_token_secret'],
                        bearer_token            =   json_content['bearer_token'])

auth = tweepy.OAuth1UserHandler(json_content['api_key'], json_content['api_key_secret'])
auth.set_access_token(
    json_content['access_token'],
    json_content['access_token_secret']
)
auth_client = tweepy.API(auth)

url = 'https://deepstatemap.live/api/history/'
content = json.loads(requests.get(url=url).content.decode('utf-8'))
latest = content[0]
l_keys = latest.keys()

cache = [None]

while True:
    time.sleep(1)

    descriptionUA_raw = latest['description']
    descriptionUA = re.sub(re.compile('<.*?>'), '', descriptionUA_raw)

    descriptionEN_raw = latest['descriptionEn']
    descriptionEN = re.sub(re.compile('<.*?>'), '', descriptionEN_raw)

    desc = f"description (UA): {descriptionUA}\ndescription (EN): {descriptionEN}\nupdated: {latest['updatedAt'].split('T')[0]}\ncreated: {latest['createdAt'].split('T')[0]}\nData from: deepstatemap.live"

    if cache[-1] != desc:
        cache.append(desc)
        tclient.create_tweet(text=desc)
    
#tclient.create_tweet(text='fuck')
