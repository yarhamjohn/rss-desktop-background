import ctypes
import feedparser
import os
import sys
import urllib
from PIL import Image, ImageFont, ImageDraw


def get_rss_entry(feed_url):
    # Gets all the entries in the RSS feed.
    feed = feedparser.parse(feed_url)
    entries = feed.entries

    # Checks there is at least one entry
    if len(entries) == 0:
        print("There were no entries in the provided RSS feed: " + feed_url)
        sys.exit()

    # Get the first entry that appears not to be of a person
    # Based on the assumption that the majority of images of people have a title starting 'FirstName LastName: ...'
    for entry in entries:
        title = entry.title
        title_might_contain_name = len(title.split(":")[0].split(" ")) == 2
        if title_might_contain_name:
            continue
        else:
            return entry

    # As a backup, just return the first entry
    return entries[0]


def process_rss_entry(entry, file_path):
    # Loops over all the links listed for entry
    for link in entry.links:
        # Finds the RSS enclosure (https://en.wikipedia.org/wiki/RSS_enclosure), saves the image and sets the background
        if link.rel == "enclosure":
            save_image(link.href, file_path)
            add_image_title(file_path, entry.title)
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
    rss_feed_url = sys.argv[1]
    image_dir = sys.argv[2]

    rss_entry = get_rss_entry(rss_feed_url)

    file_path = os.path.join(image_dir, "image.jpg")
    process_rss_entry(rss_entry, file_path)


main()
