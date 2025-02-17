import os
import requests
from bs4 import BeautifulSoup
import shutil
import time

# Website URL
BASE_URL = "https://gospelafri1.com/music/south-africa-gospel-music/"
DOWNLOAD_DIR = "/Volumes/Untitled/south_african_gospel_music/"  # Change this to your external disk path

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_song_page_links(page_num):
    """Scrapes a single page for links to individual song pages."""
    url = BASE_URL if page_num == 1 else f"{BASE_URL}page/{page_num}/"
    print(f"Scraping page {page_num}: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to load page {page_num}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    song_links = []

    # Find all links leading to song pages
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "download" in href or "mp3" in href:  # Adjust based on actual link patterns
            if not href.startswith("http"):
                href = BASE_URL + href.lstrip("/")
            song_links.append(href)

    print(f"Found {len(song_links)} song links on page {page_num}.")
    return song_links

def get_mp3_link(song_page_url):
    """Extracts the MP3 link from a song page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(song_page_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to load song page: {song_page_url}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the actual MP3 download link
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".mp3"):
            if not href.startswith("http"):
                href = BASE_URL + href.lstrip("/")
            return href

    return None  # No MP3 link found

def download_mp3(url):
    """Downloads a single MP3 file."""
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        print(f"Skipping {filename}, already downloaded.")
        return

    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {filename}")

def move_files_to_external_drive():
    """Moves downloaded MP3 files to an external drive."""
    external_drive_path = "/Volumes/Untitled/gospel_music/"

    if not os.path.exists(external_drive_path):
        os.makedirs(external_drive_path)

    for file in os.listdir(DOWNLOAD_DIR):
        src = os.path.join(DOWNLOAD_DIR, file)
        dest = os.path.join(external_drive_path, file)
        
        shutil.move(src, dest)
        print(f"Moved {file} to external drive.")

if __name__ == "__main__":
    # Loop through pages 1 to 221
    for page_num in range(1, 5):
        song_pages = get_song_page_links(page_num)
        
        if not song_pages:
            print(f"No song pages found on page {page_num}.")
        else:
            # For each song link on this page, download the MP3 if found
            for song_page in song_pages:
                mp3_link = get_mp3_link(song_page)
                if mp3_link:
                    download_mp3(mp3_link)

        # Move to the next page
        time.sleep(5)  # Sleep for a while to avoid hitting the server too quickly
    
    move_files_to_external_drive()
    print("All files downloaded and moved successfully.")