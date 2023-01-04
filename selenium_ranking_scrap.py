import json

import driver as driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import pandas as pd
import time

dict_res = defaultdict(list)

options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1000,550")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

PATH = 'chromedriver'
driver = webdriver.Chrome(PATH, options=options)

a = ActionChains(driver)
wait = WebDriverWait(driver, 10)

driver.get('https://www.fifa.com/fifa-world-ranking/men?dateId=id13792')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)

rows_count = driver.find_elements(By.XPATH, '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr')
for i in range(len(rows_count)):
    i += 1
    index = driver.find_element(By.XPATH,
                                '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                    i) + ']/td[1]')
    teams = driver.find_element(By.XPATH,
                                '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                    i) + ']/td[3]')
    ranks = driver.find_element(By.XPATH,
                                '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(i) + ']/td[6]')
    dict_res['RK'].append(index.text)
    dict_res['Teams'].append(teams.text)
    dict_res['Rank'].append(ranks.text)

# go to next pages
for page in range(4):
    next_page = driver.find_element(By.XPATH, '//*[@id="content"]/main/section[2]/div/div/div[2]/div/div/div/div/div[3]/div/button')
    driver.execute_script("arguments[0].click();", next_page)
    time.sleep(1)
    rows_count = driver.find_elements(By.XPATH, '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr')
    for i in range(len(rows_count)):
        i += 1
        index = driver.find_element(By.XPATH,
                                    '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[1]')
        teams = driver.find_element(By.XPATH,
                                    '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[3]')
        ranks = driver.find_element(By.XPATH,
                                    '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[6]')
        dict_res['RK'].append(index.text)
        dict_res['Teams'].append(teams.text)
        dict_res['Rank'].append(ranks.text)

driver.close()

df_res = pd.DataFrame(dict_res)
df_res.to_csv('the_ranking_scrap.csv', header=True, index=False)
print("--------")
print("\n")
print(df_res.to_string())
print("\n")
print("--------")
