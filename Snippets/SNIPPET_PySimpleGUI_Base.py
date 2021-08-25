import PySimpleGUI as sg

sg.theme("SystemDefaultForReal")

# DEFINE O LAYOUT
LAYOUT = [[]]

# DEFINE A JANELA
WINDOW = sg.Window("Titulo", layout=LAYOUT, size=(500, 500))

# MAIN LOOP
while True:
    events, values = WINDOW.read()

    # EVENTO PARA FECHAR A JANELA
    if events in (sg.WIN_CLOSED, "Exit"):
        break

# FINALIZA A JANELA
WINDOW.close()
