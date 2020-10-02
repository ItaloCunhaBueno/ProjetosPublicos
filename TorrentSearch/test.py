from bs4 import BeautifulSoup
from pprint import pprint
import requests
import lxml


KEYWORD = 'Enola'
search = KEYWORD.lower().replace(" ", "+")
URL = r'https://1337x.to/search/{0}/1/'.format(search)
Domain = r'https://1337x.to'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
site = requests.get(URL, headers=headers).text
soup = BeautifulSoup(site, features="lxml")
torrents = soup.find('table').find_all('tr')
choices = []
for torrent in torrents[1:2]:
    nome = torrent.find_all('a', href=True)[1].text
    link = Domain + torrent.find_all('a', href=True)[1]['href']
    seeders = torrent.find_all('td', class_='coll-2')[0].text
    leechers = torrent.find_all('td', class_='coll-3')[0].text
    date = torrent.find_all('td', class_='coll-date')[0].text
    size = torrent.find_all('td', class_='coll-4')[0].text.split(" ")
    size = size[0] + " " + size[1][0:2]
    user = torrent.find_all('td', class_='coll-5')[0].text
    torrentlink = site = requests.get(link, headers=headers).text
    soup2 = BeautifulSoup(torrentlink, features="lxml")
    magnet = soup2.find('div', class_='col-9 page-content').find('ul').find('li').find('a', href=True)['href']
    TEXTO = [nome, seeders, leechers, date, size, user, magnet]
    choices.append(TEXTO)
    DATALIST = {'Nome': nome, 'Seeders': seeders, 'Leechers': leechers, 'Data': date, 'Tamanho': size, 'User': user}
