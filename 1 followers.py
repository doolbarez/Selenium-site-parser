import requests
from selenium import webdriver
import time
import re

def get_data_with_selenium(url):
    options = webdriver.ChromeOptions()
    try:
        driver = webdriver.Chrome()
        driver.get(url=url)
        time.sleep(5)
        src = driver.page_source
        with open("index_selenium.html", "w") as file:
            file.write(driver.page_source)

        r = requests.get(url=url)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    start = 0
    while start < 8600:
        url = "https://debank.com/profile/0xe70981f2aeb601a12001465c7a5e52aa76adcbec/follower?start=" + str(start)
        get_data_with_selenium(url)
        with open("index_selenium.html", "r") as file:
            src = file.read()
        pattern = '"db-user-name is-web3" title="(.*?)"'
        for match in re.finditer(pattern, src):
            link = match.group(1)
            with open("links.txt", "a") as file:
                file.write('https://debank.com/profile/'+link+'\n')
        pattern2 = '"db-user-name is-address" title="(0x[a-fA-F0-9]{40})"'
        for match2 in re.finditer(pattern2, src):
            link2 = match2.group(1)
            with open("links.txt", "a") as file:
                file.write('https://debank.com/profile/'+link2+'\n')
        start += 100

if __name__ == '__main__':
    main()
