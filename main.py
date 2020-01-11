#!/usr/bin/python

import os
import sys
import json
import base64
import requests
import random

BASE_URL = 'https://discordapp.com/api/v7'
IMAGES_DIR = './images/'

with open('config.json') as json_config:
    config = json.load(json_config)

TOKEN = config.get('token')
GUILD_ID = config.get('guild_id')

image = random.choice(os.listdir(IMAGES_DIR))
_, image_ext = os.path.splitext(image)

if not image_ext:
    sys.exit(1)

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

r = requests.patch(f'{BASE_URL}/guilds/{GUILD_ID}', data=json.dumps(payload), headers=headers)
print(r.status_code)
