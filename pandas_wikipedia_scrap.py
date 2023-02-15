import pandas as pd 


table_Ecuador = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Hernán Galíndez', flavor = 'bs4', index_col = 0)
df_Ecuador = table_Ecuador[0]

table_Netherlands = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Remko Pasveer', flavor = 'bs4', index_col = 0)
df_Netherlands = table_Netherlands[0]

table_Qatar = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Saad Al-Sheeb', flavor = 'bs4', index_col = 0)
df_Qatar = table_Qatar[0]

table_Senegal = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Seny Dieng', flavor = 'bs4', index_col = 0)
df_Senegal = table_Senegal[0]

table_England = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Jordan Pickford', flavor = 'bs4', index_col = 0)
df_England = table_England[0]

table_Iran = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Alireza Beiranvand', flavor = 'bs4', index_col = 0)
df_Iran = table_Iran[0]

table_United_States = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Matt Turner', flavor = 'bs4', index_col = 0)
df_United_States = table_United_States[0]

table_Wales = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Wayne Hennessey', flavor = 'bs4', index_col = 0)
df_Wales = table_Wales[0]

table_Argentina = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Franco Armani', flavor = 'bs4', index_col = 0)
df_Argentina = table_Argentina[0]

table_Mexico = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Alfredo Talavera', flavor = 'bs4', index_col = 0)
df_Mexico = table_Mexico[0]

table_Poland = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Wojciech Szczęsny', flavor = 'bs4', index_col = 0)
df_Poland = table_Poland[0]

table_Saudi_Arabia = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Mohammed Al-Rubaie', flavor = 'bs4', index_col = 0)
df_Saudi_Arabia = table_Saudi_Arabia[0]

table_Australia = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Miloš Degenek', flavor = 'bs4', index_col = 0)
df_Australia = table_Australia[0]

table_Denmark = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Kasper Schmeichel', flavor = 'bs4', index_col = 0)
df_Denmark = table_Denmark[0]

table_France = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Benjamin Pavard', flavor = 'bs4', index_col = 0)
df_France = table_France[0]

table_Tunisia = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Aymen Mathlouthi', flavor = 'bs4', index_col = 0)
df_Tunisia = table_Tunisia[0]

table_Costa_Rica = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Keylor Navas', flavor = 'bs4', index_col = 0)
df_Costa_Rica = table_Costa_Rica[0]

table_Germany = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Antonio Rüdiger', flavor = 'bs4', index_col = 0)
df_Germany = table_Germany[0]

table_Japan = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Eiji Kawashima', flavor = 'bs4', index_col = 0)
df_Japan = table_Japan[0]

table_Spain = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Robert Sánchez', flavor = 'bs4', index_col = 0)
df_Spain = table_Spain[0]

table_Belgium = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Thibaut Courtois', flavor = 'bs4', index_col = 0)
df_Belgium = table_Belgium[0]

table_Canada = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Alistair Johnston', flavor = 'bs4', index_col = 0)
df_Canada = table_Canada[0]

table_Croatia = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Dominik Livaković', flavor = 'bs4', index_col = 0)
df_Croatia = table_Croatia[0]

table_Morocco = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Yassine Bounou', flavor = 'bs4', index_col = 0)
df_Morocco = table_Morocco[0]

table_Brazil = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Alisson', flavor = 'bs4', index_col = 0)
df_Brazil = table_Brazil[0]

table_Cameroon = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Simon Ngapandouetnbu', flavor = 'bs4', index_col = 0)
df_Cameroon = table_Cameroon[0]

table_Serbia = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Marko Dmitrović', flavor = 'bs4', index_col = 0)
df_Serbia = table_Serbia[0]

table_Switzerland = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Yann Sommer', flavor = 'bs4', index_col = 0)
df_Switzerland = table_Switzerland[0]

table_Ghana = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Lawrence Ati-Zigi', flavor = 'bs4', index_col = 0)
df_Ghana = table_Ghana[0]

table_Portugal = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Rui Patrício', flavor = 'bs4', index_col = 0)
df_Portugal = table_Portugal[0]

table_South_Korea = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Kim Seung-gyu', flavor = 'bs4', index_col = 0)
df_South_Korea = table_South_Korea[0]

table_Uruguay = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads', match = 'Fernando Muslera', flavor = 'bs4', index_col = 0)
df_Uruguay = table_Uruguay[0]

frames = [df_Ecuador, df_Netherlands, df_Qatar, df_Senegal, df_England, df_Iran, df_United_States, df_Wales, df_Argentina, df_Mexico, df_Poland, df_Saudi_Arabia, df_Australia, df_Denmark, df_France, df_Tunisia, 
df_Costa_Rica, df_Germany, df_Japan, df_Spain, df_Belgium, df_Canada, df_Croatia, df_Morocco, df_Brazil, df_Cameroon, df_Serbia, df_Switzerland, df_Ghana, df_Portugal, df_South_Korea, df_Uruguay]

df_final = pd.concat(frames)
df_final.to_csv('wikipedia_scrap_team_clubs.csv')

table_coach = pd.read_html('https://sportsest.com/fifa-world-cup-2022-coaches/', match = 'Lionel Scaloni', flavor = 'bs4', index_col = 0)
df_coach = table_coach[0]
df_coach.to_csv('wikipedia_scrap_coaches.csv')