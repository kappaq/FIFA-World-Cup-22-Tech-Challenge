from selenium.webdriver.support.select import Select

from who_scored_player_scrap import get_pages_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd
import time


def detailed_tackles():
    df = get_pages_data(8, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_tackles.csv', header=True, index=False)


def detailed_interception():
    df = get_pages_data(6, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_interception.csv', header=True, index=False)


def detailed_fouls():
    df = get_pages_data(7, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Foulde', 'Fouls', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_fouls.csv', header=True, index=False)


def detailed_cards():
    df = get_pages_data(7, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Yellow', 'red', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_cards.csv', header=True, index=False)

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

drop_category.select_by_visible_text("Tackles")
time.sleep(2)
detailed_tackles()

drop_category.select_by_visible_text("Interception")
time.sleep(2)
detailed_interception()

drop_category.select_by_visible_text("Fouls")
time.sleep(2)
detailed_fouls()

drop_category.select_by_visible_text("Cards")
time.sleep(2)
detailed_cards()

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
    'CREATE OR REPLACE TABLE "player_stats_detailed_tackles" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "TotalTackles" STRING , "DribbledPast" STRING , "TotalAttemptedTackles" STRING , "Rating" STRING )'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_tackles.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_tackles")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_interception" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_interception.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_interception")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_fouls" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Foulde" STRING , "Fouls" STRING , "Rating" STRING )'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_fouls.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_fouls")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_cards" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Yellow" STRING , "red" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_cards.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_cards")