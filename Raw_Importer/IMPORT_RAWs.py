from exifread import process_file
import os
from shutil import copy
from glob import glob
import threading
import PySimpleGUIQt as sg

sg.ChangeLookAndFeel("SystemDefaultForReal")

Layout = [
    [sg.Stretch(), sg.Text("Este programa importa RAWs em CR2 para a pasta selecionada subdividindo por data."), sg.Stretch()],
    [sg.T("")],
    [sg.Stretch(), sg.Text("Pasta RAWs:", size=(10, 1)), sg.Input("", do_not_clear=True, size=(40, 1), key="raws"), sg.FolderBrowse("Pasta", size=(10, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Text("Pasta de Saída:", size=(10, 1)), sg.Input("", do_not_clear=True, size=(40, 1), key="saida"), sg.FolderBrowse("Pasta", size=(10, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Button("Executar", focus=True, size=(10, 1)), sg.Exit("Sair", focus=False, size=(10, 1)), sg.Stretch()],
    [sg.T("")],
    [sg.ProgressBar(max_value=100, key="prog", orientation="h")],
    [sg.T("")],
    [sg.T("Mensagens:")],
    [sg.Output()],
]


window = sg.Window("Importar CR2s", size=(560, 460)).Layout(Layout)


def func():
    files = glob(Origem + r"\**\*.CR2", recursive=True)
    n1 = 0
    n2 = 0
    maxfiles = len(files)
    n3 = 0
    for file in files:
        n3 += 1
        porgress.UpdateBar(int(n3 / maxfiles * 100))
        window.Refresh()
        f = open(file, "rb")
        nome = os.path.basename(file)
        tags = process_file(f, details=False, stop_tag="DateTime")
        data = str(tags["Image DateTime"].values).split(" ")[0]
        data = data.split(":")
        ano = data[0]
        mes = data[1]
        dia = data[2]
        if not os.path.isdir("{0}\\{1}".format(pasta, ano)):
            os.mkdir("{0}\\{1}".format(pasta, ano))
        if not os.path.isdir("{0}\\{1}\\{1}-{2}-{3}".format(pasta, ano, mes, dia)):
            os.mkdir("{0}\\{1}\\{1}-{2}-{3}".format(pasta, ano, mes, dia))
        if not os.path.isfile("{0}\\{1}\\{1}-{2}-{3}\\{4}".format(pasta, ano, mes, dia, nome)):
            print("IMPORTANDO {0}\\{1}\\{1}-{2}-{3}\\{4}...".format(Origem, ano, mes, dia, nome))
            window.Refresh()
            copy(file, "{0}\\{1}\\{1}-{2}-{3}\\{4}".format(pasta, ano, mes, dia, nome))
            n1 += 1
            window.Refresh()
        else:
            print("ARQUIVO JÁ EXISTE: {0}\\{1}\\{1}-{2}-{3}\\{4}".format(pasta, ano, mes, dia, nome))
            n2 += 1
            window.Refresh()
    print("-" * 55)
    print("PROCESSO CONCLUÍDO")
    print("Arquivos copiados: {0}".format(n1))
    print("Arquivos ignorados: {0}".format(n2))
    window.Refresh()


while True:
    event, values = window.Read(timeout=200)
    porgress = window["prog"]
    if event is None or event == "Sair":
        break
    if event == "Executar":
        try:
            Origem = str(window.FindElement("raws").Get())
            pasta = str(window.FindElement("saida").Get())
            erro = []
            if not os.path.isdir(Origem):
                erro.append(1)
            if not os.path.isdir(pasta):
                erro.append(2)
            if erro:
                if 1 in erro:
                    sg.PopupOK("ERRO: O caminho 'Pasta RAWs' não existe.")
                if 2 in erro:
                    sg.PopupOK("ERRO: O caminho 'Pasta de Saída' não existe.")
            if not erro:
                threading.Thread(target=func).start()
        except Exception as e:
            print(e)
            window.Refresh()
