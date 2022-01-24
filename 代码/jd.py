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
driver = webdriver.Chrome(chrome_options=option) 
driver.set_window_size(1600, 1000)
driver.get("https://list.jd.com/list.html?cat=670,671,672")

def drop_down(percent):
    if percent == 'full':
        for x in range(1, 12, 2):  # 1 3 5 7 9 
            time.sleep(1)
            j = x / 9  # 1/9 3/9 5/9 9/9
            # document.documentElement.scrollTop
            # document.documentElement.scrollHeight
            js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
            driver.execute_script(js)
    else:
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % percent
        driver.execute_script(js)

page = 0
jdList = []
while page<13:

    driver.implicitly_wait(10) #wait 10s /time.sleep()
    drop_down('full')
    driver.implicitly_wait(10)
    lis = driver.find_elements_by_css_selector('#J_goodsList ul li') #get the list of products   
    for li in lis:
        row = {}
        row['title'] = li.find_element_by_css_selector('.p-name em').text
        row['price'] = li.find_element_by_css_selector('.p-price strong i').text 
        row['commit'] = li.find_element_by_css_selector('.p-commit strong a').text
        try:
            row['shop_name'] = li.find_element_by_css_selector('.J_im_icon a').text
        except Exception:
            row['shop_name'] = 'none'
        row['href'] = li.find_element_by_css_selector('.p-img a').get_attribute('href')
        li.find_element_by_css_selector('.p-img a').click()
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(3)
        
        row['brand'] = driver.find_element_by_css_selector('#parameter-brand li a').text
        try:
            row['RAM'] = driver.find_element_by_xpath('//li[contains(text(),"内存容量")]').text#//li[contains(text(),'内存容量')]
        except Exception:
            row['RAM'] = 'none'
        try:
            row['SSD'] = driver.find_element_by_xpath('//li[contains(text(),"固态硬盘")]').text
        except Exception:
            row['SSD'] = 'none'
        try:
            row['GPU'] = driver.find_element_by_xpath('//li[contains(text(),"显卡型号")]').text
        except Exception:
            row['GPU'] = 'none'
        
        
        driver.find_element_by_xpath('//li[@clstag="shangpin|keycount|product|pcanshutab"]').click()
        drop_down(2/9)
        driver.implicitly_wait(3)
        
        
        try:
            row['CPU'] = driver.find_element_by_xpath('//dt[text()="CPU型号"]/..//dd').text
        #//dt[text()='CPU型号']/..//dd
        except Exception:
            row['CPU'] = 'none'
        try:
            row['screen'] = driver.find_element_by_xpath('//dt[text()="屏幕尺寸"]/..//dd').text
        except Exception:
            row['screen'] = 'none'
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        jdList.append(row)
        
    page += 1
    b_next = driver.find_element_by_class_name('pn-next')
    b_next.click()


        
df = pd.DataFrame(jdList)
df.to_excel('jdAXP.xlsx',sheet_name='jd')


    #print(title, price, commit, shop_name, href, sep=' | ')
print('FINISH!!!!!')
driver.quit()

