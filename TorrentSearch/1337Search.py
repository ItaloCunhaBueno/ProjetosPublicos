from bs4 import BeautifulSoup
from pprint import pprint
import requests
import lxml
import PySimpleGUIQt as sg


sg.theme('Reddit')
headings = ['Nome', 'Seeders', 'Leechers', 'Data', 'Tamanho', 'Usuário', 'Download']
l = ['', '', '', '', '', '', '']
Values = [l for a in range(20)]

Layout = [[sg.T("Procurar:"), sg.I(key='keywords'), sg.B("PROCURAR", key='PROCURAR', size=(10,1))],
[sg.Listbox(l, enable_events=True, key='tabela')]]
        #   [sg.Table(Values, headings=headings, key='tabela', auto_size_columns=True, enable_events=True)]]

Window = sg.Window("1337x.to Searcher", layout=Layout, size=(1200, 695), font="SEGOEUI 11")

while True:
    event, values = Window.read()
    print(event, values)
    if event is None or event == 'sair':
        break
    if event == 'PROCURAR':
        KEYWORD = Window['keywords'].Get()
        if KEYWORD not in ['', ' ', None]:
            search = KEYWORD.lower().replace(" ", "+")
            URL = r'https://1377x.to/search/{0}/1/'.format(search)
            Domain = r'https://1377x.to'
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
            site = requests.get(URL, headers=headers).text
            soup = BeautifulSoup(site, features="lxml")
            torrents = soup.find('table').find_all('tr')
            choices = []
            for torrent in torrents[1:]:
                nome = torrent.find_all('a', href=True)[1].text
                link = Domain + torrent.find_all('a', href=True)[1]['href']
                seeders = torrent.find_all('td', class_='coll-2')[0].text
                leechers = torrent.find_all('td', class_='coll-3')[0].text
                date = torrent.find_all('td', class_='coll-date')[0].text
                size = torrent.find_all('td', class_='coll-4')[0].text.split(" ")
                size = size[0] + " " + size[1][0:2]
                user = torrent.find_all('td', class_='coll-5')[0].text
                # torrentlink = site = requests.get(link, headers=headers).text
                # soup2 = BeautifulSoup(torrentlink, features="lxml")
                # magnet = soup2.find('div', class_='col-9 page-content').find('ul').find('li').find('a', href=True)['href']
                # TEXTO = [nome, seeders, leechers, date, size, user, magnet]
                TEXTO = '\t\t'.join([nome, seeders, leechers, date, size, user])
                choices.append(TEXTO)
            Window['tabela'].Update(choices)
            Window.Refresh()
