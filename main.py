import requests
from bs4 import BeautifulSoup
import xlwt
from xlwt import Workbook

cookies = {
    '__uzma': 'afe44c78-93a5-4124-a689-c2c9bf20db28',
    '__uzmb': '1672786493',
    '_ga': 'GA1.2.63406842.1672786493',
    '_gid': 'GA1.2.1522762318.1672786493',
    '__ssds': '2',
    '__ssuzjsr2': 'a9be0cd8e',
    '__uzmaj2': 'e93eac7e-4365-42fd-be01-9b36dd179062',
    '__uzmbj2': '1672786494',
    '__uzmc': '384742258800',
    '__uzmd': '1672786538',
    '__uzmcj2': '867391642692',
    '__uzmdj2': '1672786539',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '__uzma=afe44c78-93a5-4124-a689-c2c9bf20db28; __uzmb=1672786493; _ga=GA1.2.63406842.1672786493; _gid=GA1.2.1522762318.1672786493; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=e93eac7e-4365-42fd-be01-9b36dd179062; __uzmbj2=1672786494; __uzmc=384742258800; __uzmd=1672786538; __uzmcj2=867391642692; __uzmdj2=1672786539',
    'Referer': 'https://www.pickleballtournaments.com/pbt_tlisting.pl?when=F',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'when': 'F',
    'selstate': 'CA',
    'selsanctioning': '',
    'selnettype': '',
    'openregonly': 'false',
    'ssipaFilter': 'false',
    'aauFilter': 'false',
}

response = requests.get('https://www.pickleballtournaments.com/pbt_tlisting.pl', params=params, cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')


names = []
locations = []
dates = []
applys = []


row = 3
info = soup.find_all('div', class_ = 'col-md-4 info')
for i in info:
    name = i.find('a').text
    names.append(name)
    sheet1.write(row, 0, name)

    location = i.find('p').text
    locations.append(location)
    sheet1.write(row, 1, location)

    row += 1


row = 3
info = soup.find_all('div', class_ = 'col-md-3 logos')
for i in info:
    date = i.find('p').text.replace(' ','').replace('\n','')
    dates.append(date)
    sheet1.write(row, 2, date)

    row += 1


row = 3
info = soup.find_all('div', class_ = 'row')
for i in info:
    apply = i.find('div', class_ = 'col-md-3 registration opennow')
    if apply is None:
        applys.append('No Info')
        sheet1.write(row , 3, '')
    else:
        applyDate = apply.find('p', class_ = 'registernow').text.replace('Ends: ', '')
        applys.append(applyDate)
        sheet1.write(row, 3, applyDate)
    
    row += 1


with open('info.txt', 'w') as f:

    f.write('PICKLEBALL TOURNAMENTS\n\n\n')
    
    for i in range(0,len(names)):
        
        f.write(str(i+1) + '.\nName: ' + names[i] + '\nLocation: ' + locations[i] + '\nDate: ' + dates[i]  + '\nApply By: ' + applys[i+2] + '\n\n')


sheet1.write(0, 0, 'PICKLEBALL TOURNAMENTS')
sheet1.write(2, 0, 'Name:')
sheet1.write(2, 1, 'Location:')
sheet1.write(2, 2, 'Date:')
sheet1.write(2, 3, 'Apply By:')
wb.save('info.xls')