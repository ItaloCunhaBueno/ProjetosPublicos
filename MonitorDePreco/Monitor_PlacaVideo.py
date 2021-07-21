import requests as rq
from bs4 import BeautifulSoup as bs
import json
import re

SITE = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia/geforce-rtx'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
DATA = rq.get(SITE, headers=headers)
SOUP = bs(DATA.content, "lxml")
SCRIPTS = SOUP.find_all('script', type='text/javascript')

PRECOS = []
PRECODESCONTO = []
PRODUTO = []
for S in SCRIPTS:
    json_string = re.search(r'listagemDados\s*=\s*(.*?}])\s*\n', str(S), flags=re.DOTALL)
    if json_string:
        json_data = json.loads(json_string[1])
        for D in json_data:
            #pprint(D)
            if '30' in D['nome'] and D['disponibilidade'] is True:
                PRECOS.append(D['preco'])
                PRECODESCONTO.append(D['preco_desconto'])
                PRODUTO.append(D['nome'])

BARATO = min(PRECOS)
PBARATO = PRODUTO[PRECOS.index(BARATO)]
BARATODESC = PRECODESCONTO[PRECOS.index(BARATO)]

print('='*100)
print('PRODUTO MAIS BARATO HOJE:')
print()
print(f'Nome: {PBARATO}')
print(f'Preço: {BARATO}')
print(f'Preço Boleto: {BARATODESC}')
print()
input('Precione ENTER para sair...')