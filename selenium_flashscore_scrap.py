from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import pandas as pd 
import time

dict_res = defaultdict(list)

PATH = 'C:\\Users\\anghe\\Desktop\\Challange WC\\chromedriver.exe'
driver = webdriver.Chrome(PATH)

a = ActionChains(driver)
wait = WebDriverWait(driver, 10)

driver.get('https://www.flashscore.com/')
#driver.fullscreen_window()
time.sleep(5)
accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(5)
world_cup = driver.find_element(By.XPATH, '//*[@id="my-leagues-list"]/div[3]/div[2]/a')
driver.implicitly_wait(5)
world_cup.click()
time.sleep(5)
#driver.fullscreen_window()
original_window = driver.current_window_handle
time.sleep(5)
game_1 = driver.find_element(By.XPATH, '//*[@id="g_1_ARmio3Rl"]')
driver.execute_script("arguments[0].click();", game_1)
time.sleep(5)
wait.until(EC.number_of_windows_to_be(2))
for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
stats = driver.find_element(By.XPATH, '//*[@id="detail"]/div[7]/div/a[2]')
driver.execute_script("arguments[0].click();", stats)
time.sleep(5)
time = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[1]')
home_team_name = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]')
away_team_name = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]')
final_score = driver.find_element(By.XPATH, '//*[@id="detail"]/div[1]/div[2]/div/div[1]')
dict_res['time and date'].append(time.text)
dict_res['game'].append(home_team_name.text + '-' + away_team_name.text)
dict_res['score'].append(final_score.text)
df_res = pd.DataFrame(dict_res)
print("--------")
print("\n")
print(df_res.to_string())
print("\n")
print("--------")