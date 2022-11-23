#docker-compose up
from requests_html import AsyncHTMLSession
from collections import defaultdict
import pandas as pd 

url = 'https://www.flashscore.com/match/ARmio3Rl/#/match-summary/match-summary'
asession = AsyncHTMLSession()

async def get_scores():
	r = await asession.get(url)
	await r.html.arender()
	return r

results = asession.run(get_scores)
results = results[0]
dict_res = defaultdict(list)

lista_category = []
n = 0

times = results.html.find("div.duelParticipant__startTime")
home = results.html.find("div.duelParticipant__home") 
away = results.html.find("div.duelParticipant__away")
score = results.html.find("div.detailScore__wrapper")
section = results.html.find("div.stat__row")

dict_res['time and date'].append(times[0].text)
dict_res['game'].append(home[0].text + '-' + away[0].text)
dict_res['score'].append(score[0].text)

for a in section:
	lista_category.append(a)
	split_list = lista_category[n].text.split()
	n = n+1
	lista_category_final_s = ' '.join(map(str, split_list[1:-1]))
	lista_home = ''.join(map(str, split_list[0]))
	lista_away = ''.join(map(str, split_list[-1]))
	dict_res[lista_category_final_s].append(lista_home + "-" + lista_away)
df_res = pd.DataFrame(dict_res)
print("--------")
print("\n")
print(df_res.to_string())
print("\n")
print("--------")