from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import pandas as pd 
import time
import re
from itertools import islice

PATH = 'Downloads\\chromedriver'
driver = webdriver.Chrome(PATH)

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
offensive()