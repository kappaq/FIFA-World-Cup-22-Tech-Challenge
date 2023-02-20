from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd 
import time
import re

driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)

wait = WebDriverWait(driver, 10)

team_list = []
formation_list = []

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
cs.execute('CREATE OR REPLACE TABLE "preffered_formation" ( "Team" STRING, "Formation" STRING)')

driver.get('https://www.mlssoccer.com/news/your-world-cup-guide-what-to-know-about-all-32-teams')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)

def qatar():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('//*[@id="main-content"]/section[1]/div/div/article/div[3]/div/div[6]'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('//*[@id="main-content"]/section[1]/div/div/article/div[3]/div/div[7]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
qatar()

def ecuador():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('//*[@id="main-content"]/section[1]/div/div/article/div[3]/div/div[8]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[9]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[-1]
    formation_list.append(qatar_formation)
ecuador()

def senegal():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[10]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[12]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[-1]
    formation_list.append(qatar_formation)
senegal()

def netherlands():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[13]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[14]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[8]
    formation_list.append(qatar_formation)
netherlands()

def england():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[16]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[17]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
england()

def iran():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[19]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[20]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
iran()

def usa():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[21]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[22]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
usa()

def wales():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[23]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[24]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[7]
    formation_list.append(qatar_formation)
wales()

def argentina():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[27]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[28]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[6]
    formation_list.append(qatar_formation)
argentina()

def mexico():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[29]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[30]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[9]
    formation_list.append(qatar_formation)
mexico()

def poland():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[31]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[33]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[10]
    formation_list.append(qatar_formation)
poland()

def saudi_arabia():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[34]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[35]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[11]
    formation_list.append(qatar_formation)
saudi_arabia()

def australia():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[37]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[38]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[4]
    formation_list.append(qatar_formation)
australia()

def denmark():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[40]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[41]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[6]
    formation_list.append(qatar_formation)
denmark()

def france():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[42]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[43]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[4]
    formation_list.append(qatar_formation)
france()

def tunisia():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[44]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[45]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[22]
    formation_list.append(qatar_formation)
tunisia()

def costa_rica():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[48]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[49]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[8]
    formation_list.append(qatar_formation)
costa_rica()

def germany():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[50]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[51]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
germany()

def japan():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[52]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[54]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[5]
    formation_list.append(qatar_formation)
japan()

def spain():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[55]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[56]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[3]
    formation_list.append(qatar_formation)
spain()

def belgium():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[58]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[59]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
belgium()

def canada():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[61]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[62]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
canada()

def croatia():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[63]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[64]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
croatia()

def marocco():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[65]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[66]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[19]
    formation_list.append(qatar_formation)
marocco()

def brazil():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[69]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[70]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[7]
    formation_list.append(qatar_formation)
brazil()

def cameroon():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[71]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[72]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[5]
    formation_list.append(qatar_formation)
cameroon()

def switzerland():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[73]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[75]/div[3]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
switzerland()

def ghana():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[79]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[80]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[6]
    formation_list.append(qatar_formation)
ghana()

def portugal():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[82]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[83]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[4]
    formation_list.append(qatar_formation)
portugal()

def south_korea():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[84]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[85]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[4]
    formation_list.append(qatar_formation)
south_korea()

def uruguay():
    a = []
    j = 0
    team = driver.find_element(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[86]/div/div/div[2]/div/a'))
    team_list.append(team.text)

    formation = driver.find_elements(By.XPATH, ('/html/body/div[1]/main/section[1]/div/div/article/div[3]/div/div[87]/div[2]/p'))
    for x_formation in formation:
        a.append(x_formation)
        split_formation_list = a[j].text.split()
        j = j+1
    qatar_formation = split_formation_list[2]
    formation_list.append(qatar_formation)
uruguay()

df = pd.DataFrame(list(zip(team_list, formation_list)),columns=['Team','Formation'])
df.to_csv('preffered_formation.csv',  index=False)

final_df = pd.read_csv("preffered_formation.csv", sep=",")
write_pandas(ctx,final_df,table_name="preffered_formation")