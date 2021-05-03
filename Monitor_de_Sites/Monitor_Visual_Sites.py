from selenium import webdriver
from time import sleep
import winsound
from datetime import datetime
from pushbullet import Pushbullet
from base64 import b64decode


PAGINA = 'https://vacina.mogidascruzes.sp.gov.br/'
PBAPIKEY = ''

pb = Pushbullet(PBAPIKEY)

driverpath = r'C:\Program Files\Python39\selenium\chromedriver.exe'
driver1 = webdriver.Chrome(executable_path=driverpath)
driver1.set_window_position(-10000,0)
driver1.get(PAGINA)
sleep(1)

SCREENSHOT = driver1.get_screenshot_as_base64()

while 1:
    driver1.get(PAGINA)
    print("EXECUTANDO.", end="\r")
    sleep(0.3)
    print("EXECUTANDO..", end="\r")
    sleep(0.3)
    print("EXECUTANDO...", end="\r")
    sleep(0.3)
    SCREENSHOT2 = driver1.get_screenshot_as_base64()    
    if SCREENSHOT2 != SCREENSHOT:
        winsound.MessageBeep()
        IMAGEM = b64decode(SCREENSHOT2)
        file_data = pb.upload_file(IMAGEM, "imagem.png")
        push = pb.push_note("DIFERENCA NOTADA", 'DIFERENCA NOTADA EM {0}, LINK: {1}'.format(datetime.now(), PAGINA))
        push = pb.push_file(**file_data)
        print('DIFERENCA NOTADA EM {0}, LINK: {1}'.format(datetime.now(), PAGINA))
        SCREENSHOT = SCREENSHOT2
        
    sleep(5)
driver1.quit()
