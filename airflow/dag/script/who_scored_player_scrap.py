from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
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

    if split_data_table[(nr_col * i + 2):(nr_col * i + 4)] in teams_list:
        split_data_table[(nr_col * i + 2):(nr_col * i + 4)] = [
            ' '.join(split_data_table[(nr_col * i + 2):(nr_col * i + 4)])]
    return split_data_table


def correct_page_for_players_name(nr_col, i, split_data_table):
    list_to_skip = [['Casemiro'], ['Richarlison'], ['Neymar'], ['Rodri'], ['Pedri'], ['Gavi'], ['Pepe'],
                    ['Otávio'], ['Raphinha'], ['Danilo'], ['Marquinhos'], ['Vitinha'], ['Antony'], ['Alisson'],
                    ['Rodrygo'], ['Pedro'], ['Fred'], ['Bremer'], ['Koke'], ['Ederson'], ['Weverton'], ['Fabinho']]
    list_three_names = [['Mohammed', 'Al', 'Owais'], ['Abdulelah', 'Al', 'Malki'], ['Virgil', 'van', 'Dijk'],
                        ['Salem', 'Al', 'Dawsari'], ['André-Frank', 'Zambo', 'Anguissa'],
                        ['Saleh', 'Al', 'Shehri'], ['Anis', 'Ben', 'Slimane'],
                        ['Abdulrahman', 'Al', 'Obud'], ['Pape', 'Abou', 'Cissé'], ['Mohammed', 'Al', 'Burayk'],
                        ['Hassan', 'Al', 'Haydos'], ['Abderrazzaq', 'Hamed', 'Allah'], ['Nawaf', 'Al', 'Abid'],
                        ['Andreas', 'Skov', 'Olsen'], ['Samuel', 'Oum', 'Gouet'],
                        ['Taha', 'Yassine', 'Khenissi'], ['Taha', 'Yassine', 'Khenissi'], ['Ali', 'Al', 'Bulayhi'],
                        ['Abdulelah', 'Al', 'Amri'], ['Salis', 'Abdul', 'Samed'], ['Jawad', 'El', 'Yamiq'],
                        ['Sultan', 'Al', 'Ghannam'], ['Matthijs', 'de', 'Ligt'], ['Juan', 'Pablo', 'Vargas'],
                        ['Yasir', 'Al', 'Shahrani'], ['Feras', 'Al', 'Brikan'], ['Bassam', 'Al', 'Rawi'],
                        ['Ali', 'Al', 'Hassan'], ['Rogelio', 'Funes', 'Mori'], ['Bilal', 'El', 'Khannouss'],
                        ['Salman', 'Al', 'Faraj'], ['Sami', 'Al', 'Naji'], ['Saad', 'Al', 'Sheeb']]
    list_3_names_4_details = [['Frenkie', 'de', 'Jong'], ['Luuk', 'de', 'Jong'], ['Giorgian', 'de', 'Arrascaeta'],
                              ['Randal', 'Kolo', 'Muani'], ['Alexis', 'Mac', 'Allister'],
                              ['Ángel', 'Di', 'María'], ['Kevin', 'De', 'Bruyne'], ['Rodrigo', 'De', 'Paul'],
                              ['Abdul', 'Rahman', 'Baba'], ['Karl', 'Toko', 'Ekambi'], ['Marten', 'de', 'Roon'],
                              ['Charles', 'De', 'Ketelaere']]

    if (split_data_table[(nr_col * i + 1):(nr_col * i + 5)] == ['Nicolás', 'de', 'la', 'Cruz']) or (
            split_data_table[(nr_col * i + 1):(nr_col * i + 5)] == ['Mohamed', 'Ali', 'Ben', 'Romdhane']):
        split_data_table[(nr_col * i + 1):(nr_col * i + 5)] = [
            ' '.join(split_data_table[(nr_col * i + 1):(nr_col * i + 5)])]
        split_data_table[(nr_col * i + 2):(nr_col * i + 6)] = [
            ' '.join(split_data_table[(nr_col * i + 5):(nr_col * i + 6)])]
    else:
        if (split_data_table[(nr_col * i + 1):(nr_col * i + 2)] in list_to_skip) and (
                split_data_table[(nr_col * i + 1):(nr_col * i + 3)] not in [['Pedro', 'Miguel'],
                                                                            ['Danilo', 'Pereira']]):
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


def get_pages_data(nr_col, selected_tab, pages):
    df2 = pd.DataFrame()
    data_table = driver.find_elements(By.XPATH, ('//*[@id="player-table-statistics-body"]'))
    list_data_table = []

    j = 0
    for page in range(pages):

        if page > 0:
            next_page = driver.find_element(By.XPATH, '/html/body/div[5]/div[5]/div[' + str(
                selected_tab) + ']/div[4]/div/dl[2]/dd[3]/a')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(1)
            data_table = driver.find_elements(By.XPATH, ('//*[@id="player-table-statistics-body"]'))

        for data in data_table:
            list_data_table.append(data)
            split_data_table = list_data_table[j].text.split()
            j = j + 1

        for i in range(0, 10):
            split_data_table = correct_page_for_players_name(nr_col, i, split_data_table)
            i += 1
        page += 1

        length_to_split = [nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col, nr_col]
        Inputt = iter(split_data_table)
        Output = [list(islice(Inputt, elem)) for elem in length_to_split]
        df1 = pd.DataFrame(Output)
        df2 = pd.concat([df2, df1])

    return df2


def summary():
    df = get_pages_data(13, 2, 55)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Goals', 'Assists', 'Yel', 'Red', 'SpG', 'PS%',
                  'AerialsWon', 'MotM', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_summary.csv', header=True, index=False)


def defensive():
    df = get_pages_data(13, 3, 55)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb', 'Blocks',
                  'OwnG', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_defensive.csv', header=True, index=False)


def offensive():
    df = get_pages_data(14, 4, 55)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Goals', 'Assists', 'SpG', 'KeyP', 'Drb', 'Fouled', 'Off', 'Disp',
                  'UnsTch', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_offensive.csv', header=True, index=False)


def passing():
    df = get_pages_data(12, 5, 55)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Assist', 'KeyP', 'AvgP', 'PS%', 'Crosses', 'LongB', 'ThrB',
                  'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_passing.csv', header=True, index=False)


def detailed_shoots_zones():
    df = get_pages_data(9, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_zones.csv', header=True, index=False)


def detailed_shoots_situations():
    df = get_pages_data(10, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyTaken', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_situations.csv', header=True,
              index=False)


def detailed_shoots_accuracy():
    df = get_pages_data(10, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OffTarget', 'OnPost', 'OnTarget', 'Blocked', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_accuracy.csv', header=True,
              index=False)


def detailed_shoots_body_part():
    df = get_pages_data(10, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_body_part.csv', header=True,
              index=False)


def detailed_goal_zone():
    df = get_pages_data(9, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_zone.csv', header=True,
              index=False)


def detailed_goal_situations():
    df = get_pages_data(12, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'OpenPlay', 'Counter', 'SetPiece', 'PenaltyScored', 'Own',
                  'Normal', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_situations.csv', header=True,
              index=False)


def detailed_goal_body_part():
    df = get_pages_data(10, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'RightFoot', 'LeftFoot', 'Head', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_body_part.csv', header=True,
              index=False)


def detailed_dribbles():
    df = get_pages_data(8, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Unsuccessful', 'Successful', 'Total Dribbles', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_dribbles.csv', header=True,
              index=False)


def detailed_possesion_lose():
    df = get_pages_data(7, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'UnsuccessfulTouches', 'Dispossessed', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_possesion_lose.csv', header=True,
              index=False)


def detailed_aerial():
    df = get_pages_data(8, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Won', 'Lost', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_aerial.csv', header=True,
              index=False)


def detailed_passes_length():
    df = get_pages_data(10, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_length.csv', header=True,
              index=False)


def detailed_passes_type():
    df = get_pages_data(11, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'AccCr', 'InAccCr', 'AccCrn', 'InAccCrn', 'AccFrk', 'InAccFrK',
                  'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_type.csv',
              header=True,
              index=False)


def detailed_key_passes_type():
    df = get_pages_data(11, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Cross', 'Corner', 'Throughball',
                  'Freekick', 'Throwin', 'Other', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_types.csv',
              header=True,
              index=False)


def detailed_key_passes_length():
    df = get_pages_data(8, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Long', 'Short', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_length.csv',
              header=True,
              index=False)


def detailed_assists():
    df = get_pages_data(12, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Cross', 'Corner', 'Throughball',
                  'Freekick', 'Throwin', 'Other', 'Total', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_assists.csv',
              header=True,
              index=False)


########
def detailed_tackles():
    df = get_pages_data(8, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_tackles.csv', header=True, index=False)


def detailed_interception():
    df = get_pages_data(6, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_interception.csv', header=True, index=False)


def detailed_fouls():
    df = get_pages_data(7, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Foulde', 'Fouls', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_fouls.csv', header=True, index=False)


def detailed_cards():
    df = get_pages_data(7, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Yellow', 'red', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_cards.csv', header=True, index=False)


def detailed_offside():
    df = get_pages_data(6, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'CaughtOffside', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_offside.csv', header=True, index=False)


def detailed_clearances():
    df = get_pages_data(6, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_clearances.csv', header=True, index=False)


def detailed_blocks():
    df = get_pages_data(8, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'ShotsBlocked', 'CrossesBlocked', 'PassesBlocked', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_blocks.csv', header=True, index=False)


def detailed_saves():
    df = get_pages_data(9, 6, 69)
    df.columns = ['No.', 'Player', 'Apps', 'Mins', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']
    df.to_csv('PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_saves.csv', header=True, index=False)


summary()

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


detailed_goal_zone()

dropdown_subcategory = driver.find_element(By.ID, 'subcategory')
drop_subcategory = Select(dropdown_subcategory)
drop_subcategory.select_by_visible_text("Situations")
time.sleep(2)

detailed_goal_situations()

detail_button = driver.find_element(By.XPATH, '//*[@id="stage-top-player-stats-options"]/li[5]/a')
driver.execute_script("arguments[0].click();", detail_button)
time.sleep(1)

drop_subcategory.select_by_visible_text("Body Parts")
time.sleep(2)
dropdown_total = driver.find_element(By.ID, 'statsAccumulationType')
total_subcategory = Select(dropdown_total)
total_subcategory.select_by_visible_text("Total")
time.sleep(2)

search_button = driver.find_element(By.XPATH, '//*[@class="search-button"]')
driver.execute_script("arguments[0].click();", search_button)
time.sleep(1)

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

###

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

drop_category.select_by_visible_text("Offsides")
time.sleep(2)
detailed_offside()

drop_category.select_by_visible_text("Clearances")
time.sleep(2)
detailed_clearances()

drop_category.select_by_visible_text("Blocks")
time.sleep(2)
detailed_blocks()

drop_category.select_by_visible_text("Saves")
time.sleep(2)
detailed_saves()

driver.close()


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
    'CREATE OR REPLACE TABLE "player_stats_summary" ("No." STRING, "Player" STRING, "Apps" STRING, "Mins" STRING, "Goals" STRING, "Assists" STRING, "Yel" STRING, "Red" STRING, "SpG" STRING, "PS%" STRING,"AerialsWon" STRING, "MotM" STRING, "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_summary.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_summary")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_defensive" ("No." STRING, "Player" STRING, "Apps" STRING, "Mins" STRING, "Tackles" STRING, "Inter" STRING, "Fouls" STRING, "Offsides" STRING, "Clear" STRING, "Drb" STRING, "Blocks"  STRING, "OwnG" STRING, "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_defensive.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_defensive")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_offensive" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Goals" STRING , "Assists" STRING , "SpG" STRING , "KeyP" STRING , "Drb" STRING , "Fouled" STRING , "Off" STRING , "Disp" STRING, "UnsTch" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_offensive.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_offensive")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_passing" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Assist" STRING , "KeyP" STRING , "AvgP" STRING , "PS%" STRING , "Crosses" STRING , "LongB" STRING , "ThrB" STRING ,"Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_passing.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_passing")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_zones" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OutOfBox" STRING , "SixYardBox" STRING , "PenaltyArea" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_zones.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_zones")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_situations" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OpenPlay" STRING , "Counter" STRING , "SetPiece" STRING , "PenaltyTaken" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_situations.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_situations")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_accuracy" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OffTarget" STRING , "OnPost" STRING , "OnTarget" STRING , "Blocked" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_accuracy.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_accuracy")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_shoots_body_part" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "RightFoot" STRING , "LeftFoot" STRING , "Head" STRING , "Other" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_shoots_body_part.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_shoots_body_part")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_goal_zone" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "SixYardBox" STRING , "PenaltyArea" STRING , "OutOfBox" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_zone.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_goal_zone")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_goal_situations" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "OpenPlay" STRING , "Counter" STRING , "SetPiece" STRING , "PenaltyScored" STRING , "Own" STRING ,"Normal" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_situations.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_goal_situations")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_goal_body_part" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "RightFoot" STRING , "LeftFoot" STRING , "Head" STRING , "Other" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_goal_body_part.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_goal_body_part")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_dribbles" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Unsuccessful" STRING , "Successful" STRING , "Total Dribbles" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_dribbles.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_dribbles")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_possesion_lose" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "UnsuccessfulTouches" STRING , "Dispossessed" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_possesion_lose.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_possesion_lose")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_aerial" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Won" STRING , "Lost" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_aerial.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_aerial")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_passes_length" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "AccLB" STRING , "InAccLB" STRING , "AccSP" STRING , "InAccSP" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_length.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_passes_length")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_passes_type" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "AccCr" STRING , "InAccCr" STRING , "AccCrn" STRING , "InAccCrn" STRING , "AccFrk" STRING , "InAccFrK" STRING, "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_passes_type.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_passes_type")

cs.execute('CREATE OR REPLACE TABLE "player_stats_detailed_key_passes_types" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Cross" STRING , "Corner" STRING , "Throughball" STRING, "Freekick" STRING , "Throwin" STRING , "Other" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_types.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_key_passes_types")


cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_key_passes_length" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Long" STRING , "Short" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_key_passes_length.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_key_passes_length")


cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_assists" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Cross" STRING , "Corner" STRING , "Throughball" STRING, "Freekick" STRING , "Throwin" STRING , "Other" STRING , "Total" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_assists.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_assists")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_tackles" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "TotalTackles" STRING , "DribbledPast" STRING , "TotalAttemptedTackles" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_tackles.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_tackles")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_interception" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_interception.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_interception")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_fouls" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Foulde" STRING , "Fouls" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_fouls.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_fouls")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_cards" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Yellow" STRING , "red" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_cards.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_cards")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_offside" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "CaughtOffside" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_offside.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_offside")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_clearances" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "Total" STRING , "Rating" STRING )'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_clearances.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_clearances")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_blocks" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING , "ShotsBlocked" STRING , "CrossesBlocked" STRING , "PassesBlocked" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_blocks.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_blocks")

cs.execute(
    'CREATE OR REPLACE TABLE "player_stats_detailed_saves" ("No." STRING , "Player" STRING , "Apps" STRING , "Mins" STRING,"Total" STRING , "SixYardBox" STRING , "PenaltyArea" STRING , "OutOfBox" STRING , "Rating" STRING)'
)
df = pd.read_csv("PlayerFiles/selenium_whoscored_scrap_player_stats_detailed_saves.csv", sep=",")
write_pandas(ctx, df, table_name="player_stats_detailed_saves")
