import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import sqlite3 as sql

urls = []
product_urls = []
list_of_reviews = []


# Each page urls
for i in range(1, 252):
    urls.append(f"https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&explicit=1&page={i}")

# Scrapping each product's urls | 16,064 products
for url in urls:
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    sleep(5)
    for i in range(1, 65):
        product = driver.find_element_by_xpath(f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[1]/div/div/ul/li[{i}]/div/a')
        product_urls.append(product.get_attribute('href'))

# Scrapping each product's reviews     
driver = webdriver.Chrome(executable_path='chromedriver.exe')  
for product_url in product_urls[15:]:
    try:
        driver.get(product_url)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html,'html')
        for i in range(4):
            try:
                list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
            except:
                continue
        while(True):
            try:
                next_button = driver.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
                if next_button != None:
                    next_button.click()
                    sleep(5)
                    html = driver.page_source
                    soup = BeautifulSoup(html,'html')
                    for i in range(4):
                        try: 
                            list_of_reviews.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                        except:
                            continue
            except Exception as e:
                print('finsish : ', e)
                break
    except:
        continue
            
scrappedReviewsAll = pd.DataFrame(list_of_reviews, index = None, columns = ['reviews'])         
scrappedReviewsAll.to_csv('scrappedReviewsAll.csv')


df = pd.read_csv('scrappedReviewsAll.csv')
conn = sql.connect('scrappedReviewsAll.db')
df.to_sql('scrappedReviewsAllTable', conn)       
  




