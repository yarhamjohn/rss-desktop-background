import ctypes
from dataclasses import dataclass
import feedparser
import os
import sys
import urllib.request, json
from PIL import Image, ImageFont, ImageDraw


def get_image_data(api_key):
    base_url = "https://api.nasa.gov/planetary/apod?api_key=" + api_key
    with urllib.request.urlopen(base_url) as url:
        data = json.loads(url.read().decode())
    
    return data


def process_image_data(image_data, file_path):
    save_image(image_data['hdurl'], file_path)
    add_image_title(file_path, image_data['title'])
    set_background(file_path)
    sys.exit()


def save_image(link_href, file_path):
    # Create containing folder on disk if it does not already exist
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    urllib.request.urlretrieve(link_href, file_path)


def get_font(image, title):
    font_size = 1
    jump_size = 75
    img_fraction = 0.30
    max_font_size = img_fraction * image.size[0]

    font_path = "./Lato-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, font_size)
    while True:
        if font.getsize(title)[0] < max_font_size:
            font_size += jump_size
        else:
            jump_size = jump_size // 2
            font_size -= jump_size
        font = ImageFont.truetype(font_path, font_size)
        if jump_size <= 1:
            break

    return font


def set_background(file_path):
    # Check if an image exists in the specified location and if not, exit
    if not os.path.exists(file_path):
        sys.exit()

    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)


def add_image_title(file_path, title):
    image = Image.open(file_path)
    editable_image = ImageDraw.Draw(image)

    font = get_font(image, title)

    editable_image.text((15, 15), title, (255, 153, 0), font)
    image.save(file_path)


def main():
    # Get command line arguments (first arg is python.exe)
    api_key = sys.argv[1]
    image_dir = sys.argv[2]

    image_data = get_image_data(api_key)

    file_path = os.path.join(image_dir, "image.jpg")
    process_image_data(image_data, file_path)


main()
