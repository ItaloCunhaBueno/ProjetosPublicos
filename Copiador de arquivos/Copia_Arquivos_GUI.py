from glob import glob
from shutil import copyfile
from os.path import basename, isdir
import PySimpleGUIQt as sg

sg.theme('Reddit')

layout = [[sg.Stretch(), sg.T("COPIADOR DE ARQUIVOS"), sg.Stretch()],
[sg.T("ARQUIVOS:", tooltip='Local onde as pastas contendo os documentos estão.', size=(10,1)), sg.I(size=(92, 1), key='Files', tooltip='Local onde as pastas contendo os documentos estão.'), sg.FolderBrowse("PASTA", size=(8, 1), tooltip='Procurar pasta.')],
[sg.T("EXTENSÃO:", tooltip='Local onde as pastas contendo os documentos estão.', size=(10,1)), sg.I(size=(5, 1), key='Ext', tooltip='Local onde as pastas contendo os documentos estão.'), sg.T("(sem ponto, Ex: pdf)")],
[sg.T("SAÍDA:", tooltip='Local onde os documentos serão copiados.', size=(10,1)), sg.I(size=(92, 1), key='Saida', tooltip='Local onde as pastas contendo os documentos estão.'), sg.FolderBrowse("PASTA", size=(8, 1), tooltip='Procurar pasta.')],
[sg.B('EXECUTAR', tooltip='Executar análise.', key='exec', size=(10, 1))],
[sg.T("MENSAGENS:", size=(14, 1), tooltip='Mensagens provindas do processo executado.'), sg.Stretch(), sg.B("MODO DE USAR", key='usar', tooltip='Descrição do preenchimento de cada campo.', size=(15, 1))],
[sg.Multiline(disabled=True, autoscroll=True, do_not_clear=True, size=(110, 18), key='multi')],
[sg.B("LIMPAR", key='limpar', size=(10, 1), tooltip="Limpa o texto da caixa de mensagens.")]]

window = sg.Window("COPIADOR DE ARQUIVOS", layout=layout, size=(800, 480), element_justification="LEFT", auto_size_buttons=True, auto_size_text=True, font="SEGOEUI 10", default_button_element_size=(10, 1), border_depth=0)

while True:
    event, values = window.read()
    if event is None or event == 'sair':
        break
    if event == 'usar':
        sg.PopupOK("Esta ferramenta tem como objetivo copiar recursivamente todos os arquivos com a extensão .'EXTENSÃO' na pasta 'ARQUIVOS' para a pasta 'SAÍDA'.", non_blocking=False, keep_on_top=True)
    if event == 'limpar':
        window['multi'].Update('')
        window.Refresh()
    if event == 'exec':
        PASTA_PA = window['Files'].Get()
        PASTA_SAIDA = window['Saida'].Get()
        EXT = window['Ext'].Get()
        error = 0
        if not isdir(PASTA_PA):
            error +=1
            sg.PopupOK("Campo 'ARQUIVOS' não é um caminho válido.", non_blocking=False, keep_on_top=True)
        if not isdir(PASTA_SAIDA):
            error +=1
            sg.PopupOK("Campo 'SAÍDA' não é um caminho válido.", non_blocking=False, keep_on_top=True)
        if EXT == None or EXT == "" or EXT == " ":
            error +=1
            sg.PopupOK("É necessario indicar uma extensão no campo 'EXTENSÃO'.", non_blocking=False, keep_on_top=True)
        if error == 0:
            files = glob(PASTA_PA + "\\**\\*.{0}".format(EXT), recursive=True)
            window['multi'].update("Iniciando cópia...\n\n", append=True)
            window.Refresh()
            totalfiles = len(files)
            copiados = 0
            erros = 0
            for f in files:
                name = basename(f)
                dst = "{0}\\{1}".format(PASTA_SAIDA, name)
                try:
                    copyfile(f, dst)
                    copiados += 1
                    window['multi'].update("'{0}' copiado com sucesso.\n".format(f), append=True)
                    window.Refresh()
                except:
                    erros += 1
                    window['multi'].update("não foi possivel copiar '{0}'\n".format(f), append=True)
                    window.Refresh()
            window['multi'].update("\nPROCESSO CONCLUÍDO\n", append=True)
            window['multi'].update("-----------------------------------------------------------------\n", append=True)
            window['multi'].update("Total de arquivos processados: {0}\n".format(totalfiles), append=True)
            window['multi'].update("Arquivos copiados: {0}\n".format(copiados), append=True)
            window['multi'].update("Erros: {0}\n".format(erros), append=True)
            window['multi'].update("\n", append=True)
            window.Refresh()