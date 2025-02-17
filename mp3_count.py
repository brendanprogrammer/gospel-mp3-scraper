import os

folder_path = "/Volumes/Untitled/MASTER_mp3/"

mp3_count = sum(1 for file in os.listdir(folder_path) if file.lower().endswith(".mp3") and not file.startswith("._"))

print(f"Total MP3 files: {mp3_count}")