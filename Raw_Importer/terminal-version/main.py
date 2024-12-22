from datetime import datetime
from pathlib import Path
from shutil import copy
from tkinter import filedialog as fd

import exiv2
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Input, ProgressBar, RichLog

exiv2.enableBMFF()  # NEEDED TO MAKE EXIV2 WORK WITH CR3 FILES

def listfiles(origin, logger):
    """LIST ALL THE FILES THAT WILL BE PROCESSED.

    Arguments:
    ---------
        origin: Origin path of the files
        logger: Textual's logger.

    Return:
    ------
        FILES: List of files to be processed.

    """
    logger.write("Listing files...")
    files = list(origin.rglob("*.CR2")) + list(origin.rglob("*.CR3"))
    logger.write(f"{len(files)} files found.")

    return files


def define_output(file, outputfolder):
    """READ FILE'S METADATA AND DEFINE THE OUTPUT FOLDER.

    Arguments:
    ---------
        file: File's path.
        outputfolder: Output folder.

    Return:
    ------
        OUTPUT: File's output path.

    """
    output = None

    name = file.name
    img = exiv2.ImageFactory.open(str(file))
    img.readMetadata()
    tags = img.exifData()
    date = None
    for tag in tags:
        current_tag = tag.key()
        tag_val = tag.value()
        if current_tag == "Exif.Image.DateTime":
            date = str(tag_val).split(" ")[0].split(":")
            break
    if date:
        year = date[0]
        month = date[1]
        day = date[2]
        output = Path(outputfolder, year, f"{year}-{month}-{day}", name)

    return output

# @threaded
def copyphoto(orig, dest, logger):
    """CREATE THE DESTINATION AND COPY THE FILE.

    Arguments:
    ---------
        orig: File's origin path.
        dest: File's destination path.
        logger: Textual's logger.

    """
    folder_name = dest.parents[0]

    if not folder_name.is_dir():
        folder_name.mkdir(parents=True)

    if not dest.is_file():
        logger.write(f"[grey50]\tCopying {orig}...")
        copy(orig, dest)

        # ALSO COPY XMP FILE IF EXISTS
        if Path(f"{orig}.xmp").is_file():
            copy(f"{orig}.xmp", f"{dest}.xmp")
    else:
        logger.write(f"[grey50]\tSkipping {orig}, file already exists in destination...")


class RawImporter(App):
    """A Textual app to import CR2s and CR3s raw images."""

    TITLE = "Raw Importer"
    SUB_TITLE = "CR2s and CR3s raw images importer"
    CSS_PATH = "style.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+r", "pasta_raws", "Choose RAWs folder"),
        ("ctrl+o", "pasta_saida", "Choose Output folder"),
        ("ctrl+l", "clear", "Clear log."),

        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="inputs"):
            yield Input(id="raws")
            yield Input(id="output")
        yield ProgressBar(total=100, show_percentage=True, show_eta=False)
        yield RichLog(id="log", auto_scroll=True, markup=True)
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_pasta_raws(self) -> None:
        """An action to define RAWs folder."""
        raw_path = self.query_one("#raws")
        path = Path(fd.askdirectory(initialdir=Path(raw_path.value)))
        if path.exists():
            raw_path.value = str(path)

    def action_pasta_saida(self) -> None:
        """An action to define output folder."""
        out_path = self.query_one("#output")
        path = Path(fd.askdirectory(initialdir=Path(out_path.value)))
        if path.exists():
            out_path.value = str(path)

    def action_clear(self) -> None:
        """An action to clear the log."""
        self.query_one(RichLog).clear()

    def on_mount(self) -> None:
        """Add border to widgets on mount."""
        self.query_one("#raws").border_title = "RAWs folder:"
        self.query_one("#output").border_title = "Output folder:"
        self.query_one(RichLog).border_title = "Log:"


    @on(Input.Submitted)
    @work(exclusive=True, thread=True)
    def exec(self) -> None:
        """An action to execute the import."""
        logger = self.query_one(RichLog)
        container = self.query_one("#inputs")
        progressbar = self.query_one(ProgressBar)

        time = datetime.now()

        raw_folder = self.query_one("#raws").value
        raw_path = Path(raw_folder)

        output_folder = self.query_one("#output").value
        output_path = Path(output_folder)

        if not raw_folder or not output_path.is_dir():
            self.notify(f"The output folder '{output_path}' does not exists.",title="ERROR", severity="error", timeout=10)
            return

        if not output_folder or not raw_path.is_dir():
            self.notify(f"The RAWs folder '{raw_path}' does not exists.",title="ERROR", severity="error", timeout=10)
            return

        container.loading = True
        progressbar.total = 100
        progressbar.update(progress=0)

        files = listfiles(raw_path, logger)
        count_files = len(files)

        for i, file in enumerate(files):
            dest = define_output(file, output_path)
            if dest:
                copyphoto(file, dest, logger)
            else:
                print(f"[bold red1]File {file} does not have date metadata, skipping...")
            progressbar.update(progress=(i * 100) / count_files)

        logger.write(f"[bold spring_green3]{count_files} FILES IMPORTED IN {datetime.now() - time}.")
        self.bell()
        container.loading = False

if __name__ == "__main__":
    app = RawImporter()
    app.run()
