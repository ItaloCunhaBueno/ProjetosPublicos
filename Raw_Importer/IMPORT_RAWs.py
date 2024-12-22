#
#   IMPORTA ARQUIVOS RAW CR2 E CR3 PARA A PASTA DESTINO ORGANIZANDO EM SUBPASTAS DIVIDIDAS POR DATA
#

from pathlib import Path
from shutil import copy
from threading import Thread

import exiv2
import PySimpleGUIQt as sg

exiv2.enableBMFF()  # NECESSARIO PARA QUE A BIBLIOTECA EXIV2 FUNCIONE COM ARQUIVOS CR3
sg.ChangeLookAndFeel("SystemDefaultForReal")  # DEFINE O ESTILO DA INTERFACE PARA O PADRAO DO SISTEMA

# INTERFACE GRAFICA
LAYOUT = [
    [sg.Stretch(), sg.Text("Este programa importa RAWs em CR2 e CR3 para a pasta selecionada subdividindo por data."), sg.Stretch()],
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
    """DECORADOR QUE TRANSFORMA A FUNCAO EM SUA PROPRIA THREAD."""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def listfiles(origem):
    """LISTA TODAS AS FOTOS QUE SERÃO IMPORTADAS.

    Arguments:
    ---------
        origem: Caminho de origem do arquivo

    Return:
    ------
        FILES: Lista de arquivos a serem processados

    """
    print("Listando arquivos...")
    files = list(origem.rglob("*.CR2")) + list(origem.rglob("*.CR3"))
    return files


def define_output(file, outputfolder):
    """LE O METADATA DE DATA DO ARQUIVO E DEFINE O LOCAL DE SAIDA.

    Arguments:
    ---------
        file: Caminho de origem do arquivo
        outputfolder: Pasta de destino do arquivo

    Return:
    ------
        OUTPUT: Caminho de destino do arquivo

    """
    output = None

    nome = file.name
    img = exiv2.ImageFactory.open(str(file))
    img.readMetadata()
    tags = img.exifData()
    data = None
    for tag in tags:
        current_tag = tag.key()
        tag_val = tag.value()
        if current_tag == "Exif.Image.DateTime":
            data = str(tag_val).split(" ")[0].split(":")
            break
    if data:
        ano = data[0]
        mes = data[1]
        dia = data[2]
        output = Path(outputfolder, ano, f"{ano}-{mes}-{dia}", nome)

    return output

@threaded
def copyphoto(orig, dest):
    """CRIA O DESTINO E COPIA O ARQUIVO.

    Arguments:
    ---------
        orig: Caminho de origem do arquivo
        dest: Caminho de destino do arquivo

    """
    folder_name = dest.parents[0]

    if not folder_name.is_dir():
        folder_name.mkdir(parents=True)

    if not dest.is_file():
        print(f"Copiando {orig}...")
        copy(orig, dest)

        # COPIA TAMBEM O ARQUIVO XMP CASO EXISTA
        if Path(f"{orig}.xmp").is_file():
            copy(f"{orig}.xmp", f"{dest}.xmp")
    else:
        print(f"Ignorando {orig}, arquivo já existente na pasta destino...")


@threaded
def main(origfolder, destfolder, window):
    """PROCESSO PRINCIPAL.

    Arguments:
    ---------
        origfolder: Pasta de origem dos arquivos
        destfolder: Pasta de destino dos arquivos
        window: Interface grafica

    """
    files = listfiles(origfolder)
    count_files = len(files)
    count = 0

    for file in files:
        dest = define_output(file, destfolder)
        if dest:
            copyphoto(file, dest)
        else:
            print(f"Arquivo {file} não possui metadata de data, ignorando...")
        count += 1
        window["prog"].UpdateBar((count * 100) / count_files)
        window.Refresh()

    print("-" * 55)
    print("PROCESSO CONCLUÍDO")
    print(f"Arquivos processados: {count}")
    window.Refresh()


# MAIN LOOP DA INTERFACE GRAFICA
while True:
    event, values = WINDOW.Read()

    if event in [None, "Sair", sg.WINDOW_CLOSED]:
        break

    if event == "Executar":
        ORIGEM = Path(values["raws"])
        DESTINO = Path(values["saida"])
        ERROS = False

        if not ORIGEM.is_dir():
            sg.PopupError("ERRO: O caminho 'Pasta RAWs' não existe.")
            ERROS = True

        if not DESTINO.is_dir():
            sg.PopupError("ERRO: O caminho 'Pasta de Saída' não existe.")
            ERROS = True

        if not ERROS:
            main(ORIGEM, DESTINO, WINDOW)

WINDOW.close()
