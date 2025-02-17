# MP3 Scraper & Corruption Handler

## Overview

When my pastor tasked me with downloading a vast collection of gospel songs from the web, I quickly realized that manually downloading thousands of MP3 files would be tedious and inefficient. Instead of clicking through pages endlessly, I decided to automate the process. Over multiple iterations, I developed a robust web scraper capable of fetching, verifying, and managing thousands of gospel MP3 files while ensuring data integrity.

This project is more than just a downloader—it actively detects and handles corrupted MP3 files, ensuring a clean and high-quality music collection.

## Features

- **Automated MP3 Scraping**: Uses BeautifulSoup and Requests to fetch MP3 file links from target websites.
- **Corruption Detection**: Leverages Mutagen and Pydub to verify MP3 file integrity and flag corrupted files.
- **Intelligent Re-Downloading**: Matches corrupted files with their online sources and attempts to replace them.
- **System Resource Optimization**: Uses `psutil` to monitor disk space and prevent resource overload.
- **File Organization**: Automatically moves corrupted files to a separate directory for review and redownload.

## Evolution of the Script

### 1. **download_mp3.py**

- The initial script that handled basic scraping and downloading.
- Iterated through pages, extracted MP3 URLs, and downloaded the files.
- Included a function to move files to an external drive for organization.

### 2. **download_mp3_1.py**

- Improved efficiency by refining how song links were detected.
- Enhanced URL handling and pagination support.
- Introduced more robust logging and debugging statements.

### 3. **corrupted_mp3.py**

- Developed to identify and isolate corrupted MP3 files.
- Utilized **pydub** and **mutagen** to check MP3 integrity.
- Moved corrupted files to a dedicated folder for review.

### 4. **debug.py**

- A diagnostic tool for troubleshooting scraper behavior.
- Printed server responses, headers, and key HTML snippets.

### 5. **disk_size.py**

- A utility script to monitor available disk space.
- Helped prevent system crashes due to insufficient storage.

## Installation

Ensure you have Python 3 installed, then install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

Run the main script to scan for corrupted MP3 files and attempt to re-download missing or damaged files:

```sh
python mp3_scraper.py
```

Modify the script’s configuration to specify target directories and source websites.

## Dependencies

- `requests` – For handling HTTP requests.
- `beautifulsoup4` – For parsing HTML and extracting MP3 links.
- `mutagen` – For checking MP3 metadata and integrity.
- `pydub` – For deeper audio file analysis.
- `psutil` – For monitoring system resources.
- `shutil` – For efficient file management.

## Skills Gained & Demonstrated

- **Web Scraping & Automation**

  - Extracting data from web pages with **BeautifulSoup**.
  - Handling HTTP requests and pagination with **requests**.
  - Automating file downloads and storage management.

- **File Handling & Organization**

  - Ensuring file integrity using **pydub** and **mutagen**.
  - Automating the movement of files to storage directories.
  - Implementing checks for corrupted files and re-downloading them.

- **Optimized Code & Debugging**

  - Iteratively improving scraper performance.
  - Implementing logging for better error tracking.
  - Using debugging scripts to analyze server responses.

- **System Resource Management**
  - Monitoring disk usage with **psutil**.
  - Implementing time delays to prevent server overload.

## Future Enhancements

- **Parallel Downloads**: Implementing multithreading for faster scraping.
- **Enhanced Matching Algorithms**: Improving detection of missing and corrupted files.
- **Error Handling & Logging**: More resilient exception handling and logging improvements.
- **GUI Application**: Creating a user-friendly interface for non-technical users.

## Key Takeaways

This project transformed what would have been a painstaking manual task into an efficient, automated process. With over **3500 gospel MP3s** successfully scraped and stored, it demonstrates how automation can revolutionize time-consuming workflows while ensuring data quality.

For anyone looking to automate large-scale file downloads while maintaining file integrity, this scraper is a testament to how scripting can be a game-changer!
