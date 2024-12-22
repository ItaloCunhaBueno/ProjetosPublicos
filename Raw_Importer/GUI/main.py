from collections.abc import Callable, Generator
from datetime import datetime
from pathlib import Path
from shutil import copy
from threading import Thread
from tkinter import Tk
from tkinter.filedialog import askdirectory
from typing import Any

import exiv2
from nicegui import app, ui

exiv2.enableBMFF()  # NECESSARIO PARA QUE A BIBLIOTECA EXIV2 FUNCIONE COM ARQUIVOS CR3
threads = []


def print(message: str) -> None:
    """SUBSTITUI A FUNCAO PRINT PARA A FUNCAO DE LOG DA NICEGUI."""
    log.push(message)
    log.update()


def threaded(fn: Callable[..., Any]) -> Callable[..., Thread]:
    """DECORADOR QUE TRANSFORMA A FUNCAO EM SUA PROPRIA THREAD."""

    def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Thread:
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        threads.append(thread)
        thread.start()
        return thread

    return wrapper


def chunks(lst: list[Any], n: int) -> Generator[list[Any], None, None]:
    """DIVIDE A LISTA EM LISTAS DE N TAMANHO."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def listfiles(origem: Path) -> list[Path]:
    """
    LISTA TODAS AS FOTOS QUE SERÃO IMPORTADAS.

    Arguments:
    ---------
        origem: Caminho de origem do arquivo

    Return:
    ------
        FILES: Lista de arquivos a serem processados

    """
    print("Listando arquivos...")
    return list(origem.rglob("*.CR2", case_sensitive=False)) + list(origem.rglob("*.CR3", case_sensitive=False))


def define_output(file: Path, outputfolder: Path) -> Path | None:
    """
    LE O METADATA DE DATA DO ARQUIVO E DEFINE O LOCAL DE SAIDA.

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


def copyphoto(orig: Path, output_folder: Path, quantidade: int) -> None:
    """
    CRIA O DESTINO E COPIA O ARQUIVO.

    Arguments:
    ---------
        orig: Caminho de origem do arquivo
        output_folder: Caminho de destino do arquivo
        quantidade: Quantidade de arquivos a serem copiados

    """
    dest = define_output(orig, output_folder)
    if not dest:
        print(f"Arquivo {orig} não possui metadata de data, ignorando...")
        return

    folder_name = dest.parents[0]

    if not folder_name.is_dir():
        folder_name.mkdir(parents=True, exist_ok=True)

    if not dest.is_file():
        print(f"Copiando {orig}...")
        copy(orig, dest)

        # COPIA TAMBEM O ARQUIVO XMP CASO EXISTA
        if Path(f"{orig}.xmp").is_file():
            copy(f"{orig}.xmp", f"{dest}.xmp")
    else:
        print(f"Ignorando {orig}, arquivo já existente na pasta destino...")

    barra_progresso.set_value(f"{float(barra_progresso.value.replace("%", "")) + (1/quantidade * 100):.2f}%")
    barra_progresso.update()


@threaded
def seleciona_pasta(elemento: ui.input) -> None:
    """SELECIONA A PASTA PARA O CAMPO INPUT."""
    window = Tk()
    window.wm_attributes("-topmost", 1)
    window.withdraw()
    caminho = askdirectory(mustexist=True, initialdir=Path.home(), parent=window)
    if caminho not in ["", ".", None]:
        elemento.set_value(str(Path(caminho)))
        elemento.update()


def valida_inputs() -> tuple[Path, Path] | None:
    """VALIDA OS INPUTS."""
    valor_1 = valor_pasta_raws.value
    valor_2 = valor_pasta_saida.value
    if not valor_1 or not valor_2:
        with pagina:
            ui.notify("Preencha todos os campos!", type="warning", position="bottom-right", close_button=False)
        return None
    if not Path(valor_1).is_dir() or not Path(valor_2).is_dir():
        with pagina:
            ui.notify("Um dos campos não possui um caminho de pasta válido!", type="warning", position="bottom-right", close_button=False)
        return None
    return (Path(valor_1), Path(valor_2))


def desabilita_botao(botao: ui.button) -> None:
    """DESABILITA UM BOTAO."""
    botao.disable()
    _ = botao.props(add="loading")
    botao.update()


def habilita_botao(botao: ui.button) -> None:
    """HABILITA UM BOTAO."""
    botao.enable()
    _ = botao.props(remove="loading")
    botao.update()


@threaded
def executa() -> None:
    """EXECUTA A IMPORTAÇÃO DE ARQUIVOS."""
    caminhos = valida_inputs()
    if not caminhos:
        return

    hora = datetime.now()
    desabilita_botao(botao_executar)
    botao_sair.disable()

    pasta_raws, pasta_saida = caminhos

    barra_progresso.set_value("0.00%")
    threads = []

    files = listfiles(pasta_raws)
    count_files = len(files)

    threads = chunks([Thread(target=copyphoto, kwargs={"orig": file, "output_folder": pasta_saida, "quantidade": count_files}) for file in files], 10)

    for pacote in threads:
        for t in pacote:
            t.start()

        for t in pacote:
            t.join()

    print("-" * 55)
    print(f"Processo concluído em: {datetime.now() - hora}")
    print(f"Arquivos processados: {count_files}")
    with pagina:
        ui.notify("Processo concluído com sucesso!", type="positive", position="bottom-right", close_button=False)
    habilita_botao(botao_executar)
    botao_sair.enable()


_ = ui.colors(
    primary="#61AFEF",
    secondary="#56B6C2",
    accent="#C678DD",
    positive="#98C379",
    negative="#E06C75",
    info="#61AFEF",
    warning="#E5C07B",
)

with ui.dialog() as dialog, ui.card():
    _ = ui.markdown("""
#### Raw Importer
##### Importação de arquivos RAW para a pasta selecionada subdividindo por data.
- **Pasta RAWs**: Pasta contendo os arquivos RAW a serem importados.
- **Pasta de Saída**: Pasta de destino dos arquivos importados.
""")
    with ui.row().classes("w-full flex items-center justify-end"):
        _ = ui.button("Fechar", on_click=dialog.close).props("flat").classes("rounded-lg")

with ui.column().classes("flex flex-col w-full h-[95dvh] overflow-auto gap-2 p-0 m-0") as pagina:
    with ui.row().classes("w-full flex items-center justify-center rounded-lg bg-neutral-800 p-2"):
        _ = ui.label("Raw Importer").classes("text-lg font-bold")
        _ = ui.separator().classes("flex-1")
        with ui.button(icon="info", on_click=dialog.open).props("flat dense").classes("w-8 aspect-square rounded-lg") as botao_info:
            _ = ui.tooltip("Informações")

    with ui.row().classes("w-full flex items-center justify-center"):
        valor_pasta_raws = ui.input(label="Pasta RAWs:").props("filled dense").classes("flex-1 rounded-lg")
        with ui.button(icon="search", on_click=lambda: seleciona_pasta(valor_pasta_raws)).props("flat dense").classes("w-10 aspect-square rounded-lg") as botao_procura_pasta_raws:
            _ = ui.tooltip("Procurar")
    with ui.row().classes("w-full flex items-center justify-center"):
        valor_pasta_saida = ui.input(label="Pasta de Saída:").props("filled dense").classes("flex-1 rounded-lg")
        with ui.button(icon="search", on_click=lambda: seleciona_pasta(valor_pasta_saida)).props("flat dense").classes("w-10 aspect-square rounded-lg") as botao_procura_pasta_raws:
            _ = ui.tooltip("Procurar")
    with ui.row().classes("w-full flex items-center justify-center"):
        with ui.button("Executar", icon="play_arrow", color="positive", on_click=executa).props("flat").classes("rounded-lg") as botao_executar:
            _ = ui.tooltip("Iniciar a importação")
        with ui.button("Sair", icon="logout", color="negative", on_click=app.shutdown).props("flat").classes("rounded-lg") as botao_sair:
            _ = ui.tooltip("Sair da aplicação")
    barra_progresso = ui.linear_progress(value="0.00%").props("instant-feedback").classes("w-full rounded-full")
    with ui.row().classes("relative flex-1 flex w-full rounded-lg overflow-hidden"):
        log = ui.log().classes("w-full h-full overflow-auto")
        with ui.button("limpar", on_click=lambda: log.clear()).props("flat").classes("absolute top-2 right-2 rounded-lg") as botao_limpar_log:
            _ = ui.tooltip("Limpar o log")
ui.run(title="Raw Importer", native=True, dark=True)
