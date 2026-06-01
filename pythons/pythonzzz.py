import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import json

url = 'https://game8.co'
endpoint = "https://game8.co/games/Zenless-Zone-Zero/archives/457176"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
page = rq.get(endpoint, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table',class_='a-table')
resultados = []
rows = tables[0].find_all('tr')
rows.extend(tables[1].find_all('tr')[1:])


for i in range(1, len(rows), 2): 
    a = rows[i].find('a') 

    img_url = a.find('img').get('data-src')

    tittle = a.get_text(strip=True)

    f = rows[i].find('td',width='35%').get_text(strip=True)
    t = rows[i+1].find('span').get_text(strip=True)

    more_info = a['href']

    init = datetime.strptime(f, "%B %d, %Y")
    finish = datetime.strptime(t, "%B %d, %Y")

    resultados.append({
       'tittle' : tittle,
       'more_info': url+more_info,
       'init' : str(init.date()),
       'finish' : str(finish.date()) if finish else None,
       'img' : img_url
    })

f = open("data_zzz.json","w")
f.write(json.dumps(resultados))
f.close()
print(json.dumps(resultados))