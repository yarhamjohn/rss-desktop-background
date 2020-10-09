import ctypes
import feedparser
import os
import sys
import urllib


def get_rss_entry(feed_url):
    # Gets all the entries in the RSS feed.
    feed = feedparser.parse(feed_url)
    entries = feed.entries

    # Checks there is at least one entry
    if len(entries) == 0:
        print("There were no entries in the provided RSS feed: " + feed_url)
        sys.exit()

    # Retrieves all the links listed for the first entry (assumes first entry is most recent)
    return entries[0]


def process_rss_entry(entry, file_path):
    # Loops over all the links listed for entry
    for link in entry.links:

        # Finds the RSS enclosure (https://en.wikipedia.org/wiki/RSS_enclosure), saves the image and sets the background
        if link.rel == "enclosure":
            save_image(link.href, file_path)
            set_background(file_path)
            sys.exit()


def save_image(link_href, file_path):
    # Create containing folder on disk if it does not already exist
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    urllib.request.urlretrieve(link_href, file_path)


def set_background(file_path):
    # Check if an image exists in the specified location and if not, exit
    if not os.path.exists(file_path):
        sys.exit()

    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)


def main():
    # Get command line arguments (first arg is python.exe)
    rss_feed_url = sys.argv[1]
    image_dir = sys.argv[2]

    rss_entry = get_rss_entry(rss_feed_url)

    file_path = os.path.join(image_dir, "image.jpg")
    process_rss_entry(rss_entry, file_path)


main()
