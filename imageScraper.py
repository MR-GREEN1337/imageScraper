import os
from icrawler.builtin import BingImageCrawler, BaiduImageCrawler
from bs4 import BeautifulSoup
import requests
import sys

count = int(sys.argv[1])
keyword = sys.argv[2:]
keyword = ' '.join(keyword)

# create a directory to store the images
if not os.path.exists(f"{keyword}"):
    os.makedirs(f"{keyword}")
    os.makedirs(f"{keyword}/google")

# define the crawlers and start crawling
bing_crawler = BingImageCrawler(
    downloader_threads=4,
    storage={'root_dir': f"{keyword}/bing"}
)
bing_crawler.crawl(
    keyword=keyword,
    max_num=count
)

baidu_crawler = BaiduImageCrawler(
    downloader_threads=4,
    storage={'root_dir': f"{keyword}/baidu"}
)
baidu_crawler.crawl(
    keyword=keyword,
    max_num=count
)
#Google scraper
query = keyword
url = f"https://www.google.com/search?q={query}&tbm=isch"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
images = soup.find_all("img")

max_images = 50  # Download up to 50 images

for img in images:
    if count == max_images:
        break

    image_url = img['src']
    try:
        image_content = requests.get(image_url).content
    except:
        continue

    image_file = open(f"{keyword}/google/{query}_{count}.jpg", 'wb')
    image_file.write(image_content)
    image_file.close()

    count += 1
