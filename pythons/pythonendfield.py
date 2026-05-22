import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import json

url = 'https://game8.co'
endpoint = "http://127.0.0.1:5500/saveendfield.html"
page = rq.get(endpoint)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table', class_='a-table')
resultados = []
rows = tables[1].find_all('tr')
rows.extend(tables[2].find_all('tr')[1:])

for i in range(1, len(rows), 2): 
    a = rows[i].find('a')

    img_url = a.find('img').get('data-src') if a.find('img') else None

    tittle = a.get_text(strip=True) 
    column = rows[i].find_all('td')
    
    duration = column[1].get_text().split('\r\n')[1].strip().split(' ')

    f = duration[0].strip()
    t = duration[2].strip()

    more_info = a['href'] 


    init = datetime.strptime(f, "%m/%d/%y") if f else None
    finish = datetime.strptime(t, "%m/%d/%y") if t else None

    resultados.append({
       'tittle' : tittle,
       'more_info': url+more_info,
       'init' : str(init.date()) if init else None, 
       'finish' : str(finish.date()) if finish else None,
       'img' : img_url
    })

print(json.dumps(resultados))