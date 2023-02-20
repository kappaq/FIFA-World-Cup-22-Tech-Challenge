import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd

import time


dict_res = defaultdict(list)

options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1000,550")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)

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
    total_points = driver.find_element(By.XPATH,
                                       '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                           i) + ']/td[4]')
    previous_points = driver.find_element(By.XPATH,
                                          '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                              i) + ']/td[5]')
    ranks = driver.find_element(By.XPATH,
                                '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(i) + ']/td[6]')
    dict_res['RK'].append(index.text)
    dict_res['Teams'].append(teams.text)
    dict_res['Total Points'].append(total_points.text)
    dict_res['Previous Points'].append(previous_points.text)
    dict_res['+/-'].append(ranks.text)

# go to next pages
for page in range(4):
    next_page = driver.find_element(By.XPATH,
                                    '//*[@id="content"]/main/section[2]/div/div/div[2]/div/div/div/div/div[3]/div/button')
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
        total_points = driver.find_element(By.XPATH,
                                           '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                               i) + ']/td[4]')
        previous_points = driver.find_element(By.XPATH,
                                              '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                                  i) + ']/td[5]')
        ranks = driver.find_element(By.XPATH,
                                    '//*[@id="content"]/main/section[2]/div/div/div/table/tbody/tr[' + str(
                                        i) + ']/td[6]')
        dict_res['RK'].append(index.text)
        dict_res['Teams'].append(teams.text)
        dict_res['Total Points'].append(total_points.text)
        dict_res['Previous Points'].append(previous_points.text)
        dict_res['+/-'].append(ranks.text)

driver.close()

df_res = pd.DataFrame(dict_res)
df_res.to_csv('the_ranking_scrap.csv', header=True, index=False)

ctx = snowflake.connector.connect(user='KAPPAQ',
                                  password='Divine123!',
                                  account='ze71073',
                                  warehouse='COMPUTE_WH',
                                  region='eu-central-1',
                                  schema='PUBLIC'
                                  )
cs = ctx.cursor()
cs.execute("USE WAREHOUSE COMPUTE_WH")
cs.execute("USE ROLE SYSADMIN")
cs.execute("USE DATABASE WORLD_CUP_22_CHALLENGE")
cs.execute("USE SCHEMA  PUBLIC")
cs.execute(
    'CREATE OR REPLACE  TABLE "ranking" ("RK" STRING,"Teams" STRING,"Total Points" STRING,"Previous Points" STRING,"+/-" STRING)')

df_ranking = pd.read_csv("the_ranking_scrap.csv", sep=",")

write_pandas(ctx, df_ranking, table_name="ranking")

