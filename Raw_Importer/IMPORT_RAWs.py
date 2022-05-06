from exifread import process_file
import os
from shutil import copy
from glob import glob
import PySimpleGUIQt as sg
from os.path import join, dirname, isfile, isdir, basename
from threading import Thread

sg.ChangeLookAndFeel("SystemDefaultForReal")

LAYOUT = [
    [sg.Stretch(), sg.Text("Este programa importa RAWs em CR2 para a pasta selecionada subdividindo por data."), sg.Stretch()],
    [sg.T("")],
    [sg.Stretch(), sg.Text("Pasta RAWs:", size=(10, 1)), sg.Input("", do_not_clear=True, size=(40, 1), key="raws"), sg.FolderBrowse("Pasta", size=(10, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Text("Pasta de Saída:", size=(10, 1)), sg.Input("", do_not_clear=True, size=(40, 1), key="saida"), sg.FolderBrowse("Pasta", size=(10, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Button("Executar", focus=True, size=(10, 1)), sg.Exit("Sair", focus=False, size=(10, 1)), sg.Stretch()],
    [sg.Stretch(), sg.ProgressBar(max_value=100, key="prog", size=(6, 1)), sg.Stretch()],
    [sg.HorizontalSeparator()],
    [sg.T("Mensagens:")],
    [sg.Output()],
]

WINDOW = sg.Window("Importar CR2s", layout=LAYOUT, size=(560, 460))


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def listfiles(origem):

    """
    LISTA TODAS AS FOTOS QUE SERÃO IMPORTADAS
    """

    print("Listando arquivos...")
    FILES = glob(origem + r"\**\*.CR2", recursive=True)
    return FILES


def defineOutput(file, outputfolder):

    """
    LE O ARQUIVO E DEFINE O LOCAL DE OUTPUT
    """

    OUTPUT = None

    with open(file, "rb") as F:
        NOME = basename(file)
        TAGS = process_file(F, details=False, stop_tag="DateTime")
        DATA = str(TAGS["Image DateTime"].values).split(" ")[0]
        DATA = DATA.split(":")
        ANO = DATA[0]
        MES = DATA[1]
        DIA = DATA[2]
        OUTPUT = join(f"{outputfolder}", f"{ANO}", f"{ANO}-{MES}-{DIA}", f"{NOME}")

    return OUTPUT


def copyphoto(orig, dest):

    """
    CRIA O DESTINO E COPIA O ARQUIVO
    """

    FOLDERSNAME = dirname(dest).split("\\")

    if not isdir(join(*FOLDERSNAME[:-1])):
        os.mkdir(join(*FOLDERSNAME[:-1]))

    if not isdir(join(*FOLDERSNAME)):
        os.mkdir(join(*FOLDERSNAME))

    if not isfile(dest):
        print(f"Copiando {orig}...")

        copy(orig, dest)

    else:
        print(f"Ignorando {orig}...")

    return 1


@threaded
def main(ORIGFOLDER, DESTFOLDER, WINDOW):

    FILES = listfiles(ORIGFOLDER)
    COUNTFILES = len(FILES)
    COUNT = 0

    for FILE in FILES:
        DEST = defineOutput(FILE, DESTFOLDER)
        N = copyphoto(FILE, DEST)
        COUNT += N
        WINDOW["prog"].UpdateBar((COUNT * 100) / COUNTFILES)
        WINDOW.Refresh()

    print("-" * 55)
    print("PROCESSO CONCLUÍDO")
    print("Arquivos processados: {0}".format(COUNT))
    WINDOW.Refresh()


while True:
    event, values = WINDOW.Read()

    if event in [None, "Sair", sg.WINDOW_CLOSED]:
        break

    if event == "Executar":
        ORIGEM = values["raws"]
        DESTINO = values["saida"]
        ERROS = False

        if not os.path.isdir(ORIGEM):
            sg.PopupError("ERRO: O caminho 'Pasta RAWs' não existe.")
            ERROS = True

        if not os.path.isdir(DESTINO):
            sg.PopupError("ERRO: O caminho 'Pasta de Saída' não existe.")
            ERROS = True

        if not ERROS:

            main(ORIGEM, DESTINO, WINDOW)

WINDOW.close()
