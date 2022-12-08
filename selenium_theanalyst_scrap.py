from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
import pandas as pd 
import time


dict_res = defaultdict(list)


PATH = 'Downloads\\chromedriver'
driver = webdriver.Chrome(PATH)

wait = WebDriverWait(driver, 10)

driver.get('https://dataviz.theanalyst.com/fifa-world-cup-2022/')
time.sleep(1)

player_stats = driver.find_element(By.XPATH, '//*[@id="Player Stats"]')
driver.execute_script("arguments[0].click();", player_stats)
time.sleep(1)

def main_function():
	list_header = []
	n = 0
	m = 0
	headers = driver.find_elements(By.XPATH, ('//*[@id="root"]/div/div/div/div[5]/div[2]/div[2]/div[2]/table/thead/tr[2]'))
	for header in headers:
		list_header.append(header)
		split_list_header = list_header[n].text.split()
		n = n+1
		split_list_header[1:3] = ['-'.join(split_list_header[1:3])]
		split_list_header[6:8] = ['-'.join(split_list_header[6:8])]
		split_list_header[10:12] = ['-'.join(split_list_header[10:12])]
		split_list_header[11:13] = ['-'.join(split_list_header[11:13])]
		split_list_header[20:22] = ['-'.join(split_list_header[20:22])]


	players = driver.find_elements(By.CLASS_NAME, ('NSFMbBzuHrufmLlei2bm'))
	for player in players:
		split_list_player = players[m].text.split()
		m = m+1
		data = [x for x in split_list_player if x.isalpha() == True]
		data_final = ' '.join(map(str, data))
		dict_res[split_list_header[0]].append(data_final)
		list_no_name = [i for i in split_list_player if i not in data]
		dict_res[split_list_header[1]].append(list_no_name[0])
		dict_res[split_list_header[2]].append(list_no_name[1])
		dict_res[split_list_header[3]].append(list_no_name[2])
		dict_res[split_list_header[4]].append(list_no_name[3])
		dict_res[split_list_header[5]].append(list_no_name[4])
		dict_res[split_list_header[6]].append(list_no_name[5])
		dict_res[split_list_header[7]].append(list_no_name[6])
		dict_res[split_list_header[8]].append(list_no_name[7])
		dict_res[split_list_header[9]].append(list_no_name[8])
		dict_res[split_list_header[10]].append(list_no_name[9])
		dict_res[split_list_header[11]].append(list_no_name[10])
		dict_res[split_list_header[12]].append(list_no_name[11])
		dict_res[split_list_header[13]].append(list_no_name[12])
		dict_res[split_list_header[14]].append(list_no_name[13])
		dict_res[split_list_header[15]].append(list_no_name[14])
		dict_res[split_list_header[16]].append(list_no_name[15])
		dict_res[split_list_header[17]].append(list_no_name[16])
		dict_res[split_list_header[18]].append(list_no_name[17])
		dict_res[split_list_header[19]].append(list_no_name[18])
		dict_res[split_list_header[20]].append(list_no_name[19])

main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()
next_page = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[5]/div[2]/div[2]/div[3]/button[2]')
driver.execute_script("arguments[0].click();", next_page)
time.sleep(1)
main_function()

df_res = pd.DataFrame(dict_res)
df_res.to_csv('the_analyst_scrap.csv',header=True)
