# -*- coding: utf-8 -*-
"""


@author: btood
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

option = Options()
option.add_argument('--headless')
#option.add_argument('--incognito')
driver = webdriver.Chrome(chrome_options=option) 

driver.set_window_size(1600, 1000)
driver.get("https://market.yandex.ru/catalog--noutbuki/26895412/list?hid=91013")

def drop_down():
    for x in range(1, 12, 2):  # 1 3 5 7 9 
        time.sleep(1)
        j = x / 9  # 1/9 3/9 5/9 9/9
        # document.documentElement.scrollTop
        # document.documentElement.scrollHeight
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)

page = 0
ydList = []
while page<20:
    driver.implicitly_wait(10) #wait 10s /time.sleep()
    drop_down()
    
    lis = driver.find_elements_by_css_selector('._2vCnw')
    for li in lis:
        row = {}
        row['title'] = li.find_element_by_css_selector('._3Fff3 h3 a span').text
        row['price'] = li.find_element_by_css_selector('[data-zone-name="price"] span span').text 
        try:    
            row['commit'] = li.find_element_by_css_selector('.ZIZLH').text
        except Exception:
            row['commit'] = 'none'
        try:
            row['CPU'] = li.find_element_by_xpath('//li[contains(text(),"процессор")]').text
        except Exception:
            row['CPU'] = 'none'
        try:
            row['screen'] = li.find_element_by_xpath('//li[contains(text(),"экран")]').text
        except Exception:
            row['screen'] = 'none'
        try:
            row['memory'] = li.find_element_by_xpath('//li[contains(text(),"память")]').text
        except Exception:
            row['memory'] = 'none'
        try:
            row['GPU'] = li.find_element_by_xpath('//li[contains(text(),"видеокарта")]').text
        except Exception:
            row['GPU'] = 'none'
        #print(row['title'],row['price'],row['commit'],sep=' | ')
        
        ydList.append(row)
    time.sleep(2)
    page += 1
    b_next = driver.find_element_by_css_selector('[aria-label="Следующая страница"]')
    b_next.click()
    
df = pd.DataFrame(ydList)
df.to_excel('YandexAXP.xlsx',sheet_name='yandex')


    #print(title, price, commit, shop_name, href, sep=' | ')
print('FINISH!!!!!')
driver.quit()