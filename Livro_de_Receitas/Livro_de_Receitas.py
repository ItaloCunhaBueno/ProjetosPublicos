import PySimpleGUIQt as sg
import sqlite3
from os import path
import sys
import base64
from PIL import Image
from io import BytesIO
from pprint import pprint
from PySimpleGUIQt.PySimpleGUIQt import POPUP_BUTTONS_NO_BUTTONS
import fitz

if getattr(sys, 'frozen', False):
    RUNPATH = path.dirname(sys.executable)
elif __file__:
    RUNPATH = path.dirname(__file__)

print(path.dirname(sys.executable))
print(path.dirname(__file__))

NO_IMG = b"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"


def ImageToBase64(url):
    if url:
        img = Image.open(url)
        img.thumbnail((300, 300), Image.BICUBIC)
        im_file = BytesIO()
        if (
            url.endswith("jpg")
            or url.endswith("jpeg")
            or url.endswith("JPG")
            or url.endswith("JPEG")
        ):
            img.save(im_file, format="JPEG")
        elif url.endswith("png") or url.endswith("PNG"):
            img.save(im_file, format="PNG")
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        im_b64 = base64.b64encode(im_bytes)
        return im_b64
    else:
        return ""


def base64ToImage(BASE64CODE):
    imgdata = base64.b64decode(BASE64CODE)
    pix = fitz.Pixmap(imgdata)  # any image type supported by PyMuPDF
    data = pix.getImageData("png")
    return data


def createDB():
    if not path.isfile(RUNPATH + "\\receitas.db"):
        con = sqlite3.connect(RUNPATH + "\\receitas.db")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE receitas
               (id integer primary key autoincrement, nome text not null, categoria text, ingredientes text not null, preparo blob not null, foto blob)"""
        )
        con.close()


def connectDB():
    con = sqlite3.connect(RUNPATH + "\\receitas.db")
    return con


def insertDB(con, values):
    cur = con.cursor()
    cur.execute(
        "insert into receitas(nome, ingredientes, preparo, foto, categoria) values(?,?,?,?,?)",
        values,
    )
    con.commit()


sg.theme("SystemDefaultForReal")


def janelareceita(
    NOME, RECEITA_IMAGEM, RECEITA_INGREDIENTES, RECEITA_CATEGORIAS, RECEITA_MODOPREPARO
):
    window.Disable()
    LAYOUT2 = [
        [sg.Stretch(), sg.Text(NOME, font=("SegoeUI bold", 24)), sg.Stretch()],
        [sg.HorizontalSeparator()],
        [
            sg.Column(
                [
                    [sg.Stretch(), sg.Image(data=RECEITA_IMAGEM), sg.Stretch()],
                    [sg.Text("Ingredientes:")],
                    [sg.Listbox(RECEITA_INGREDIENTES)],
                    [sg.Text("Categorias:")],
                    [sg.Listbox(RECEITA_CATEGORIAS)],
                ]
            ),
            sg.VerticalSeparator(),
            sg.Column(
                [[sg.Text("MODO DE PREPARO:")], [sg.Multiline(RECEITA_MODOPREPARO)]]
            ),
        ],
    ]
    window2 = sg.Window(
        "Livro de Receitas",
        layout=LAYOUT2,
        size=(1200, 600),
        keep_on_top=True,
    )
    while 1:
        event2, values2 = window2.read()
        if event2 == sg.WINDOW_CLOSED:
            break
        window2.close()
    window.Enable()


ABA1_COL1 = [
    [sg.Text("Pesquisa por nome (deixe vazio para ver todas as receitas):")],
    [sg.Input(default_text=path.dirname(sys.executable), key="nome_val"), sg.Button("Pesquisar", size=(10, 1), key="pesq_nome")],
    [
        sg.Text(
            "Pesquisa por ingredientes (separado por vírgula, deixe vazio para ver todas as receitas):"
        )
    ],
    [
        sg.Radio("Apenas", "rgroup", default=True, key="rad_apenas"),
        sg.Radio("Também", "rgroup", key="rad_tambem"),
    ],
    [
        sg.Input(default_text=path.dirname(__file__), key="ingred_val"),
        sg.Button("Pesquisar", size=(10, 1), key="pesq_ingred"),
    ],
    [sg.Text("Resultados:")],
    [sg.Listbox([], enable_events=True, key="resultados")],
]
ABA1_COL2 = [
    [
        sg.Text("Listar todos os ingredientes:"),
        sg.Button("Listar", size=(10, 1), key="con_lista_ingredientes"),
    ],
    [sg.Listbox([], key="con_ingredientes_listbox", enable_events=True)],
]
ABA1_COLS = [[sg.Column(ABA1_COL1), sg.Column(ABA1_COL2)]]
ABA1 = sg.Tab(title="Consultar uma receita", layout=ABA1_COLS, background_color="white")
ABA2_COL1 = [
    [sg.Text("Nome:"), sg.Input(key="in_nome")],
    [
        sg.Text("Foto:  "),
        sg.Input(key="in_foto"),
        sg.FileBrowse(
            "Procurar",
            file_types=(("Imagem", "*.jpg;*.jpeg;*.png;*.JPG;*.JPEG;*.PNG"),),
            size=(10, 1),
        ),
    ],
    [sg.Text("Ingredientes separado por vírgula. Exemplo: cebola, alho, arroz...:")],
    [sg.Input(key="in_ingredientes")],
    [sg.Text("Categorias. Exemplo: assado, salgado, doce...:")],
    [sg.Input(key="in_cat")],
    [sg.Text("Modo de preparo:")],
    [sg.Multiline(key="in_preparo")],
    [sg.Stretch(), sg.Button("Salvar", size=(10, 1), key="in_salvar"), sg.Stretch()],
]
ABA2_COL2 = [
    [
        sg.Text("Lista de ingredientes:"),
        sg.Button("Listar", size=(10, 1), key="in_list_ingred"),
        sg.Text("Lista de categorias:"),
        sg.Button("Listar", size=(10, 1), key="in_list_cat"),
    ],
    [
        sg.Listbox([], key="in_ingred_list", enable_events=True),
        sg.Listbox([], key="in_cat_list", enable_events=True),
    ],
]

ABA2_COLS = [[sg.Column(ABA2_COL1), sg.Column(ABA2_COL2)]]
ABA2 = sg.Tab(title="Anotar uma receita", layout=ABA2_COLS, background_color="white")
LAYOUT = [[sg.TabGroup([[ABA1, ABA2]], background_color="white")]]
window = sg.Window("Livro de Receitas", layout=LAYOUT, size=(1200, 600))
createDB()
conn = connectDB()

while 1:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "in_salvar":
        NOME = window["in_nome"].Get().upper()
        FOTO = ImageToBase64(window["in_foto"].Get())
        INGREDIENTES = [
            a.lstrip(" ").rstrip(" ")
            for a in window["in_ingredientes"].Get().lower().split(",")
            if a != ""
        ]
        PREPARO = window["in_preparo"].Get()
        CATEGORIAS = [
            a.lstrip(" ").rstrip(" ")
            for a in window["in_cat"].Get().lower().split(",")
            if a != ""
        ]
        ERROS = []
        if NOME in (None, "", " "):
            ERROS.append("Nome em branco. Por favor, defina um nome para a receita.")
        if not INGREDIENTES:
            ERROS.append(
                "Ingredientes em branco. Por favor, liste todos os ingredinetes da receita."
            )
        else:
            for I in INGREDIENTES:
                if I in (None, "", " "):
                    ERROS.append(
                        "A lista de ingredientes possui um erro de digitação. Por favor verifique o campo Ingredientes."
                    )
                    break
        if PREPARO in (None, "", " "):
            ERROS.append(
                "Modo de preparo em branco. Por favor, adicione uma descrição do modo de preparo da receita."
            )
        if not ERROS:
            try:
                insertDB(
                    conn,
                    (NOME, ";".join(INGREDIENTES), PREPARO, FOTO, ";".join(CATEGORIAS)),
                )
                window["in_nome"].Update("")
                window["in_foto"].Update("")
                window["in_ingredientes"].Update("")
                window["in_preparo"].Update("")
                window["in_ingred_list"].Update("")
                window["in_cat"].Update("")
                window["in_cat_list"].Update("")
                window.Refresh()
                sg.PopupAutoClose(
                    "Receita inserida com sucesso!",
                    keep_on_top=True,
                    no_titlebar=True,
                    auto_close=True,
                    auto_close_duration=2,
                    button_type=POPUP_BUTTONS_NO_BUTTONS,
                )
            except Exception as e:
                sg.PopupError(
                    f"ERRO. Não foi possível inserir a receita. Por favor verifique os campos preenchidos.\nMotivo:\n{e}",
                    title="ERRO",
                )
        else:
            sg.PopupError(
                "ERRO: os seguintes erros foram encontrados:\n{0}".format(
                    "\n".join(ERROS), title="ERRO"
                )
            )

    if event == "in_list_ingred":
        cur = conn.cursor()
        SQL_INGREDIENTES = cur.execute("select ingredientes from receitas")
        LISTA_INGREDIENTES = []
        for ING in SQL_INGREDIENTES:
            if ING[0]:
                INGS = [
                    LISTA_INGREDIENTES.append(IN)
                    for IN in ING[0].split(";")
                    if IN not in LISTA_INGREDIENTES
                ]
        window["in_ingred_list"].Update(LISTA_INGREDIENTES)
        window.Refresh()

    if event == "in_list_cat":
        cur = conn.cursor()
        SQL_CATEGORIAS = cur.execute("select categoria from receitas")
        LISTA_CATEGORIAS = []
        for CAT in SQL_CATEGORIAS:
            if CAT[0]:
                CATS = [
                    LISTA_CATEGORIAS.append(CA)
                    for CA in CAT[0].split(";")
                    if CA not in LISTA_CATEGORIAS
                ]
        window["in_cat_list"].Update(LISTA_CATEGORIAS)
        window.Refresh()

    if event == "con_lista_ingredientes":
        cur = conn.cursor()
        SQL_INGREDIENTES = cur.execute("select ingredientes from receitas")
        LISTA_INGREDIENTES = []
        for ING in SQL_INGREDIENTES:
            if ING[0]:
                INGS = [
                    LISTA_INGREDIENTES.append(IN)
                    for IN in ING[0].split(";")
                    if IN not in LISTA_INGREDIENTES
                ]
        window["con_ingredientes_listbox"].Update(LISTA_INGREDIENTES)
        window.Refresh()

    if event == "con_ingredientes_listbox":
        if values["con_ingredientes_listbox"]:
            VALUE = values["con_ingredientes_listbox"][0]
            cur = conn.cursor()
            SQL_RECEITAS = cur.execute(
                f"select id, nome from receitas where ingredientes like '%{VALUE}%'"
            )
            LISTA_RECEITAS = []
            for REC in SQL_RECEITAS:
                if f"{REC[0]}. {REC[1]}" not in LISTA_RECEITAS:
                    LISTA_RECEITAS.append(f"{REC[0]}. {REC[1]}")
            window["resultados"].Update(LISTA_RECEITAS)
            window.Refresh()

    if event == "pesq_nome":
        cur = conn.cursor()
        TEXTO = window["nome_val"].Get().upper()
        if TEXTO in (None, ""):
            QUERY = "select id, nome from receitas"
        else:
            QUERY = f"select id, nome from receitas where nome like '%{TEXTO}%'"
        SQL_RECEITAS = cur.execute(QUERY)
        LISTA_RECEITAS = []
        for REC in SQL_RECEITAS:
            if f"{REC[0]}. {REC[1]}" not in LISTA_RECEITAS:
                LISTA_RECEITAS.append(f"{REC[0]}. {REC[1]}")
        window["resultados"].Update(LISTA_RECEITAS)
        window.Refresh()

    if event == "pesq_ingred":
        cur = conn.cursor()
        INGREDIENTES = [
            a.lstrip(" ").rstrip(" ")
            for a in window["ingred_val"].Get().lower().split(",")
            if a != ""
        ]
        if not INGREDIENTES:
            QUERY = "select id, nome from receitas"
        else:
            APENAS = values["rad_apenas"]
            if APENAS:
                TEXTO = f"ingredientes like '%{INGREDIENTES[0]}%'"
                for IN in INGREDIENTES[1:]:
                    TEXTO += f" and ingredientes like '%{IN}%'"
                QUERY = f"select id, nome from receitas where {TEXTO}"
            else:
                TEXTO = f"ingredientes like '%{INGREDIENTES[0]}%'"
                for IN in INGREDIENTES[1:]:
                    TEXTO += f" or ingredientes like '%{IN}%'"
                QUERY = f"select id, nome from receitas where {TEXTO}"
        SQL_RECEITAS = cur.execute(QUERY)
        LISTA_RECEITAS = []
        for REC in SQL_RECEITAS:
            if f"{REC[0]}. {REC[1]}" not in LISTA_RECEITAS:
                LISTA_RECEITAS.append(f"{REC[0]}. {REC[1]}")
        window["resultados"].Update(LISTA_RECEITAS)
        window.Refresh()

    if event == "in_ingred_list":
        if values["in_ingred_list"]:
            VALUE = values["in_ingred_list"][0]
            INGREDIENTES = window["in_ingredientes"].Get()
            if INGREDIENTES in (None, "", " "):
                window["in_ingredientes"].Update(VALUE)
                window.Refresh()
            else:
                if not VALUE in INGREDIENTES:
                    window["in_ingredientes"].Update(INGREDIENTES + f", {VALUE}")
                    window.Refresh()

    if event == "in_cat_list":
        if values["in_cat_list"]:
            VALUE = values["in_cat_list"][0]
            CATEGORIAS = window["in_cat"].Get()
            if CATEGORIAS in (None, "", " "):
                window["in_cat"].Update(VALUE)
                window.Refresh()
            else:
                if not VALUE in CATEGORIAS:
                    window["in_cat"].Update(CATEGORIAS + f", {VALUE}")
                    window.Refresh()

    if event == "resultados":
        if values["resultados"]:
            cur = conn.cursor()
            ID, NOME = values["resultados"][0].split(". ")
            QUERY = f"select nome, foto, ingredientes, categoria, preparo from receitas where id = {ID} and nome = '{NOME}'"
            (
                RECEITA_NOME,
                RECEITA_IMAGEM,
                RECEITA_INGREDIENTES,
                RECEITA_CATEGORIAS,
                RECEITA_MODOPREPARO,
            ) = cur.execute(QUERY).fetchone()
            if RECEITA_IMAGEM in (None, "", " "):
                RECEITA_IMAGEM = NO_IMG
            if RECEITA_INGREDIENTES in (None, "", " "):
                RECEITA_INGREDIENTES = ""
            if RECEITA_CATEGORIAS in (None, "", " "):
                RECEITA_CATEGORIAS = ""

            RECEITA_INGREDIENTES = [
                a for a in RECEITA_INGREDIENTES.split(";") if a != ""
            ]
            RECEITA_CATEGORIAS = [a for a in RECEITA_CATEGORIAS.split(";") if a != ""]
            janelareceita(
                RECEITA_NOME,
                base64ToImage(RECEITA_IMAGEM),
                RECEITA_INGREDIENTES,
                RECEITA_CATEGORIAS,
                RECEITA_MODOPREPARO,
            )

window.close()
