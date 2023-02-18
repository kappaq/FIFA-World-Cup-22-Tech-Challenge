import pandas as pd 
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

table_player_followers = pd.read_html('https://www.theafricandream.net/world-cup-players-followers-on-instagram/', match = '496,585,283', flavor = 'bs4', index_col = 0)
df_player_followers = table_player_followers[0]
df_player_followers.to_csv('instagram_followers_players.csv', header=False)

table_team_followers = pd.read_html('https://www.theafricandream.net/world-cup-players-followers-on-instagram/', match = '543,105,857', flavor = 'bs4', index_col = 0)
df_team_followers = table_team_followers[0]
df_team_followers.to_csv('instagram_followers_teams.csv',  header=False)

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
cs.execute('CREATE OR REPLACE TABLE "instagram_players" ( "Ranking" STRING, "Name" STRING, "Followers 15/11/2022" STRING, "Potential earnings per post" STRING, "Team" STRING, "Club" STRING)')
cs.execute('CREATE OR REPLACE TABLE "instagram_teams" ( "Ranking" STRING, "Team" STRING, "SUM of followers 15/11/2022" STRING, "Potential earnings per post" STRING)')


df_players = pd.read_csv("instagram_followers_players.csv", sep=",")
df_teams = pd.read_csv("instagram_followers_teams.csv", sep=",")

write_pandas(ctx,df_players,table_name="instagram_players")
write_pandas(ctx,df_teams,table_name="instagram_teams")