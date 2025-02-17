import os
import requests
from bs4 import BeautifulSoup
import shutil
import time
from mutagen.mp3 import MP3
from pydub.utils import mediainfo
from pydub import AudioSegment

# Website URL
BASE_URL = "https://gospelafri1.com/music/"
DOWNLOAD_DIR = "/Volumes/Untitled/gospelafri1_all/"  # Change this to your external disk path
CORRUPTED_DIR = os.path.join(DOWNLOAD_DIR, "corrupted_mp3")

# Ensure necessary directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CORRUPTED_DIR, exist_ok=True)

def get_song_page_links(page_num):
    """Scrapes a single page for links to individual song pages."""
    url = BASE_URL if page_num == 1 else f"{BASE_URL}page/{page_num}/"
    print(f"Scraping page {page_num}: {url}")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to load page {page_num}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    song_links = [link["href"] for link in soup.find_all("a", href=True) if "gospelafri1.com" in link["href"]]

    print(f"Found {len(song_links)} song links on page {page_num}.")
    return song_links

def get_mp3_link(song_page_url):
    """Extracts the MP3 link from a song page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(song_page_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to load song page: {song_page_url}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".mp3"):
            return href if href.startswith("http") else BASE_URL + href.lstrip("/")
    return None

def download_mp3(url):
    """Downloads a single MP3 file."""
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        print(f"Skipping {filename}, already downloaded.")
        return filepath

    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
        return filepath
    else:
        print(f"Failed to download {filename}")
        return None

def is_mp3_corrupted(filepath):
    """Checks if an MP3 file is corrupted using pydub."""
    try:
        AudioSegment.from_file(filepath, format="mp3")
        return False
    except Exception as e:
        print(f"Corrupted MP3 detected: {filepath} - {e}")
        return True

def is_corrupted(file_path):
    """Checks if the file is corrupted by inspecting its metadata."""
    try:
        # Check if the file is a valid mp3 by inspecting its metadata
        info = mediainfo(file_path)
        return 'mp3' not in info.get('codec_name', '').lower()
    except Exception as e:
        # If an error occurs (e.g., file format issue), treat it as corrupted
        print(f"Error checking file {file_path}: {e}")
        return True

def move_corrupted_files():
    """Moves corrupted MP3 files to a separate folder."""
    for filename in os.listdir(DOWNLOAD_DIR):
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith('.mp3'):
            if is_corrupted(file_path) or is_mp3_corrupted(file_path):
                print(f"Moving corrupted file: {filename}")
                shutil.move(file_path, os.path.join(CORRUPTED_DIR, filename))

if __name__ == "__main__":
    # Loop through the pages and scrape MP3 files
    for page_num in range(1, 4):
        song_pages = get_song_page_links(page_num)
        
        if not song_pages:
            print(f"No song pages found on page {page_num}.")
        else:
            for song_page in song_pages:
                print(f"Scraping song page: {song_page}")
                mp3_link = get_mp3_link(song_page)
                if mp3_link:
                    downloaded_file = download_mp3(mp3_link)
                    if downloaded_file and (is_corrupted(downloaded_file) or is_mp3_corrupted(downloaded_file)):
                        shutil.move(downloaded_file, os.path.join(CORRUPTED_DIR, os.path.basename(downloaded_file)))
                        print(f"Moved corrupted file: {downloaded_file}")

        time.sleep(5)  # Prevents overloading the server
    
    # Move any existing corrupted files in the download folder to the corrupted directory
    move_corrupted_files()
    
    print("All files downloaded and corrupted files moved successfully.")