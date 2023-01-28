import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
source_link = ""
def get_data_with_selenium(url):
    global source_link
    options = webdriver.ChromeOptions()
    try:
        driver = webdriver.Chrome()
        driver.get(url=url)
        time.sleep(6)
        src = driver.page_source
        with open("index_selenium.html", "w") as file:
            file.write(driver.page_source)
        r = requests.get(url=url)
        source_link = driver.current_url
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
        while True:
            with open("links.txt", "r") as file:
                for url in file:
                    url = url.strip()
                    get_data_with_selenium(url)
                    with open("index_selenium.html", "r") as file:
                        src = file.read()
                    soup = BeautifulSoup(src, "lxml")
                    twitter_link = soup.find_all("a", class_="SocialTag_tag__1aRTW")
                    twitter_link = re.search('https://www.twitter.com(.*?)"', src)
                    if not twitter_link:
                        continue
                    href = twitter_link.group(1)
                    with open("parser.txt", "a") as file:
                        file.write('https://www.twitter.com'+href+'\t')

                    with open("parser.txt", "a") as file:
                        file.write(source_link+'\t')
                        
                    net_worth = soup.find_all("div", class_="HeaderInfo_totalAssetInner__1mOQs")
                    net_worth = re.search('"HeaderInfo_totalAssetInner__1mOQs">(.*?)<', src)
                    if net_worth:
                        balance = net_worth.group(1)
                        with open("parser.txt", "a") as file:
                            file.write(balance+'\n')

                    if not url:
                        break

if __name__ == '__main__':
    main()