from selenium.webdriver.common.by import By
import pandas as pd
import time

from itertools import islice



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


def get_pages_data(nr_col, selected_tab, pages, driver):
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




