import requests

url = "https://gospelafri1.com/music/south-africa-gospel-music/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Page Content:", response.text[:120000])  # Print first 5000 characters to inspect