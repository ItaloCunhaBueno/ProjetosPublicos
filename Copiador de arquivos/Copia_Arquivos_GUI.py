from glob import glob
from shutil import copy
from os.path import basename, isdir
import threading
import PySimpleGUIQt as sg

sg.ChangeLookAndFeel('SystemDefaultForReal')

layout = [[sg.Stretch(), sg.T("COPIADOR DE ARQUIVOS"), sg.Stretch()],
[sg.T("ARQUIVOS:", tooltip='Local onde as pastas contendo os documentos estão.', size=(10,1)), sg.I("", do_not_clear=True, size=(92, 1), key='Files', tooltip='Local onde as pastas contendo os documentos estão.'), sg.FolderBrowse("PASTA", size=(8, 1), tooltip='Procurar pasta.'), sg.Stretch()],
[sg.T("EXTENSÃO:", tooltip='Local onde as pastas contendo os documentos estão.', size=(10,1)), sg.I("", do_not_clear=True, size=(5, 1), key='Ext', tooltip='Local onde as pastas contendo os documentos estão.'), sg.T("(sem ponto, Ex: pdf)"), sg.Stretch()],
[sg.T("SAÍDA:", tooltip='Local onde os documentos serão copiados.', size=(10,1)), sg.I(size=(92, 1), key='Saida', tooltip='Local onde as pastas contendo os documentos estão.'), sg.FolderBrowse("PASTA", size=(8, 1), tooltip='Procurar pasta.'), sg.Stretch()],
[sg.B('EXECUTAR', tooltip='Executar análise.', key='exec', size=(10, 1))],
[sg.T("MENSAGENS:", size=(14, 1), tooltip='Mensagens provindas do processo executado.'), sg.Stretch(), sg.B("MODO DE USAR", key='usar', tooltip='Descrição do preenchimento de cada campo.', size=(15, 1))],
[sg.Output(key='out')],
[sg.B("LIMPAR", key='limpar', size=(10, 1), tooltip="Limpa o texto da caixa de mensagens."), sg.ProgressBar(max_value=100, key="prog", orientation="h")]]

window = sg.Window("COPIADOR DE ARQUIVOS", size=(800, 480)).Layout(layout)

def func():
    files = glob(PASTA_PA + "\\**\\*.{0}".format(EXT), recursive=True)
    print("Iniciando cópia...\n")
    window.Refresh()
    totalfiles = len(files)
    nfiles = 0
    copiados = 0
    erros = 0
    for f in files:
        nfiles += 1
        progress.UpdateBar(int(nfiles / totalfiles * 100))
        window.Refresh()
        name = basename(f)
        dst = "{0}\\{1}".format(PASTA_SAIDA, name)
        try:
            copy(f, dst)
            copiados += 1
            print("'{0}' copiado com sucesso.".format(f))
            window.Refresh()
        except:
            erros += 1
            print("não foi possivel copiar '{0}'".format(f))
            window.Refresh()
    print("\nPROCESSO CONCLUÍDO")
    print("-----------------------------------------------------------------")
    print("Total de arquivos processados: {0}".format(totalfiles))
    print("Arquivos copiados: {0}".format(copiados))
    print("Erros: {0}".format(erros))
    print("")
    window.Refresh()


while True:
    event, values = window.read()
    progress = window['prog']
    if event is None or event == 'sair':
        break
    if event == 'usar':
        sg.PopupOK("Esta ferramenta tem como objetivo copiar recursivamente todos os arquivos com a extensão .'EXTENSÃO' na pasta 'ARQUIVOS' para a pasta 'SAÍDA'.", non_blocking=False, keep_on_top=True)
    if event == 'limpar':
        window['out'].Update('')
        window.Refresh()
    if event == 'exec':
        try:
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
                threading.Thread(target=func).start()
        except Exception as e:
            print(e)
            window.Refresh()
