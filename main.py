#!/usr/bin/python

import os
import sys
import json
import base64
import pickle
import requests
import random


BASE_URL = 'https://discordapp.com/api/v7'
IMAGES_DIR = './images/'
POSTED_IMAGES_FILE = './posted_images.bin'
IMAGES = os.listdir(IMAGES_DIR)


def get_random_image(posted_images):
    image = random.choice(IMAGES)
    if not image in posted_images:
        _, image_ext = os.path.splitext(image)

        if not image_ext:
            return get_random_image(posted_images)

        return image, image_ext
    return get_random_image(posted_images)


with open('config.json') as json_config:
    config = json.load(json_config)

TOKEN = config.get('token')
GUILD_ID = config.get('guild_id')

with open(POSTED_IMAGES_FILE, 'rb') as f:
    try:
        posted_images = pickle.load(f)
        if not posted_images or len(IMAGES) - 1 == len(posted_images):
            posted_images = []
    except EOFError:
        posted_images = []

print(posted_images)
image, image_ext = get_random_image(posted_images)

posted_images.append(image)

with open(POSTED_IMAGES_FILE, 'wb') as f:
    pickle.dump(posted_images, f)


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
