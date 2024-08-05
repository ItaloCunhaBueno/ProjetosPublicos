from asyncio import new_event_loop, set_event_loop
from datetime import datetime
from pathlib import Path
from tkinter import filedialog as fd
from typing import ClassVar

from spotdl import Spotdl
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    Footer,
    Header,
    Input,
    ProgressBar,
    RadioButton,
    RichLog,
)


class SpotDL(App):
    """A Textual app to download songs."""

    TITLE = "SpotDL"
    SUB_TITLE = "Music Downloader"
    CSS_PATH = "style.css"

    # PARA QUE O CLIENT SPOTIFY NAO SUMA E PRECISO CRIAR ESSE EVENT LOOP
    LOOP = new_event_loop()
    SPOTIFY_CLIENT = Spotdl(client_id="", client_secret="", headless=True, loop=LOOP)

    BINDINGS: ClassVar[list[tuple]] = [
        ("escape", "quit", "Sair"),
        ("ctrl+t", "toggle_dark", "Tema escuro"),
        ("ctrl+l", "clear", "Limpar mensagens"),
        ("ctrl+p", "procurar_pasta", "Procurar pasta de saida"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        with Container(id="inputs"):
            with Horizontal():
                yield Input(str(Path(Path.home(), "Music")), id="pasta_saida")
                yield RadioButton(value=False, label="Separar por artista e album")
            yield Input(placeholder="URL do Spotify ou 'ARTISTA - NOME DA MUSICA'", id="search")
        with Container(id="logs"):
            yield ProgressBar(total=100, show_eta=False)
            yield RichLog(id="log", auto_scroll=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#pasta_saida").border_title = "Pasta de saída:"
        self.query_one("#search").border_title = "Música, Album ou Playlist:"
        self.query_one(RichLog).border_title = "Mensagens"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit(self) -> None:
        """An action to quit the app."""
        self.exit()

    def action_clear(self) -> None:
        """An action to clear the log."""
        self.query_one(RichLog).clear()

    def action_procurar_pasta(self) -> None:
        """An action to search for output folder."""
        output_folder = self.query_one("#pasta_saida")
        path = Path(fd.askdirectory(initialdir=Path(output_folder.value)))
        if path.exists():
            output_folder.value = str(path)

    @on(Input.Submitted)
    @work(exclusive=True, thread=True)
    def baixa_musica(self) -> None:
        """An action to search for songs."""
        # SETA O EVENT LOOP PARA O CRIADO ANTERIORMENTE PARA QUE O CLIENT SPOTIFY NAO SUMA
        set_event_loop(self.LOOP)

        logger = self.query_one(RichLog)
        container = self.query_one("#inputs")
        progressbar = self.query_one(ProgressBar)
        album = self.query_one(RadioButton).value

        hora = datetime.now()

        pasta_saida_valor = self.query_one("#pasta_saida").value
        pasta_saida = Path(pasta_saida_valor)

        url_valor = self.query_one("#search").value

        if not pasta_saida_valor or not pasta_saida.is_dir():
            self.notify(f"A pasta de saída '{pasta_saida}' não existe.", title="ERRO", severity="error", timeout=10)
            return

        if not url_valor:
            self.notify("Digite uma URL do Spotify ou o nome de uma música.", title="ERRO", severity="error", timeout=10)
            return

        container.loading = True
        progressbar.total = 100
        progressbar.update(progress=0)
        logger.write("\nProcurando músicas...")

        output = str(Path(pasta_saida, r"{artist} - {title}.{output-ext}")) if not album else str(Path(pasta_saida, r"{artist}", r"{album}", r"{artist} - {title}.{output-ext}"))

        self.SPOTIFY_CLIENT.downloader.settings["output"] = output

        songs = self.SPOTIFY_CLIENT.search([url_valor])
        n_songs = len(songs)
        logger.write(f"[bold spring_green3]{n_songs} músicas encontradas:")

        for i, s in enumerate(songs, start=1):
            logger.write(f"[grey50]\t{i}. Baixando '{s.artist} - {s.name}'...")
            _, path = self.SPOTIFY_CLIENT.download(s)
            if not path:
                logger.write(f"[bold red1]\tERRO: '{s.artist} - {s.name}' não foi baixado.")
            progressbar.update(progress=(100 / n_songs) * i)

        logger.write(f"[bold spring_green3]PROCESSO CONCLUIDO EM {datetime.now() - hora}.")
        self.bell()
        container.loading = False


if __name__ == "__main__":
    app = SpotDL()
    app.run()
