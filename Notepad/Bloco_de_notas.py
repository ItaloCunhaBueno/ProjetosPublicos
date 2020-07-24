import PySimpleGUI as sg

Layout = [[sg.Multiline(autoscroll=True,size=(100,20),do_not_clear=True, auto_size_text=True, key='texto', background_color='#252525', text_color='#FFFFFF')],
          [sg.Text(' '*50,background_color='#131313', text_color='#131313'), sg.Button('Salvar', key='Salvar', button_color=('#FFFFFF', '#252525')),sg.Button('Limpar', key='clean', button_color=('#FFFFFF', '#252525')), sg.Exit('Sair', button_color=('#FFFFFF', '#AA2525')), sg.Text(" "*44, background_color='#131313', text_color='#131313'), sg.Button("?", key='info', size=(2,1), button_color=('#FFFFFF', '#252525'))]]

window = sg.Window('Bloco de Notas', disable_close=True).Layout(Layout)
window.AutoSizeButtons = False
window.AutoSizeText = True
window.BorderDepth = True
# window.ElementPadding = (10,10)
window.Resizable = False
window.BackgroundColor = '#131313'

while True:
    event, value = window.Read()
    if event is None or event == 'Sair':
        if value:
            if value['texto'] != '\n':
                saida = sg.PopupYesNo('\nTem certeza que deseja sair?\n', text_color='#FFFFFF', background_color='#131313', button_color=('#FFFFFF', '#252525'))
                if saida == 'Yes':
                    break
                elif saida == 'No':
                    pass
            else:
                break
        else:
            break
    elif event == 'clean':
        window.FindElement('texto').Update("")
        window.Refresh()
    elif event == 'info':
        lay_info = [[sg.Text('Bloco de notas.\nCriado por Italo Cunha Bueno como exercício de aprendizagem.\n\nPython 3.7\nPySimpleGUI 3.26\n\nSão Paulo, 03/2019', justification='center', background_color='#131313', text_color='#FFFFFF')],
                    [sg.Button('Fechar', key='info_fecha')]]
        informacao = sg.Window('Informações', no_titlebar=True, keep_on_top=True, background_color='#131313', button_color=('#FFFFFF', '#252525'), force_toplevel=True).Layout(lay_info)
        event2, value2 = informacao.Read()
        if event2 == 'info_fecha':
            informacao.Close()
    elif event == 'Salvar':
        try:
            Save = sg.PopupGetFile('Caminho',no_titlebar=True,no_window=True,save_as=True, file_types=[('Documento de texto','.txt')])
            conteudo = value['texto']
            f = open(Save, 'w+')
            f.write(conteudo)
            f.close()
            lay = [[sg.Text('Arquivo salvo')]]
            mensagem = sg.Window('Salvo',no_titlebar=True, auto_close=True, auto_close_duration=2, keep_on_top=True).Layout(lay).Read()
        except FileNotFoundError:
            pass
