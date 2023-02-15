import pandas as pd 


table_player_followers = pd.read_html('https://www.theafricandream.net/world-cup-players-followers-on-instagram/', match = '496,585,283', flavor = 'bs4', index_col = 0)
df_player_followers = table_player_followers[0]
df_player_followers.to_csv('instagram_followers_players.csv')

table_team_followers = pd.read_html('https://www.theafricandream.net/world-cup-players-followers-on-instagram/', match = '543,105,857', flavor = 'bs4', index_col = 0)
df_team_followers = table_team_followers[0]
df_team_followers.to_csv('instagram_followers_teams.csv')