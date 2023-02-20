from selenium.webdriver.support.select import Select

from who_scored_player_scrap import get_pages_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd
import time


def detailed_shoots_zones():
    df = get_pages_data(9, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_shoots_zones.csv', header=True, index=False)


def detailed_shoots_situations():
    df = get_pages_data(10, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyTaken', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_shoots_situations.csv', header=True,
              index=False)


def detailed_shoots_accuracy():
    df = get_pages_data(10, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OffTarget', 'OnPost', 'OnTarget', 'Blocked', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_shoots_accuracy.csv', header=True,
              index=False)


def detailed_shoots_body_part():
    df = get_pages_data(10, 6, 69, driver)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df.to_csv('selenium_whoscored_scrap_player_stats_detailed_shoots_body_part.csv', header=True,
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

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

search_button = driver.find_element(By.XPATH, '//*[@class="search-button"]')
driver.execute_script("arguments[0].click();", search_button)
time.sleep(1)

detailed_shoots_zones()

dropdown_subcategory = driver.find_element(By.ID, 'subcategory')
drop_subcategory = Select(dropdown_subcategory)
drop_subcategory.select_by_visible_text("Situations")
time.sleep(2)

detailed_shoots_situations()

drop_subcategory.select_by_visible_text("Accuracy")
time.sleep(2)

detailed_shoots_accuracy()

drop_subcategory.select_by_visible_text("Body Parts")
time.sleep(2)

detailed_shoots_body_part()


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
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_zones" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OutOfBox" STRING , "SixYardBox" STRING , "PenaltyArea" STRING , "Rating" STRING )'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_shoots_zones.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_zones")


cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_situations" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OpenPlay" STRING , "Counter" STRING , "SetPiece" STRING , "PenaltyTaken" STRING , "Rating" STRING )'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_shoots_situations.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_situations")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_accuracy" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OffTarget" STRING , "OnPost" STRING , "OnTarget" STRING , "Blocked" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_shoots_accuracy.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_accuracy")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_body_part" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "RightFoot" STRING , "LeftFoot" STRING , "Head" STRING , "Other" STRING , "Rating" STRING)'
)
df = pd.read_csv("selenium_whoscored_scrap_player_stats_detailed_shoots_body_part.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_body_part")