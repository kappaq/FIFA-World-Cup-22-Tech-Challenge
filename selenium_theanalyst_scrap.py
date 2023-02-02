from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import pandas as pd 
import time
import re


dict_res = defaultdict(list)
dict_res_gk = defaultdict(list)

PATH = 'Downloads\\chromedriver'
driver = webdriver.Chrome(PATH)

wait = WebDriverWait(driver, 10)

driver.get('https://dataviz.theanalyst.com/fifa-world-cup-2022/')
time.sleep(1)

def gk_function():
    list_header_gk = []
    j = 0
    k = 0
    headers_gk = driver.find_elements(By.XPATH, ('//*[@id="root"]/div/div/div/div[4]/div[2]/div[2]/div[2]/table/thead/tr'))
    for header_gk in headers_gk:
        list_header_gk.append(header_gk)
        split_list_header_gk = list_header_gk[j].text.split()
        j = j+1
        split_list_header_gk[1:3] = ['-'.join(split_list_header_gk[1:3])]
        split_list_header_gk[2:4] = ['-'.join(split_list_header_gk[2:4])]
        split_list_header_gk[3:5] = ['-'.join(split_list_header_gk[3:5])]
        split_list_header_gk[4:6] = ['-'.join(split_list_header_gk[4:6])]
        split_list_header_gk[5:8] = ['-'.join(split_list_header_gk[5:8])]
        split_list_header_gk[6:8] = ['-'.join(split_list_header_gk[6:8])]

    goalkeepers = driver.find_elements(By.CLASS_NAME, ('NSFMbBzuHrufmLlei2bm '))
    for gk in goalkeepers:
        split_list_gk = goalkeepers[k].text.split()
        k = k+1
        regex_gk = re.compile("[A-Za-z_À-ÿ]+")
        data_gk = [s for s in split_list_gk if regex_gk.match(s)]
        data_final_gk = ' '.join(map(str, data_gk))
        dict_res_gk[split_list_header_gk[0]].append(data_final_gk)
        list_no_name_gk = [i for i in split_list_gk if i not in data_gk]
        dict_res_gk[split_list_header_gk[1]].append(list_no_name_gk[0])
        dict_res_gk[split_list_header_gk[2]].append(list_no_name_gk[1])
        dict_res_gk[split_list_header_gk[3]].append(list_no_name_gk[2])
        dict_res_gk[split_list_header_gk[4]].append(list_no_name_gk[3])
        dict_res_gk[split_list_header_gk[5]].append(list_no_name_gk[4])
        dict_res_gk[split_list_header_gk[6]].append(list_no_name_gk[5])

def player_function():
    list_header_player = []
    n = 0
    m = 0
    headers = driver.find_elements(By.XPATH, ('//*[@id="root"]/div/div/div/div[4]/div[2]/div[2]/div[2]/table/thead/tr[2]'))
    for header in headers:
        list_header_player.append(header)
        split_list_header_pleayer = list_header_player[n].text.split()
        n = n+1
        split_list_header_pleayer[1:3] = ['-'.join(split_list_header_pleayer[1:3])]
        split_list_header_pleayer[6:8] = ['-'.join(split_list_header_pleayer[6:8])]
        split_list_header_pleayer[10:12] = ['-'.join(split_list_header_pleayer[10:12])]
        split_list_header_pleayer[11:13] = ['-'.join(split_list_header_pleayer[11:13])]
        split_list_header_pleayer[20:22] = ['-'.join(split_list_header_pleayer[20:22])]


    players = driver.find_elements(By.CLASS_NAME, ('NSFMbBzuHrufmLlei2bm'))
    for player in players:
        split_list_player = players[m].text.split()
        m = m+1
        p = re.compile("[A-Za-z_À-ÿ]+")
        data_player = [s for s in split_list_player if p.match(s)]
        data_final_player = ' '.join(map(str, data_player))
        dict_res[split_list_header_pleayer[0]].append(data_final_player)
        list_no_name_player = [i for i in split_list_player if i not in data_player]
        dict_res[split_list_header_pleayer[1]].append(list_no_name_player[0])
        dict_res[split_list_header_pleayer[2]].append(list_no_name_player[1])
        dict_res[split_list_header_pleayer[3]].append(list_no_name_player[2])
        dict_res[split_list_header_pleayer[4]].append(list_no_name_player[3])
        dict_res[split_list_header_pleayer[5]].append(list_no_name_player[4])
        dict_res[split_list_header_pleayer[6]].append(list_no_name_player[5])
        dict_res[split_list_header_pleayer[7]].append(list_no_name_player[6])
        dict_res[split_list_header_pleayer[8]].append(list_no_name_player[7])
        dict_res[split_list_header_pleayer[9]].append(list_no_name_player[8])
        dict_res[split_list_header_pleayer[10]].append(list_no_name_player[9])
        dict_res[split_list_header_pleayer[11]].append(list_no_name_player[10])
        dict_res[split_list_header_pleayer[12]].append(list_no_name_player[11])
        dict_res[split_list_header_pleayer[13]].append(list_no_name_player[12])
        dict_res[split_list_header_pleayer[14]].append(list_no_name_player[13])
        dict_res[split_list_header_pleayer[15]].append(list_no_name_player[14])
        dict_res[split_list_header_pleayer[16]].append(list_no_name_player[15])
        dict_res[split_list_header_pleayer[17]].append(list_no_name_player[16])
        dict_res[split_list_header_pleayer[18]].append(list_no_name_player[17])
        dict_res[split_list_header_pleayer[19]].append(list_no_name_player[18])
        dict_res[split_list_header_pleayer[20]].append(list_no_name_player[19])
player_stats = driver.find_element(By.XPATH, '//*[@id="Player Stats"]')
driver.execute_script("arguments[0].click();", player_stats)
time.sleep(1)
player_function()

for page in range(26):
    next_page = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[4]/div[2]/div[2]/div[3]/button[2]')
    driver.execute_script("arguments[0].click();", next_page)
    time.sleep(1)
    player_function()

df_res = pd.DataFrame(dict_res)
df_res.to_csv('selenium_theanalyst_scrap_player.csv',header=True)

gk_stats = driver.find_element(By.XPATH, '//*[@id="goalkeepers"]')
driver.execute_script("arguments[0].click();", gk_stats)
time.sleep(1) 
gk_function()

next_page = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[4]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
gk_function()

df_res_gk = pd.DataFrame(dict_res_gk)
df_res_gk.to_csv('selenium_theanalyst_scrap_gk.csv',header=True)
