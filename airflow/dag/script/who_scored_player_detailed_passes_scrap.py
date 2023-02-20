from selenium.webdriver.support.select import Select

from who_scored_player_scrap import get_pages_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd
import time


def detailed_passes_length():
    df = get_pages_data(10, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_passes_length.csv', header=True,
              index=False)


def detailed_passes_type():
    df = get_pages_data(11, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'AccCr', 'InAccCr', 'AccCrn', 'InAccCrn', 'AccFrk', 'InAccFrK',
                  'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_passes_type.csv',
              header=True,
              index=False)


def detailed_key_passes_type():
    df = get_pages_data(11, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Cross', 'Corner', 'Throughball',
                  'Freekick', 'Throwin', 'Other', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_key_passes_types.csv',
              header=True,
              index=False)


def detailed_key_passes_length():
    df = get_pages_data(8, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Long', 'Short', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_key_passes_length.csv',
              header=True,
              index=False)

PATH = 'chromedriver'
driver = webdriver.Chrome(PATH)


wait = WebDriverWait(driver, 10)

driver.get(
    'https://www.whoscored.com/Regions/247/Tournaments/36/Seasons/8213/Stages/18657/PlayerStatistics/International-FIFA-World-Cup-2022')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)

detail_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[5]/a')
driver.execute_script("arguments[0].click();", detail_button)
time.sleep(1)

driver.refresh()
time.sleep(3)

detail_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[5]/a')
driver.execute_script("arguments[0].click();", detail_button)
time.sleep(1)

dropdown_category = driver.find_element(By.ID, 'category')
drop_category = Select(dropdown_category)
drop_category.select_by_visible_text("Goals")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

search_button = driver.find_element(By.XPATH, '//*[@class="search-button"]')
driver.execute_script("arguments[0].click();", search_button)
time.sleep(1)

drop_category.select_by_visible_text("Passes")
time.sleep(2)

detailed_passes_length()

dropdown_subcategory = driver.find_element(By.ID, 'subcategory')
drop_subcategory = Select(dropdown_subcategory)
drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

detailed_passes_type()

drop_category.select_by_visible_text("Key passes")
time.sleep(2)

detailed_key_passes_length()

drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

detailed_key_passes_type()


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
    'CREATE OR REPLACE TABLE "player_stats_detailed_passes_length" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "AccLB" STRING , "InAccLB" STRING , "AccSP" STRING , "InAccSP" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_passes_length.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_passes_length")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_passes_type" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "AccCr" STRING , "InAccCr" STRING , "AccCrn" STRING , "InAccCrn" STRING , "AccFrk" STRING , "InAccFrK" STRING, "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_passes_type.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_passes_type")

cs.execute('CREATE OR REPLACE TABLE "player_stats_detailed_key_passes_types" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Cross" STRING , "Corner" STRING , "Throughball" STRING, "Freekick" STRING , "Throwin" STRING , "Other" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_key_passes_types.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_key_passes_types")


cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_key_passes_length" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Long" STRING , "Short" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_key_passes_length.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_key_passes_length")