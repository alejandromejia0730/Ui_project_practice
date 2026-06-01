import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import json

url = 'https://game8.co'
endpoint = "https://game8.co/games/Arknights-Endfield/archives/535443"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


""" 
<td width="50%" class="top center">
<div class="align"><div class="imageLink js-archive-open-image-modal" data-image-url="https://img.game8.co/4466415/935193d3400b79d1b70e52a5d731ab6e.png/original" data-micromodal-trigger="js-archive-open-image-modal" data-archive-url="">
<img src="https://img.game8.co/4466415/935193d3400b79d1b70e52a5d731ab6e.png/show" class="a-img lazy lazy-non-square lazy-loaded" alt="Uso curioso de la xiranita" data-src="https://img.game8.co/4466415/935193d3400b79d1b70e52a5d731ab6e.png/show" width="728" style="height: 0; padding-bottom: calc(px*410/728); padding-bottom: calc(min(100%,728px)*410/728);" data-loaded="true"><span class="imageLink__icon"></span>
</div></div>

<hr class="a-table__line">

<a class="a-link" href="https://game8.co/games/Arknights-Endfield/archives/594312"><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;">Uso curioso de Xiranite</font></font></a><br><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;"> (Versión 1.2) </font></font><br><font dir="auto" style="vertical-align: inherit;"><font dir="auto" style="vertical-align: inherit;">14/05/26 - 05/06/26</font></font>
</td>
 """

page = rq.get(endpoint,headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
ancor = soup.find('h3',class_='a-header--3')
table = ancor.find_next_sibling('table')
resultados = []

rows = table.find_all('td')
#rows.extend(tables[2].find_all('tr')[1:])

for i in rows : 
    img_url = i.find('img').get('data-src') if i.find('img') else None
    a = i.find('a')
    tittle = a.get_text(strip=True) 
    duration = a.find_next_siblings('br')[1].next_sibling.strip().split(' - ')
    
    f = duration[0].strip().split('/')
    t = duration[1].strip().split('/')
    
    more_info = a['href'] 

    init = datetime.strptime(f"{t[1]}/{t[0]}/2026", "%d/%m/%Y")
    finish = datetime.strptime(f"{f[1]}/{f[0]}/2026", "%d/%m/%Y")

    resultados.append({
       'tittle' : tittle,
       'more_info': url+more_info,
       'init' :  init.strftime("%d/%m/%Y"), 
       'finish' : finish.strftime("%d/%m/%Y"),
       'img' : img_url
    })


f = open("data_endfield.json","w")
f.write(json.dumps(resultados))
f.close()
print(json.dumps(resultados))