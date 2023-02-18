from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from snowflake.connector.pandas_tools import write_pandas
from collections import defaultdict
from itertools import islice
import time
import pandas as pd 
import time
import re
import snowflake.connector

ctx = snowflake.connector.connect(
    user='KAPPAQ',
    password='Divine123!',
    account='ze71073',
    warehouse = 'COMPUTE_WH',
    region = 'eu-central-1',
    schema = 'PUBLIC'
    )
cs = ctx.cursor()

cs.execute('USE WAREHOUSE COMPUTE_WH')
cs.execute('USE ROLE SYSADMIN')
cs.execute('CREATE DATABASE IF NOT EXISTS WORLD_CUP_22_CHALLENGE')
cs.execute('USE DATABASE WORLD_CUP_22_CHALLENGE')
cs.execute('USE SCHEMA PUBLIC')
cs.execute('CREATE OR REPLACE TABLE "team_stats_aerial" ( "No." STRING,"Team" STRING,"Total" STRING,"Won" STRING,"Lost" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_assists" ( "No." STRING,"Team" STRING,"Cross" STRING,"Corner" STRING,"Throughball" STRING,"Freekick" STRING,"Throwin" STRING,"Other" STRING,"Total" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_summary" ("No." STRING,"Team" STRING,"Goals" STRING,"Shoot-pg" STRING,"Discipline" STRING,"Possession%" STRING,"Pass%" STRING,"AerialsWon" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_defensive" ("No." STRING,"Team" STRING,"Shots-pg" STRING,"Tackles-pg" STRING,"Interceptions-pg" STRING,"Fouls-pg" STRING,"Offsides-pg" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_ofensive" ("No." STRING,"Team" STRING,"Shots-pg" STRING,"Shots-OT-pg" STRING,"Dribbles-pg" STRING,"Fouled-pg" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_shoot_zones" ("No." STRING,"Team" STRING,"Total" STRING,"OutOfBox" STRING,"SixYardBox" STRING,"PenaltyArea" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_shoot_situations" ("No." STRING,"Team" STRING,"Total" STRING,"OpenPlay" STRING,"Counter" STRING,"SetPiece" STRING,"PenaltyTaken" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_shoot_accuracy" ("No." STRING,"Team" STRING,"Total" STRING,"OffTarget" STRING,"OnPost" STRING,"OnTarget" STRING,"Blocked" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_shoot_body_part" ("No." STRING,"Team" STRING,"Total" STRING,"RightFoot" STRING,"LeftFoot" STRING,"Head" STRING,"Other" STRING,"Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_goal_zone" ("No." STRING, "Team" STRING, "Total" STRING, "SixYardBox" STRING, "PenaltyArea" STRING, "OutOfBox" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_goal_situations" ("No." STRING, "Team" STRING, "Total" STRING, "OpenPlay" STRING, "Counter" STRING, "SetPiece" STRING, "PenaltyScored" STRING, "Own" STRING, "Normal" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_goal_body_part" ("No." STRING, "Team" STRING, "Total" STRING, "RightFoot" STRING, "LeftFoot" STRING, "Head" STRING, "Other" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_dribbles" ("No." STRING, "Team" STRING, "Unsuccessful" STRING, "Successful" STRING, "Total-Dribbles" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_possesion_lose" ("No." STRING, "Team" STRING, "UnsuccessfulTouches" STRING, "Dispossessed" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_passes_length" ("No." STRING, "Team" STRING, "Total" STRING, "AccLB" STRING, "InAccLB" STRING, "AccSP" STRING, "InAccSP" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_passes_type" ("No." STRING, "Team" STRING, "AccCr" STRING, "InAccCr" STRING, "AccCrn" STRING, "InAccCrn" STRING, "AccFrK" STRING, "InAccFrK" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_key_passes_length" ("No." STRING, "Team" STRING, "Total" STRING, "Long" STRING, "Short" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_key_passes_type" ("No." STRING, "Team" STRING, "Cross" STRING, "Corner" STRING, "Throughball" STRING, "Freekick" STRING, "Throwin" STRING, "Other" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_tackles" ("No." STRING, "Team" STRING, "TotalTackles" STRING, "DribbledPast" STRING, "TotalAttemptedTackles" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_interception" ("No." STRING, "Team" STRING, "Total" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_fouls" ("No." STRING, "Team" STRING, "Fouled" STRING, "Fouls" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_cards" ("No." STRING, "Team" STRING, "Yellow" STRING, "Red" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_offside" ("No." STRING, "Team" STRING, "CaughtOffside" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_clearances" ("No." STRING, "Team" STRING, "Total" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_blocks" ("No." STRING, "Team" STRING, "ShotsBlocked" STRING, "CrossessBlocked" STRING, "PassesBlocked" STRING, "Rating" STRING)')
cs.execute('CREATE OR REPLACE TABLE "team_stats_saves" ("No." STRING, "Team" STRING, "Total" STRING, "SixYardBox" STRING, "PenaltyArea" STRING, "OutOfBox" STRING, "Rating" STRING)')


driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)

wait = WebDriverWait(driver, 10)

driver.get('https://www.whoscored.com/Regions/247/Tournaments/36/Seasons/8213/Stages/18657/TeamStatistics/International-FIFA-World-Cup-2022')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(2)

def summary():
    data_table = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table = []
    j = 0
    for data in data_table:
        list_data_table.append(data)
        split_data_table = list_data_table[j].text.split()
        j = j+1
    split_data_table[181:183] = ['-'.join(split_data_table[181:183])]
    split_data_table[226:228] = ['-'.join(split_data_table[226:228])]
    split_data_table[253:255] = ['-'.join(split_data_table[253:255])]
    length_to_split = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    Inputt = iter(split_data_table)
    Output = [list(islice(Inputt, elem)) for elem in length_to_split]
    df = pd.DataFrame(Output)
    df.columns = ['No.', 'Team', 'Goals', 'Shoot-pg', 'Discipline', 'Possession%', 'Pass%', 'AerialsWon', 'Rating']
    df.to_csv('selenium_whoscored_scrap_team_stats_summary.csv',header=True, index=False)
    write_pandas(ctx,df,table_name="team_stats_summary")
summary()

defensive_button = driver.find_element(By.XPATH, '//*[@id="stage-team-stats-options"]/li[2]/a')
driver.execute_script("arguments[0].click();", defensive_button)
time.sleep(1)

def deffense():
    data_table_def = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_def = []
    k = 0
    for data_def in data_table_def:
        list_data_table_def.append(data_def)
        split_data_table_def = list_data_table_def[k].text.split()
        k = k+1
    split_data_table_def[161:163] = ['-'.join(split_data_table_def[161:163])]
    split_data_table_def[201:203] = ['-'.join(split_data_table_def[201:203])]
    split_data_table_def[225:227] = ['-'.join(split_data_table_def[225:227])]
    length_to_split_def = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_def = iter(split_data_table_def)
    Output_def = [list(islice(Inputt_def, elem_def)) for elem_def in length_to_split_def]
    df_def = pd.DataFrame(Output_def)
    df_def.columns = ['No.', 'Team', 'Shots-pg', 'Tackles-pg', 'Interceptions-pg', 'Fouls-pg', 'Offsides-pg', 'Rating',]
    df_def.to_csv('selenium_whoscored_scrap_team_stats_deffensive.csv',header=True, index=False)
    write_pandas(ctx,df_def,table_name="team_stats_defensive")
deffense()

offensive_button = driver.find_element(By.XPATH, '//*[@id="stage-team-stats-options"]/li[3]/a')
driver.execute_script("arguments[0].click();", offensive_button)
time.sleep(3)

driver.refresh()
time.sleep(3)

offensive_button = driver.find_element(By.XPATH, '//*[@id="stage-team-stats-options"]/li[3]/a')
driver.execute_script("arguments[0].click();", offensive_button)
time.sleep(3)

def offensive():
    data_table_off = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_off = []
    l = 0
    for data_off in data_table_off:
        list_data_table_off.append(data_off)
        split_data_table_off = list_data_table_off[l].text.split()
        l = l+1
    split_data_table_off[141:143] = ['-'.join(split_data_table_off[141:143])]
    split_data_table_off[176:178] = ['-'.join(split_data_table_off[176:178])]
    split_data_table_off[197:199] = ['-'.join(split_data_table_off[197:199])]
    length_to_split_off = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    Inputt_off = iter(split_data_table_off)
    Output_off = [list(islice(Inputt_off, elem_off)) for elem_off in length_to_split_off]
    df_off = pd.DataFrame(Output_off)
    df_off.columns = ['No.', 'Team', 'Shots-pg', 'Shots-OT-pg', 'Dribbles-pg', 'Fouled-pg', 'Rating']
    df_off.to_csv('selenium_whoscored_scrap_team_stats_offensive.csv',header=True, index=False)
    write_pandas(ctx,df_off,table_name="team_stats_ofensive")
offensive()

detail_button = driver.find_element(By.XPATH, '//*[@id="stage-team-stats-options"]/li[4]/a')
driver.execute_script("arguments[0].click();", detail_button)
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_shoots_zones():
    data_table_shoot_zone = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_shoot_zone = []
    l = 0
    for data_shoot_zone in data_table_shoot_zone:
        list_data_table_shoot_zone.append(data_shoot_zone)
        split_data_table_shoot_zone = list_data_table_shoot_zone[l].text.split()
        l = l+1
    split_data_table_shoot_zone[141:143] = ['-'.join(split_data_table_shoot_zone[141:143])]
    split_data_table_shoot_zone[176:178] = ['-'.join(split_data_table_shoot_zone[176:178])]
    split_data_table_shoot_zone[197:199] = ['-'.join(split_data_table_shoot_zone[197:199])]
    length_to_split_shoot_zone = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    Inputt_shoot_zone = iter(split_data_table_shoot_zone)
    Output_shoot_zone = [list(islice(Inputt_shoot_zone, elem_shoot_zone)) for elem_shoot_zone in length_to_split_shoot_zone]
    df_shoot_zone = pd.DataFrame(Output_shoot_zone)
    df_shoot_zone.columns = ['No.', 'Team', 'Total', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']
    df_shoot_zone.to_csv('selenium_whoscored_scrap_team_stats_shoot_zone.csv',header=True, index=False)
    write_pandas(ctx,df_shoot_zone,table_name="team_stats_shoot_zones")
detailed_shoots_zones()

dropdown_subcategory = driver.find_element(By.ID, 'subcategory')
drop_subcategory = Select(dropdown_subcategory)
drop_subcategory.select_by_visible_text("Situations")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_shoots_situations():
    data_table_shoot_situation = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_shoot_situation = []
    l = 0
    for data_shoot_situation in data_table_shoot_situation:
        list_data_table_shoot_situation.append(data_shoot_situation)
        split_data_table_shoot_situation = list_data_table_shoot_situation[l].text.split()
        l = l+1
    split_data_table_shoot_situation[161:163] = ['-'.join(split_data_table_shoot_situation[161:163])]
    split_data_table_shoot_situation[201:203] = ['-'.join(split_data_table_shoot_situation[201:203])]
    split_data_table_shoot_situation[225:227] = ['-'.join(split_data_table_shoot_situation[225:227])]
    length_to_split_shoot_situation = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_shoot_situation = iter(split_data_table_shoot_situation)
    Output_shoot_situation = [list(islice(Inputt_shoot_situation, elem_shoot_situation)) for elem_shoot_situation in length_to_split_shoot_situation]
    df_shoot_situation = pd.DataFrame(Output_shoot_situation)
    df_shoot_situation.columns = ['No.', 'Team', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyTaken', 'Rating']
    df_shoot_situation.to_csv('selenium_whoscored_scrap_team_stats_shoot_situation.csv',header=True, index=False)
    write_pandas(ctx,df_shoot_situation,table_name="team_stats_shoot_situations")
detailed_shoots_situations()

drop_subcategory.select_by_visible_text("Accuracy")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_shoots_accuracy():
    data_table_shoot_accuracy = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_shoot_accuracy = []
    l = 0
    for data_shoot_accuracy in data_table_shoot_accuracy:
        list_data_table_shoot_accuracy.append(data_shoot_accuracy)
        split_data_table_shoot_accuracy = list_data_table_shoot_accuracy[l].text.split()
        l = l+1
    split_data_table_shoot_accuracy[161:163] = ['-'.join(split_data_table_shoot_accuracy[161:163])]
    split_data_table_shoot_accuracy[201:203] = ['-'.join(split_data_table_shoot_accuracy[201:203])]
    split_data_table_shoot_accuracy[225:227] = ['-'.join(split_data_table_shoot_accuracy[225:227])]
    length_to_split_shoot_accuracy = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_shoot_accuracy = iter(split_data_table_shoot_accuracy)
    Output_shoot_accuracy = [list(islice(Inputt_shoot_accuracy, elem_shoot_accuracy)) for elem_shoot_accuracy in length_to_split_shoot_accuracy]
    df_shoot_accuracy = pd.DataFrame(Output_shoot_accuracy)
    df_shoot_accuracy.columns = ['No.', 'Team', 'Total', 'OffTarget', 'OnPost', 'OnTarget', 'Blocked', 'Rating']
    df_shoot_accuracy.to_csv('selenium_whoscored_scrap_team_stats_shoot_accuracy.csv',header=True, index=False)
    write_pandas(ctx,df_shoot_accuracy,table_name="team_stats_shoot_accuracy")
detailed_shoots_accuracy()

drop_subcategory.select_by_visible_text("Body Parts")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_shoots_body_part():
    data_table_shoot_body_part = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_shoot_body_part = []
    l = 0
    for data_shoot_body_part in data_table_shoot_body_part:
        list_data_table_shoot_body_part.append(data_shoot_body_part)
        split_data_table_shoot_body_part = list_data_table_shoot_body_part[l].text.split()
        l = l+1
    split_data_table_shoot_body_part[161:163] = ['-'.join(split_data_table_shoot_body_part[161:163])]
    split_data_table_shoot_body_part[201:203] = ['-'.join(split_data_table_shoot_body_part[201:203])]
    split_data_table_shoot_body_part[225:227] = ['-'.join(split_data_table_shoot_body_part[225:227])]
    length_to_split_shoot_body_part = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_shoot_body_part = iter(split_data_table_shoot_body_part)
    Output_shoot_body_part = [list(islice(Inputt_shoot_body_part, elem_shoot_body_part)) for elem_shoot_body_part in length_to_split_shoot_body_part]
    df_shoot_body_part = pd.DataFrame(Output_shoot_body_part)
    df_shoot_body_part.columns = ['No.', 'Team', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df_shoot_body_part.to_csv('selenium_whoscored_scrap_team_stats_shoot_body_part.csv',header=True, index=False)
    write_pandas(ctx,df_shoot_body_part,table_name="team_stats_shoot_body_part")
detailed_shoots_body_part()

dropdown_category = driver.find_element(By.ID, 'category')
drop_category = Select(dropdown_category)
drop_category.select_by_visible_text("Goals")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_goal_zone():
    data_table_goal_zone = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_goal_zone = []
    l = 0
    for data_goal_zone in data_table_goal_zone:
        list_data_table_goal_zone.append(data_goal_zone)
        split_data_table_goal_zone = list_data_table_goal_zone[l].text.split()
        l = l+1
    split_data_table_goal_zone[141:143] = ['-'.join(split_data_table_goal_zone[141:143])]
    split_data_table_goal_zone[176:178] = ['-'.join(split_data_table_goal_zone[176:178])]
    split_data_table_goal_zone[197:199] = ['-'.join(split_data_table_goal_zone[197:199])]
    length_to_split_goal_zone = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    Inputt_goal_zone = iter(split_data_table_goal_zone)
    Output_goal_zone = [list(islice(Inputt_goal_zone, elem_goal_zone)) for elem_goal_zone in length_to_split_goal_zone]
    df_goal_zone = pd.DataFrame(Output_goal_zone)
    df_goal_zone.columns = ['No.', 'Team', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']
    df_goal_zone.to_csv('selenium_whoscored_scrap_team_stats_goal_zone.csv',header=True, index=False)
    write_pandas(ctx,df_goal_zone,table_name="team_stats_goal_zone")
detailed_goal_zone()

drop_subcategory.select_by_visible_text("Situations")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_goal_situations():
    data_table_goal_situations = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_goal_situations = []
    l = 0
    for data_goal_situations in data_table_goal_situations:
        list_data_table_goal_situations.append(data_goal_situations)
        split_data_table_goal_situations = list_data_table_goal_situations[l].text.split()
        l = l+1
    split_data_table_goal_situations[201:203] = ['-'.join(split_data_table_goal_situations[201:203])]
    split_data_table_goal_situations[251:253] = ['-'.join(split_data_table_goal_situations[251:253])]
    split_data_table_goal_situations[281:283] = ['-'.join(split_data_table_goal_situations[281:283])]
    length_to_split_goal_situations = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    Inputt_goal_situations = iter(split_data_table_goal_situations)
    Output_goal_situations = [list(islice(Inputt_goal_situations, elem_goal_situations)) for elem_goal_situations in length_to_split_goal_situations]
    df_goal_situations = pd.DataFrame(Output_goal_situations)
    df_goal_situations.columns = ['No.', 'Team', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyScored', 'Own', 'Normal', 'Rating',]
    df_goal_situations.to_csv('selenium_whoscored_scrap_team_stats_goal_situations.csv',header=True, index=False)
    write_pandas(ctx,df_goal_situations,table_name="team_stats_goal_situations")
detailed_goal_situations()

drop_subcategory.select_by_visible_text("Body Parts")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_goal_body_part():
    data_table_goal_body_part = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_goal_body_part = []
    l = 0
    for data_goal_body_part in data_table_goal_body_part:
        list_data_table_goal_body_part.append(data_goal_body_part)
        split_data_table_goal_body_part = list_data_table_goal_body_part[l].text.split()
        l = l+1
    split_data_table_goal_body_part[161:163] = ['-'.join(split_data_table_goal_body_part[161:163])]
    split_data_table_goal_body_part[201:203] = ['-'.join(split_data_table_goal_body_part[201:203])]
    split_data_table_goal_body_part[225:227] = ['-'.join(split_data_table_goal_body_part[225:227])]
    length_to_split_goal_body_part = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_goal_body_part = iter(split_data_table_goal_body_part)
    Output_goal_body_part = [list(islice(Inputt_goal_body_part, elem_goal_body_part)) for elem_goal_body_part in length_to_split_goal_body_part]
    df_goal_body_part = pd.DataFrame(Output_goal_body_part)
    df_goal_body_part.columns = ['No.', 'Team', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating',]
    df_goal_body_part.to_csv('selenium_whoscored_scrap_team_stats_goal_body_part.csv',header=True, index=False)
    write_pandas(ctx,df_goal_body_part,table_name="team_stats_goal_body_part")
detailed_goal_body_part()

drop_category.select_by_visible_text("Dribbles")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_dribbles():
    data_table_dribbles = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_dribbles = []
    l = 0
    for data_dribbles in data_table_dribbles:
        list_data_table_dribbles.append(data_dribbles)
        split_data_table_dribbles = list_data_table_dribbles[l].text.split()
        l = l+1
    split_data_table_dribbles[121:123] = ['-'.join(split_data_table_dribbles[121:123])]
    split_data_table_dribbles[151:153] = ['-'.join(split_data_table_dribbles[151:153])]
    split_data_table_dribbles[169:171] = ['-'.join(split_data_table_dribbles[169:171])]
    length_to_split_dribbles = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    Inputt_dribbles = iter(split_data_table_dribbles)
    Output_dribbles = [list(islice(Inputt_dribbles, elem_dribbles)) for elem_dribbles in length_to_split_dribbles]
    df_dribbles = pd.DataFrame(Output_dribbles)
    df_dribbles.columns = ['No.', 'Team', 'Unsuccessful', 'Successful', 'Total-Dribbles', 'Rating',]
    df_dribbles.to_csv('selenium_whoscored_scrap_team_stats_dribbles.csv',header=True, index=False)
    write_pandas(ctx,df_dribbles,table_name="team_stats_dribbles")
detailed_dribbles()

drop_category.select_by_visible_text("Possession loss")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_possesion_lose():
    data_table_possesion_lose = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_possesion_lose = []
    l = 0
    for data_possesion_lose in data_table_possesion_lose:
        list_data_table_possesion_lose.append(data_possesion_lose)
        split_data_table_possesion_lose = list_data_table_possesion_lose[l].text.split()
        l = l+1
    split_data_table_possesion_lose[101:103] = ['-'.join(split_data_table_possesion_lose[101:103])]
    split_data_table_possesion_lose[126:128] = ['-'.join(split_data_table_possesion_lose[126:128])]
    split_data_table_possesion_lose[141:143] = ['-'.join(split_data_table_possesion_lose[141:143])]
    length_to_split_possesion_lose = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    Inputt_possesion_lose = iter(split_data_table_possesion_lose)
    Output_possesion_lose = [list(islice(Inputt_possesion_lose, elem_possesion_lose)) for elem_possesion_lose in length_to_split_possesion_lose]
    df_possesion_lose = pd.DataFrame(Output_possesion_lose)
    df_possesion_lose.columns = ['No.', 'Team', 'UnsuccessfulTouches', 'Dispossessed', 'Rating',]
    df_possesion_lose.to_csv('selenium_whoscored_scrap_team_stats_possesion_lose.csv',header=True, index=False)
    write_pandas(ctx,df_possesion_lose,table_name="team_stats_possesion_lose")
detailed_possesion_lose()

drop_category.select_by_visible_text("Aerial")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_aerial():
    data_table_aerial = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_aerial = []
    l = 0
    for data_aerial in data_table_aerial:
        list_data_table_aerial.append(data_aerial)
        split_data_table_aerial = list_data_table_aerial[l].text.split()
        l = l+1
    split_data_table_aerial[121:123] = ['-'.join(split_data_table_aerial[121:123])]
    split_data_table_aerial[151:153] = ['-'.join(split_data_table_aerial[151:153])]
    split_data_table_aerial[169:171] = ['-'.join(split_data_table_aerial[169:171])]
    length_to_split_aerial = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    Inputt_aerial = iter(split_data_table_aerial)
    Output_aerial = [list(islice(Inputt_aerial, elem_aerial)) for elem_aerial in length_to_split_aerial]
    df_aerial = pd.DataFrame(Output_aerial)
    df_aerial.columns = ['No.', 'Team', 'Total', 'Won', 'Lost', 'Rating',]
    df_aerial.to_csv('selenium_whoscored_scrap_team_stats_aerial.csv',header=True, index=False)
    write_pandas(ctx,df_aerial,table_name="team_stats_aerial")
detailed_aerial()

drop_category.select_by_visible_text("Passes")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_passes_length():
    data_table_passes_length = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_passes_length = []
    l = 0
    for data_passes_length in data_table_passes_length:
        list_data_table_passes_length.append(data_passes_length)
        split_data_table_passes_length = list_data_table_passes_length[l].text.split()
        l = l+1
    split_data_table_passes_length[161:163] = ['-'.join(split_data_table_passes_length[161:163])]
    split_data_table_passes_length[201:203] = ['-'.join(split_data_table_passes_length[201:203])]
    split_data_table_passes_length[225:227] = ['-'.join(split_data_table_passes_length[225:227])]
    length_to_split_passes_length = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    Inputt_passes_length = iter(split_data_table_passes_length)
    Output_passes_length = [list(islice(Inputt_passes_length, elem_passes_length)) for elem_passes_length in length_to_split_passes_length]
    df_passes_length = pd.DataFrame(Output_passes_length)
    df_passes_length.columns = ['No.', 'Team', 'Total', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating',]
    df_passes_length.to_csv('selenium_whoscored_scrap_team_stats_passes_length.csv',header=True, index=False)
    write_pandas(ctx,df_passes_length,table_name="team_stats_passes_length")
detailed_passes_length()

drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_passes_type():
    data_table_passes_type = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_passes_type = []
    l = 0
    for data_passes_type in data_table_passes_type:
        list_data_table_passes_type.append(data_passes_type)
        split_data_table_passes_type = list_data_table_passes_type[l].text.split()
        l = l+1
    split_data_table_passes_type[181:183] = ['-'.join(split_data_table_passes_type[181:183])]
    split_data_table_passes_type[226:228] = ['-'.join(split_data_table_passes_type[226:228])]
    split_data_table_passes_type[253:255] = ['-'.join(split_data_table_passes_type[253:255])]
    length_to_split_passes_type = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    Inputt_passes_type = iter(split_data_table_passes_type)
    Output_passes_type = [list(islice(Inputt_passes_type, elem_passes_type)) for elem_passes_type in length_to_split_passes_type]
    df_passes_type = pd.DataFrame(Output_passes_type)
    df_passes_type.columns = ['No.', 'Team', 'AccCr', 'InAccCr', 'AccCrn', 'InAccCrn', 'AccFrK', 'InAccFrK', 'Rating',]
    df_passes_type.to_csv('selenium_whoscored_scrap_team_stats_passes_type.csv',header=True, index=False)
    write_pandas(ctx,df_passes_type,table_name="team_stats_passes_type")
detailed_passes_type()

drop_category.select_by_visible_text("Key passes")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_key_passes_length():
    data_table_key_passes_length = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_key_passes_length = []
    l = 0
    for data_key_passes_length in data_table_key_passes_length:
        list_data_table_key_passes_length.append(data_key_passes_length)
        split_data_table_key_passes_length = list_data_table_key_passes_length[l].text.split()
        l = l+1
    split_data_table_key_passes_length[121:123] = ['-'.join(split_data_table_key_passes_length[121:123])]
    split_data_table_key_passes_length[151:153] = ['-'.join(split_data_table_key_passes_length[151:153])]
    split_data_table_key_passes_length[169:171] = ['-'.join(split_data_table_key_passes_length[169:171])]
    length_to_split_key_passes_length = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    Inputt_key_passes_length = iter(split_data_table_key_passes_length)
    Output_key_passes_length = [list(islice(Inputt_key_passes_length, elem_key_passes_length)) for elem_key_passes_length in length_to_split_key_passes_length]
    df_key_passes_length = pd.DataFrame(Output_key_passes_length)
    df_key_passes_length.columns = ['No.', 'Team', 'Total', 'Long', 'Short', 'Rating']
    df_key_passes_length.to_csv('selenium_whoscored_scrap_team_stats_key_passes_length.csv',header=True, index=False)
    write_pandas(ctx,df_key_passes_length,table_name="team_stats_key_passes_length")
detailed_key_passes_length()

drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_key_passes_type():
    data_table_key_passes_type = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_key_passes_type = []
    l = 0
    for data_key_passes_type in data_table_key_passes_type:
        list_data_table_key_passes_type.append(data_key_passes_type)
        split_data_table_key_passes_type = list_data_table_key_passes_type[l].text.split()
        l = l+1
    split_data_table_key_passes_type[181:183] = ['-'.join(split_data_table_key_passes_type[181:183])]
    split_data_table_key_passes_type[226:228] = ['-'.join(split_data_table_key_passes_type[226:228])]
    split_data_table_key_passes_type[253:255] = ['-'.join(split_data_table_key_passes_type[253:255])]
    length_to_split_key_passes_type = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    Inputt_key_passes_type = iter(split_data_table_key_passes_type)
    Output_key_passes_type = [list(islice(Inputt_key_passes_type, elem_key_passes_type)) for elem_key_passes_type in length_to_split_key_passes_type]
    df_key_passes_type = pd.DataFrame(Output_key_passes_type)
    df_key_passes_type.columns = ['No.', 'Team', 'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin', 'Other', 'Rating']
    df_key_passes_type.to_csv('selenium_whoscored_scrap_team_stats_key_passes_type.csv',header=True, index=False)
    write_pandas(ctx,df_key_passes_type,table_name="team_stats_key_passes_type")
detailed_key_passes_type()

drop_category.select_by_visible_text("Assists")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_assists():
    data_table_assists = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_assists = []
    l = 0
    for data_assists in data_table_assists:
        list_data_table_assists.append(data_assists)
        split_data_table_assists = list_data_table_assists[l].text.split()
        l = l+1
    split_data_table_assists[201:203] = ['-'.join(split_data_table_assists[201:203])]
    split_data_table_assists[251:253] = ['-'.join(split_data_table_assists[251:253])]
    split_data_table_assists[281:283] = ['-'.join(split_data_table_assists[281:283])]
    length_to_split_assists = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    Inputt_assists = iter(split_data_table_assists)
    Output_assists = [list(islice(Inputt_assists, elem_assists)) for elem_assists in length_to_split_assists]
    df_assists = pd.DataFrame(Output_assists)
    df_assists.columns = ['No.', 'Team', 'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin', 'Other', 'Total', 'Rating']
    df_assists.to_csv('selenium_whoscored_scrap_team_stats_assists.csv',header=True, index=False)
    write_pandas(ctx,df_assists,table_name="team_stats_assists")
detailed_assists()

drop_category.select_by_visible_text("Tackles")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_tackles():
    data_table_tackles = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_tackles = []
    l = 0
    for data_tackles in data_table_tackles:
        list_data_table_tackles.append(data_tackles)
        split_data_table_tackles = list_data_table_tackles[l].text.split()
        l = l+1
    split_data_table_tackles[121:123] = ['-'.join(split_data_table_tackles[121:123])]
    split_data_table_tackles[151:153] = ['-'.join(split_data_table_tackles[151:153])]
    split_data_table_tackles[169:171] = ['-'.join(split_data_table_tackles[169:171])]
    length_to_split_tackles = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    Inputt_tackles = iter(split_data_table_tackles)
    Output_tackles = [list(islice(Inputt_tackles, elem_tackles)) for elem_tackles in length_to_split_tackles]
    df_tackles = pd.DataFrame(Output_tackles)
    df_tackles.columns = ['No.', 'Team', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles', 'Rating']
    df_tackles.to_csv('selenium_whoscored_scrap_team_stats_tackles.csv',header=True, index=False)
    write_pandas(ctx,df_tackles,table_name="team_stats_tackles")
detailed_tackles()

drop_category.select_by_visible_text("Interception")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_interception():
    data_table_interception = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_interception = []
    l = 0
    for data_interception in data_table_interception:
        list_data_table_interception.append(data_interception)
        split_data_table_interception = list_data_table_interception[l].text.split()
        l = l+1
    split_data_table_interception[81:83] = ['-'.join(split_data_table_interception[81:83])] #20
    split_data_table_interception[101:103] = ['-'.join(split_data_table_interception[101:103])] #25
    split_data_table_interception[113:115] = ['-'.join(split_data_table_interception[113:115])] #28
    length_to_split_interception = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    Inputt_interception = iter(split_data_table_interception)
    Output_interception = [list(islice(Inputt_interception, elem_interception)) for elem_interception in length_to_split_interception]
    df_interception = pd.DataFrame(Output_interception)
    df_interception.columns = ['No.', 'Team', 'Total', 'Rating']
    df_interception.to_csv('selenium_whoscored_scrap_team_stats_interception.csv',header=True, index=False)
    write_pandas(ctx,df_interception,table_name="team_stats_interception")
detailed_interception()

drop_category.select_by_visible_text("Fouls")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_fouls():
    data_table_fouls = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_fouls = []
    l = 0
    for data_fouls in data_table_fouls:
        list_data_table_fouls.append(data_fouls)
        split_data_table_fouls = list_data_table_fouls[l].text.split()
        l = l+1
    split_data_table_fouls[101:103] = ['-'.join(split_data_table_fouls[101:103])]
    split_data_table_fouls[126:128] = ['-'.join(split_data_table_fouls[126:128])]
    split_data_table_fouls[141:143] = ['-'.join(split_data_table_fouls[141:143])]
    length_to_split_fouls = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    Inputt_fouls = iter(split_data_table_fouls)
    Output_fouls = [list(islice(Inputt_fouls, elem_fouls)) for elem_fouls in length_to_split_fouls]
    df_fouls = pd.DataFrame(Output_fouls)
    df_fouls.columns = ['No.', 'Team', 'Fouled', 'Fouls', 'Rating']
    df_fouls.to_csv('selenium_whoscored_scrap_team_stats_fouls.csv',header=True, index=False)
    write_pandas(ctx,df_fouls,table_name="team_stats_fouls")
detailed_fouls()

drop_category.select_by_visible_text("Cards")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_cards():
    data_table_cards = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_cards = []
    l = 0
    for data_cards in data_table_cards:
        list_data_table_cards.append(data_cards)
        split_data_table_cards = list_data_table_cards[l].text.split()
        l = l+1
    split_data_table_cards[101:103] = ['-'.join(split_data_table_cards[101:103])]
    split_data_table_cards[126:128] = ['-'.join(split_data_table_cards[126:128])]
    split_data_table_cards[141:143] = ['-'.join(split_data_table_cards[141:143])]
    length_to_split_cards = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    Inputt_cards = iter(split_data_table_cards)
    Output_cards = [list(islice(Inputt_cards, elem_cards)) for elem_cards in length_to_split_cards]
    df_cards = pd.DataFrame(Output_cards)
    df_cards.columns = ['No.', 'Team', 'Yellow', 'Red', 'Rating']
    df_cards.to_csv('selenium_whoscored_scrap_team_stats_cards.csv',header=True, index=False)
    write_pandas(ctx,df_cards,table_name="team_stats_cards")
detailed_cards()

drop_category.select_by_visible_text("Offsides")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_offside():
    data_table_offside = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_offside = []
    l = 0
    for data_offside in data_table_offside:
        list_data_table_offside.append(data_offside)
        split_data_table_offside = list_data_table_offside[l].text.split()
        l = l+1
    split_data_table_offside[81:83] = ['-'.join(split_data_table_offside[81:83])] #20
    split_data_table_offside[101:103] = ['-'.join(split_data_table_offside[101:103])] #25
    split_data_table_offside[113:115] = ['-'.join(split_data_table_offside[113:115])] #28
    length_to_split_offside = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    Inputt_offside = iter(split_data_table_offside)
    Output_offside = [list(islice(Inputt_offside, elem_offside)) for elem_offside in length_to_split_offside]
    df_offside = pd.DataFrame(Output_offside)
    df_offside.columns = ['No.', 'Team', 'CaughtOffside', 'Rating']
    df_offside.to_csv('selenium_whoscored_scrap_team_stats_offside.csv',header=True, index=False)
    write_pandas(ctx,df_offside,table_name="team_stats_offside")
detailed_offside()

drop_category.select_by_visible_text("Clearances")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_clearances():
    data_table_clearances = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_clearances = []
    l = 0
    for data_clearances in data_table_clearances:
        list_data_table_clearances.append(data_clearances)
        split_data_table_clearances = list_data_table_clearances[l].text.split()
        l = l+1
    split_data_table_clearances[81:83] = ['-'.join(split_data_table_clearances[81:83])] #20
    split_data_table_clearances[101:103] = ['-'.join(split_data_table_clearances[101:103])] #25
    split_data_table_clearances[113:115] = ['-'.join(split_data_table_clearances[113:115])] #28
    length_to_split_clearances = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    Inputt_clearances = iter(split_data_table_clearances)
    Output_clearances = [list(islice(Inputt_clearances, elem_clearances)) for elem_clearances in length_to_split_clearances]
    df_clearances = pd.DataFrame(Output_clearances)
    df_clearances.columns = ['No.', 'Team', 'Total', 'Rating']
    df_clearances.to_csv('selenium_whoscored_scrap_team_stats_clearances.csv',header=True, index=False)
    write_pandas(ctx,df_clearances,table_name="team_stats_clearances")
detailed_clearances()

drop_category.select_by_visible_text("Blocks")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_blocks():
    data_table_blocks = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_blocks = []
    l = 0
    for data_blocks in data_table_blocks:
        list_data_table_blocks.append(data_blocks)
        split_data_table_blocks = list_data_table_blocks[l].text.split()
        l = l+1
    split_data_table_blocks[121:123] = ['-'.join(split_data_table_blocks[121:123])]
    split_data_table_blocks[151:153] = ['-'.join(split_data_table_blocks[151:153])]
    split_data_table_blocks[169:171] = ['-'.join(split_data_table_blocks[169:171])]
    length_to_split_blocks = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    Inputt_blocks = iter(split_data_table_blocks)
    Output_blocks = [list(islice(Inputt_blocks, elem_blocks)) for elem_blocks in length_to_split_blocks]
    df_blocks = pd.DataFrame(Output_blocks)
    df_blocks.columns = ['No.', 'Team', 'ShotsBlocked', 'CrossessBlocked', 'PassesBlocked', 'Rating']
    df_blocks.to_csv('selenium_whoscored_scrap_team_stats_blocks.csv',header=True, index=False)
    write_pandas(ctx,df_blocks,table_name="team_stats_blocks")
detailed_blocks()

drop_category.select_by_visible_text("Saves")
time.sleep(2)

dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

def detailed_saves():
    data_table_saves = driver.find_elements(By.XPATH, ('//*[@id="top-team-stats-summary-content"]'))
    list_data_table_saves = []
    l = 0
    for data_saves in data_table_saves:
        list_data_table_saves.append(data_saves)
        split_data_table_saves = list_data_table_saves[l].text.split()
        l = l+1
    split_data_table_saves[141:143] = ['-'.join(split_data_table_saves[141:143])]
    split_data_table_saves[176:178] = ['-'.join(split_data_table_saves[176:178])]
    split_data_table_saves[197:199] = ['-'.join(split_data_table_saves[197:199])]
    length_to_split_saves = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    Inputt_saves = iter(split_data_table_saves)
    Output_saves = [list(islice(Inputt_saves, elem_saves)) for elem_saves in length_to_split_saves]
    df_saves = pd.DataFrame(Output_saves)
    df_saves.columns = ['No.', 'Team', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']
    df_saves.to_csv('selenium_whoscored_scrap_team_stats_saves.csv',header=True, index=False)
    write_pandas(ctx,df_saves,table_name="team_stats_saves")
detailed_saves()