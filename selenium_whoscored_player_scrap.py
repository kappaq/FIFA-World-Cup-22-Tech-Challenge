from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
from collections import defaultdict
import pandas as pd
import time
import re
from itertools import islice

options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1000,550")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

PATH = 'chromedriver'
driver = webdriver.Chrome(PATH)

a = ActionChains(driver)
wait = WebDriverWait(driver, 10)

driver.get(
    'https://www.whoscored.com/Regions/247/Tournaments/36/Seasons/8213/Stages/18657/PlayerStatistics/International-FIFA-World-Cup-2022')
time.sleep(1)

accept_cookie_main_page = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", accept_cookie_main_page)
time.sleep(1)


def correct_page_for_teams_name(nr_col, i, split_data_table):
    teams_list = [['Costa', 'Rica,'], ['Saudi', 'Arabia,'], ['South', 'Korea,']]
    print(split_data_table[(nr_col * i + 2):(nr_col * i + 4)])
    print("--------------------------")
    if split_data_table[(nr_col * i + 2):(nr_col * i + 4)] in teams_list:
        split_data_table[(nr_col * i + 2):(nr_col * i + 4)] = [
            ' '.join(split_data_table[(nr_col * i + 2):(nr_col * i + 4)])]
    return split_data_table


def correct_page_for_players_name(nr_col, i, split_data_table):
    list_to_skip = [['Casemiro'], ['Richarlison'], ['Neymar'], ['Rodri'], ['Pedri'], ['Gavi'], ['Pepe'],
                    ['Otávio'], ['Raphinha'], ['Danilo'], ['Marquinhos'], ['Vitinha'], ['Antony'], ['Alisson'],
                    ['Rodrygo'], ['Pedro'], ['Fred'], ['Bremer'], ['Koke']]
    list_three_names = [['Mohammed', 'Al', 'Owais'], ['Abdulelah', 'Al', 'Malki'], ['Virgil', 'van', 'Dijk'],
                        ['Salem', 'Al', 'Dawsari'], ['André-Frank', 'Zambo', 'Anguissa'],
                        ['Saleh', 'Al', 'Shehri'], ['Anis', 'Ben', 'Slimane'],
                        ['Abdulrahman', 'Al', 'Obud'], ['Pape', 'Abou', 'Cissé'], ['Mohammed', 'Al', 'Burayk'],
                        ['Hassan', 'Al', 'Haydos'], ['Abderrazzaq', 'Hamed', 'Allah'], ['Nawaf', 'Al', 'Abid'],
                        ['Andreas', 'Skov', 'Olsen'], ['Samuel', 'Oum', 'Gouet'],
                        ['Taha', 'Yassine', 'Khenissi'], ['Taha', 'Yassine', 'Khenissi'], ['Ali', 'Al', 'Bulayhi'],
                        ['Abdulelah', 'Al', 'Amri'], ['Salis', 'Abdul', 'Samed'], ['Jawad', 'El', 'Yamiq'],
                        ['Sultan', 'Al', 'Ghannam'], ['Matthijs', 'de', 'Ligt'], ['Juan', 'Pablo', 'Vargas']]
    list_3_names_4_details = [['Frenkie', 'de', 'Jong'], ['Giorgian', 'de', 'Arrascaeta'],
                              ['Randal', 'Kolo', 'Muani'], ['Alexis', 'Mac', 'Allister'],
                              ['Ángel', 'Di', 'María'], ['Kevin', 'De', 'Bruyne'], ['Rodrigo', 'De', 'Paul'],
                              ['Abdul', 'Rahman', 'Baba'], ['Karl', 'Toko', 'Ekambi'], ['Marten', 'de', 'Roon']]
    print(split_data_table)
    print(split_data_table[(nr_col * i):(nr_col * i + 1)])
    if split_data_table[(nr_col * i + 1):(nr_col * i + 5)] == ['Nicolás', 'de', 'la', 'Cruz']:
        split_data_table[(nr_col * i + 1):(nr_col * i + 5)] = [
            ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 5)])]
        split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
            ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
    else:
        if (split_data_table[(nr_col * i + 1):(nr_col * i + 2)] in list_to_skip) and (
                split_data_table[(nr_col * i + 1):(nr_col * i + 3)] != ['Pedro', 'Miguel']):
            split_data_table[(nr_col * i + 1):(nr_col * i + 2)] = [
                ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 2)])]
            split_data_table = correct_page_for_teams_name(nr_col, i, split_data_table)
            split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
                ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
        else:
            if split_data_table[(nr_col * i + 1):(nr_col * i + 4)] in list_three_names:
                split_data_table[(nr_col * i + 1):(nr_col * i + 4)] = [
                    ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 4)])]
                split_data_table = correct_page_for_teams_name(nr_col, i, split_data_table)
                split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
                    ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
            else:
                if split_data_table[(nr_col * i + 1):(nr_col * i + 4)] in list_3_names_4_details:
                    split_data_table[(nr_col * i + 1):(nr_col * i + 4)] = [
                        ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 4)])]
                    split_data_table = correct_page_for_teams_name(nr_col, i, split_data_table)
                    split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
                        ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
                else:
                    split_data_table[(nr_col * i + 1):(nr_col * i + 3)] = [
                        ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 3)])]
                    split_data_table = correct_page_for_teams_name(nr_col, i, split_data_table)
                    split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
                        ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
    return split_data_table


def get_pages_data(nr_col):
    df2 = pd.DataFrame()
    data_table = driver.find_elements(By.XPATH, ('//*[@id="player-table-statistics-body"]'))
    list_data_table = []
    Inputt = []
    Output = []
    j = 0
    for page in range(2):
        print(page)
        if page > 0:
            next_page = driver.find_element(By.XPATH, '//*[@id="next"]')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(1)

            data_table = driver.find_elements(By.XPATH, ('//*[@id="player-table-statistics-body"]'))

        for data in data_table:
            list_data_table.append(data)
            split_data_table = list_data_table[j].text.split()
            j = j + 1

        print(data_table)
        print(list_data_table)
        print(split_data_table)
        for i in range(0, 10):
            split_data_table = correct_page_for_players_name(nr_col, i, split_data_table)
            i += 1
        page += 1

        length_to_split = [nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col]
        Inputt = iter(split_data_table)
        Output = [list(islice(Inputt, elem)) for elem in length_to_split]
        df1 = pd.DataFrame(Output)
        df2 = pd.concat([df2, df1])
        print(Output)

    return df2


def summary():
    df = get_pages_data(13)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Goals', 'Assists', 'Yel', 'Red', 'SpG', 'PS%',
                  'AerialsWon', 'MotM', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_summary.csv', header=True, index=False)


def defensive():
    df = get_pages_data(13)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb', 'Blocks',
                  'OwnG', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_defensive.csv', header=True, index=False)


def offensive():
    df = pd.DataFrame()
    df = get_pages_data(14)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Goals', 'Assists', 'SpG', 'KeyP', 'Drb', 'Fouled', 'Off', 'Disp',
                  'UnsTch', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_offensive.csv', header=True, index=False)


def passing():
    df = pd.DataFrame()
    df = get_pages_data(12)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Assist', 'KeyP', 'AvgP', 'PS%', 'Crosses', 'LongB', 'ThrB',
                  'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_passing.csv', header=True, index=False)


def detailed_shoots_zones():
    df = pd.DataFrame()
    df = get_pages_data(9)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_zones.csv', header=True, index=False)


def detailed_shoots_situations():
    df = pd.DataFrame()
    df = get_pages_data(10)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyTaken', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_situations.csv', header=True,
              index=False)


def detailed_shoots_accuracy():
    df = pd.DataFrame()
    df = get_pages_data(10)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OffTarget', 'OnPost', 'OnTarget', 'Blocked', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_accuracy.csv', header=True,
              index=False)


def detailed_shoots_body_part():
    df = pd.DataFrame()
    df = get_pages_data(10)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_body_part.csv', header=True,
              index=False)


def detailed_goal_zone():
    df = pd.DataFrame()
    df = get_pages_data(9)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_zone.csv', header=True,
              index=False)


def detailed_goal_situations():
    df = get_pages_data(12)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyScored', 'Own',
                  'Normal', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_situations.csv', header=True,
              index=False)

def detailed_goal_body_part():
    df = get_pages_data(10)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_body_part.csv', header=True,
              index=False)


def detailed_dribbles():
    df = get_pages_data(8)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Unsuccessful', 'Successful', 'Total Dribbles', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_dribbles.csv', header=True,
              index=False)


def detailed_possesion_lose():
    df = get_pages_data(7)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'UnsuccessfulTouches', 'Dispossessed', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_possesion_lose.csv', header=True,
              index=False)


def detailed_aerial():
    df = get_pages_data(8)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Won', 'Lost', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_aerial.csv', header=True,
              index=False)


def detailed_passes_length():
    df = get_pages_data(10)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_length.csv', header=True,
              index=False)


def detailed_passes_type():
    df = get_pages_data(11)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'AccCr', 'InAccCr', 'AccCrn', 'InAccCrn', 'AccFrk', 'InAccFrK',
                  'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_type.csv',
              header=True,
              index=False)


def detailed_key_passes_type():
    df = get_pages_data(11)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Cross', 'Corner', 'Throughball',
                  'Freekick', 'Throwin', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_types.csv',
              header=True,
              index=False)


def detailed_key_passes_length():
    df = get_pages_data(8)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Long', 'Short', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_length.csv',
              header=True,
              index=False)


def detailed_assists():
    df = get_pages_data(12)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Cross', 'Corner', 'Throughball',
                  'Freekick', 'Throwin', 'Other', 'Total', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_assists.csv',
              header=True,
              index=False)


summary()

defensive_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[2]/a')
driver.execute_script("arguments[0].click();", defensive_button)
time.sleep(1)

driver.refresh()
time.sleep(3)

defensive_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[2]/a')
driver.execute_script("arguments[0].click();", defensive_button)
time.sleep(1)

defensive()

offensive_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[3]/a')
driver.execute_script("arguments[0].click();", offensive_button)
time.sleep(1)

offensive()

passing_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[4]/a')
driver.execute_script("arguments[0].click();", passing_button)
time.sleep(1)

passing()

detail_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[5]/a')
driver.execute_script("arguments[0].click();", detail_button)
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

dropdown_category = driver.find_element(By.ID, 'category')
drop_category = Select(dropdown_category)
drop_category.select_by_visible_text("Goals")
time.sleep(2)

detailed_goal_zone()

drop_subcategory.select_by_visible_text("Situations")
time.sleep(2)

detailed_goal_situations()

drop_subcategory.select_by_visible_text("Body Parts")
time.sleep(2)

detailed_goal_body_part()

drop_category.select_by_visible_text("Dribbles")
time.sleep(2)

detailed_dribbles()

drop_category.select_by_visible_text("Possession loss")
time.sleep(2)

detailed_possesion_lose()

drop_category.select_by_visible_text("Aerial")
time.sleep(2)

detailed_aerial()

drop_category.select_by_visible_text("Passes")
time.sleep(2)

detailed_passes_length()

drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

detailed_passes_type()

drop_category.select_by_visible_text("Key passes")
time.sleep(2)

detailed_key_passes_length()

drop_subcategory.select_by_visible_text("Type")
time.sleep(2)

detailed_key_passes_type()

drop_category.select_by_visible_text("Assists")
time.sleep(2)

detailed_assists()

driver.close()
