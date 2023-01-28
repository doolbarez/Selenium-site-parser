import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By

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
        time.sleep(5)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/a').click()
        time.sleep(5)
        # Тут вводить логин
        driver.find_element(By.NAME, 'text').send_keys('LOGIN')
        driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
        time.sleep(5)
        # Тут вводить пароль
        driver.find_element(By.NAME,"password").send_keys('PASSWORD')
        driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
        time.sleep(5)        
        driver.get(url=url)
        time.sleep(5)    
        src = driver.page_source
        print (source_link)
        with open("index_selenium.html", "w", encoding='utf-8') as file:
            file.write(driver.page_source)

        r = requests.get(url=url)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
        global source_link
        while True:
            with open("parser.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("\t")
                    url = parts[0]
                    get_data_with_selenium(url)
                    with open("index_selenium.html", "r", encoding='utf-8') as file:
                        src = file.read()
                    soup = BeautifulSoup(src, "lxml")
                    twitter_link = soup.find_all("div", role_="button")
                    twitter_link = re.search('div aria-label=(.*?)"', src)
                    if not twitter_link:
                        continue
                    twitter_link2 = twitter_link.group(1)
                    with open('parser.txt') as f:
                        lines = f.readlines()
                    with open('twitter.txt', 'a') as f:
                        for line in lines:
                            parts = line.split('\t')
                            f.write(parts[0] + '\t' + parts[1] + '\t' + parts[2]+ '\n')
                    if not url:
                        break

if __name__ == '__main__':
    main()