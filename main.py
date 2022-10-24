# Importing random for choosing random image, requests for getting data from xkcd.com and json to load data
import random
import requests
import json

# Variables
number = input("What comic number to download? ")
url = "https://xkcd.com/"
file_url = f"{number}/info.0.json"
local_file = "img.png"

# Getting and loading information about image
print(f"Getting information about comic number: {number}")
response = requests.get(url + file_url).text
loaded_response = json.loads(response)
img_url = loaded_response["img"]
# Downloading image
print(f"Downloading comic number: {number}")
img_content = requests.get(img_url).content

# Writing image to file
print(f"Writing image to file: {local_file}")
with open(local_file, "wb") as file:
    file.write(img_content)

print(f"Successfully downloaded comic number {number} to file {local_file}")
