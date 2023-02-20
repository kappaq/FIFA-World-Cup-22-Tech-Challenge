from who_scored_player_scrap import get_pages_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import time
from collections import defaultdict
import pandas as pd
import time
import re
from itertools import islice

PATH = 'chromedriver'
driver = webdriver.Chrome(PATH)

wait = WebDriverWait(driver, 10)

driver.get(
    'https://www.whoscored.com/Regions/247/Tournaments/36/Seasons/8213/Stages/18657/PlayerStatistics/International-FIFA-World-Cup-2022')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)


def defensive():
    df = get_pages_data(13, 3, 55, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb', 'Blocks',
                  'OwnG', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_defensive.csv', header=True, index=False)


defensive_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[2]/a')
driver.execute_script("arguments[0].click();", defensive_button)
time.sleep(1)

defensive()

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
    'CREATE OR REPLACE TABLE "player_stats_defensive" ("No." STRING, "Player" STRING, "Apps" STRING, "Mins" STRING, "Tackles" STRING, "Inter" STRING, "Fouls" STRING, "Offsides" STRING, "Clear" STRING, "Drb" STRING, "Blocks"  STRING, "OwnG" STRING, "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_defensive.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_defensive")
