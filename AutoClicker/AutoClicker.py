import keyboard 
import PySimpleGUIQt as sg
from time import sleep
    

sg.theme('Reddit')

Layout = [[sg.T("Tecla para iniciar:"), sg.I(key='in', size=(20, 1))],
          [sg.T("Tecla acionada:"), sg.I(key='do', size=(20, 1))], 
          [sg.T("Tecla para parar:"), sg.I(key='out', size=(20, 1))],
          [sg.T("Intervalo:"), sg.I(default_text='0.1', key='tim', size=(20, 1))],
          [sg.T("Status:"), sg.Stretch(), sg.B("Executar", key='exec', size=(10, 1))],
          [sg.Multiline(autoscroll=True, key='multi', disabled=True)]]

Window = sg.Window("AutoClicker", layout=Layout, font="SEGOEUI 11")

while True:
    event, values = Window.read(timeout=1000)
    if event is None:
        break
    if event == 'exec':
        START = Window['in'].Get()
        END = Window['out'].Get()
        DO = Window['do'].Get()
        TIME = float(Window['tim'].Get().replace(",", '.'))
        if (START == '' or START == ' ' or START is None) or (END == '' or END == ' ' or END is None) or (DO == '' or DO == ' ' or DO is None) or (TIME == '' or TIME == ' ' or TIME is None):
            sg.PopupOK('ERRO: Um ou mais campos estão sem preenchimento.')
        else:
            Window['multi'].Update("Executando...", text_color='green')
            Window.Refresh()
            while True:
                status = False
                if keyboard.is_pressed(START):
                    Window['multi'].Update("ATIVADO", text_color='green')
                    Window.Refresh()
                    while True:
                        keyboard.press_and_release(DO)
                        sleep(TIME)
                        if keyboard.is_pressed(END):
                            Window['multi'].Update("DESATIVADO", text_color='red')
                            Window.Refresh()
                            status = True
                            break
                if status is True:
                    break
