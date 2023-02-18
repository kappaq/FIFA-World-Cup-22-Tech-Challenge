from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import pandas as pd 
import time

games_round_1 = [
'//*[@id="g_1_jsidfnm5"]', '//*[@id="g_1_0G0LfGbo"]', '//*[@id="g_1_4pe0g62B"]', '//*[@id="g_1_GUm04257"]',
'//*[@id="g_1_rH3ChoZE"]', '//*[@id="g_1_p42XiEr4"]', '//*[@id="g_1_8pCMVNR1"]', '//*[@id="g_1_2ucxiYcA"]', 
'//*[@id="g_1_IJ781Sp9"]', '//*[@id="g_1_ARmio3Rl"]', '//*[@id="g_1_YXjQDWEJ"]', '//*[@id="g_1_hjgnnqCr"]', 
'//*[@id="g_1_4pXg5OIK"]', '//*[@id="g_1_GpSZeKu7"]',' //*[@id="g_1_zZAxc0Q0"]', '//*[@id="g_1_zBSk643E"]', 
'//*[@id="g_1_4psrTor8"]', '//*[@id="g_1_n9p5hQHH"]', '//*[@id="g_1_Qaq9ipXN"]', '//*[@id="g_1_Cj4PgzEi"]', 
'//*[@id="g_1_bVO50n0F"]', '//*[@id="g_1_YRJ9YPsq"]', '//*[@id="g_1_M1F3f742"]', '//*[@id="g_1_tWetjhDG"]', 
'//*[@id="g_1_COkUCjUP"]', '//*[@id="g_1_lInepNte"]', '//*[@id="g_1_runaqsd1"]', '//*[@id="g_1_dK7Gi5lL"]', 
'//*[@id="g_1_lI8Qa2tr"]', '//*[@id="g_1_8vFLJNXD"]', '//*[@id="g_1_ryWc4rYQ"]', '//*[@id="g_1_fyRweveD"]', 
'//*[@id="g_1_fZmDj4nU"]', '//*[@id="g_1_drzunOfo"]', '//*[@id="g_1_rytnS5cE"]', '//*[@id="g_1_6D3ThfTc"]', 
'//*[@id="g_1_0hE7gRJ8"]', '//*[@id="g_1_xMN9a6FL"]', '//*[@id="g_1_UgDIW3Ce"]', '//*[@id="g_1_nVNDXqck"]', 
'//*[@id="g_1_fFk3r1B7"]', '//*[@id="g_1_dKTo7pl8"]', '//*[@id="g_1_js7KjP3R"]', '//*[@id="g_1_I5Sd8Axs"]', 
'//*[@id="g_1_MsJPIsmK"]', '//*[@id="g_1_468UH12Q"]', '//*[@id="g_1_drCYctBf"]', '//*[@id="g_1_2LCUbMel"]', 
'//*[@id="g_1_ClJjw1Og"]', '//*[@id="g_1_Ya9wwgP2"]', '//*[@id="g_1_Cj8sxDv9"]', '//*[@id="g_1_bswGq3oQ"]', 
'//*[@id="g_1_MVnruykg"]', '//*[@id="g_1_A7cQ5yBg"]', '//*[@id="g_1_4fxmve4a"]', '//*[@id="g_1_GpbM6Hem"]',
'//*[@id="g_1_lGiFEPmp"]', '//*[@id="g_1_G0rn6WE5"]', '//*[@id="g_1_hdEvqxcM"]', '//*[@id="g_1_2g49AZK4"]',
'//*[@id="g_1_QXChy9gE"]', '//*[@id="g_1_M9g47WCj"]', '//*[@id="g_1_U7jo7z91"]', '//*[@id="g_1_rBfk6fO7"]'
]


lista_category = []
n = 0
driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
dict_res = defaultdict(list)

a = ActionChains(driver)
wait = WebDriverWait(driver, 10)

driver.get('https://www.flashscore.com/')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)

world_cup = driver.find_element(By.XPATH, '//*[@id="my-leagues-list"]/div[3]/div[2]/a')
driver.implicitly_wait(1)
world_cup.click()
time.sleep(1)

results = driver.find_element(By.XPATH, '//*[@id="li1"]')
driver.execute_script("arguments[0].click();", results)


for game in games_round_1:
	original_window = driver.current_window_handle
	game_1 = driver.find_element(By.XPATH, game)
	driver.execute_script("arguments[0].click();", game_1)
	wait.until(EC.number_of_windows_to_be(2))
	for window_handle in driver.window_handles:
	        if window_handle != original_window:
	            driver.switch_to.window(window_handle)
	            break
	stats = driver.find_element(By.XPATH, '//*[@id="detail"]/div[7]/div/a[2]')
	driver.execute_script("arguments[0].click();", stats)
	section = driver.find_elements(By.CLASS_NAME, ('stat__row'))
	time = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[1]')
	home_team_name = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]')
	away_team_name = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a')
	final_score = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]')
	dict_res['Time and Date'].append(time.text)
	dict_res['Game'].append(home_team_name.text + '-' + away_team_name.text)
	dict_res['Final Score'].append(final_score.text.split()[0] + '-' + final_score.text.split()[-1])
	for a in section:
		lista_category.append(a)
		split_list = lista_category[n].text.split()
		n = n+1
		lista_category_final_s = ' '.join(map(str, split_list[1:-1]))
		lista_home = ''.join(map(str, split_list[0]))
		lista_away = ''.join(map(str, split_list[-1]))
		dict_res[lista_category_final_s].append(lista_home + "-" + lista_away)
	driver.close()
	driver.switch_to.window(original_window)
df_res = pd.DataFrame.from_dict(dict_res, orient='index')
df_res = df_res.transpose()
del df_res["Yellow Cards"]
del df_res["Red Cards"]
df_res.to_csv('selenium_flashscore_scrap.csv',header=True, index= None)

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
cs.execute('CREATE OR REPLACE TABLE "flashscore_scrap" ( "Time and Date" STRING,"Game" STRING,"Final Score" STRING,"Ball Possession" STRING,"Goal Attempts" STRING,"Shots on Goal" STRING,"Shots off Goal" STRING,"Blocked Shots" STRING,"Free Kicks" STRING,"Corner Kicks" STRING,"Offsides" STRING,"Throw-in" STRING,"Goalkeeper Saves" STRING,"Fouls" STRING,"Total Passes" STRING,"Completed Passes" STRING,"Tackles" STRING,"Attacks" STRING,"Dangerous Attacks" STRING)')

df_flashscore = pd.read_csv("selenium_flashscore_scrap.csv", sep=",")

write_pandas(ctx,df_flashscore,table_name="flashscore_scrap")