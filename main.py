#!/usr/bin/python

import os
import base64
import json
import requests
from random import choice

BASE_URL = 'https://discordapp.com/api/v7'
IMAGES_DIR = './images/'

with open('config.json') as json_config:
    config = json.load(json_config)

TOKEN = config.get('token')
GUILD_ID = config.get('guild_id')

image = choice(os.listdir(IMAGES_DIR))
_, image_ext = os.path.splitext(image)
image_type = 'jpeg' if image_ext == '.jpg' else image_ext[1:]

with open(f'{IMAGES_DIR}{image}', 'rb') as image_file:
    b64_image = base64.b64encode(image_file.read())

payload = {
    'banner': f'data:image/{image_type};base64,{b64_image.decode()}'
}

headers = {
    'Accept': '*/*',
    'Authorization': f'Bot {TOKEN}',
    'Content-Type': 'application/json'
}

# r = requests.patch(f'{BASE_URL}/guilds/{GUILD_ID}', data=json.dumps(payload), headers=headers)
r = requests.get(f'{BASE_URL}/guilds/{GUILD_ID}', headers=headers)
print(r.status_code)