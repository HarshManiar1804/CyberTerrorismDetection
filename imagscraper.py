import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://codeforces.com/profile/HarshManiar'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

img_tags = soup.find_all('img')

image_urls = [urljoin(url, img['src']) for img in img_tags]

for i, image_url in enumerate(image_urls):
    response = requests.get(image_url)
    image_path = f'image_{i}.jpg' 
    with open(image_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded image: {image_path}")