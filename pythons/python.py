import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import json

url = 'https://game8.co'
endpoint = "https://game8.co/games/Wuthering-Waves/archives/453473"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
page = rq.get(endpoint, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

tittles = soup.find_all('h4',class_='a-header--4')
resultados = []

for t in tittles : 
    tittle = t.get_text(strip=True)
    table = t.find_next_sibling('table')

    img = table.select_one('img')

    img_url = img.get("data-src") if img else None

    td = table.select_one('td.center') if table else None
    duration = td.get_text(strip=True).split(' - ') if td else None

    init = datetime.strptime(duration[0], "%B %d, %Y") if duration else None
    if duration and duration[1] != "Permanent":
        finish = datetime.strptime(duration[1], "%B %d, %Y")
    else :
        finish = None

    p = t.find_next_sibling('p')
    desc = p.get_text(strip=True) if p else None

    a = p.find_next_sibling('p').select_one('a.a-btn')
    if a:
        more_info = a['href']
    else :
        more_info = ""   

    resultados.append({
        'tittle' : tittle,
        'desc' :  desc,
        'more_info': url+more_info,
        'init' : str(init.date()),
        'finish' : str(finish.date()) if finish else None,
        'img' : img_url
    })

print(json.dumps(resultados))




