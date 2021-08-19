from requests_html import HTMLSession

print("ANALISANDO KABUM E TERABYTESHOP...")

KABUM = "https://kabum.com.br/hardware/placa-de-video-vga/nvidia/geforce-rtx?page_number=1&page_size=20&facet_filters=&sort=price"
TERABYTE = "https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce"

session = HTMLSession(browser_args=["--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"])
pagina = session.get(KABUM)
pagina.html.render(scrolldown=10, sleep=1)

LISTA60_TITULO = []
LISTA60_PRECO = []
LISTA60_LINK = []

LISTA70_TITULO = []
LISTA70_PRECO = []
LISTA70_LINK = []

ELEMENT = pagina.html.find("main")
for E in ELEMENT:
    if "id" in E.attrs:
        if E.attrs["id"] == "listing":
            DIV = E.find("div")
            for D in DIV:
                if "class" in D.attrs:
                    if "productCard" in D.attrs["class"]:
                        CARD = D.find("a")[0]
                        TEXTO = CARD.text.split("\n")
                        TITULO = TEXTO[1]
                        PRECO = float("".join([p for p in TEXTO[2] if p in "0123456789,"]).replace(",", "."))
                        LINK = list(CARD.absolute_links)[0]

                        if "3060" in TITULO:
                            LISTA60_TITULO.append(TITULO)
                            LISTA60_PRECO.append(PRECO)
                            LISTA60_LINK.append(LINK)

                        if "3070" in TITULO:
                            LISTA70_TITULO.append(TITULO)
                            LISTA70_PRECO.append(PRECO)
                            LISTA70_LINK.append(LINK)

pagina = session.get(TERABYTE)
pagina.html.render(scrolldown=10, sleep=1)
ELEMENT = pagina.html.find("div")
for E in ELEMENT:
    if "id" in E.attrs:
        if E.attrs["id"] == "prodarea":
            DIVS = E.find("div")
            for D in DIVS:
                if "class" in D.attrs:
                    if "commerce_columns_item_inner" in D.attrs["class"]:
                        DIVS2 = D.find("div")
                        for D2 in DIVS2:
                            if "class" in D2.attrs:
                                if "commerce_columns_item_caption" in D2.attrs["class"]:
                                    TITULO = D2.text
                                    LINK = list(D2.absolute_links)[0]
                                if "commerce_columns_item_info" in D2.attrs["class"]:
                                    DIVS3 = D2.find("div")
                                    for D3 in DIVS3:
                                        if "class" in D3.attrs:
                                            if "prod-new-price" in D3.attrs["class"]:
                                                PRECO = float("".join([p for p in D3.text if p in "0123456789,"]).replace(",", "."))
                                                if PRECO:
                                                    if "3060" in TITULO:
                                                        LISTA60_TITULO.append(TITULO)
                                                        LISTA60_PRECO.append(PRECO)
                                                        LISTA60_LINK.append(LINK)

                                                    if "3070" in TITULO:
                                                        LISTA70_TITULO.append(TITULO)
                                                        LISTA70_PRECO.append(PRECO)
                                                        LISTA70_LINK.append(LINK)

MIN60 = min(LISTA60_PRECO)
ID60 = LISTA60_PRECO.index(MIN60)

MIN70 = min(LISTA70_PRECO)
ID70 = LISTA70_PRECO.index(MIN70)

print("")
print("MENOR PREÇO 3060:")
print(LISTA60_TITULO[ID60])
print(LISTA60_PRECO[ID60])
print(LISTA60_LINK[ID60])
print("")

print("MENOR PREÇO 3070:")
print(LISTA70_TITULO[ID70])
print(LISTA70_PRECO[ID70])
print(LISTA70_LINK[ID70])
print("")
input('Pressione ENTER para sair...')