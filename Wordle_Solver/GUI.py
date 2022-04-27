import PySimpleGUIQt as sg
from os.path import dirname, join

# DEIXA O TEMA DO PROGRAMA NO NATIVO DO OS
sg.theme("SystemDefaultForReal")
font = ("Calibri", 12)

# RETORNA A PASTA DO DICIONARIO
PASTA = dirname(__file__)

# FUNCAO PARA GERAR A LISTA DE PALAVRAS DO DICIONARIO
def load_words(n):
    """
    Carrega todas as palavras com N letras do dicionario TXT e retorna uma lista
    """

    # LISTA DE PALAVRAS ENCONTRADAS
    NWORDS = []

    # ABRE O TXT E SEPARA AS PALAVRAS
    with open(join(PASTA, "Palavras_ASCII.txt"), "r") as words:

        # ITERA AS LINHAS DO DOCUMENTO
        for line in words.readlines():

            # ADICIONA A PALAVRA NA LISTA CASO ELA TENHA O MESMO NUMERO DE CARACTERES QUE O NUMERO DE LETRAS
            if len(line.strip()) == n:
                NWORDS.append(line.strip())

    # RETORNA A LISTA DE PALAVRAS
    return NWORDS


# LAYOUT DO PROGRAMA
LAYOUT = [
    [sg.Stretch(), sg.T("Wordle Solver", font=("Calibri bold", 14)), sg.Stretch()],
    [sg.T("Número de letras:", font=font), sg.Spin(values=[4, 5, 6, 7, 8, 9, 10, 11], initial_value=11, key="num_letters", change_submits=True, font=font), sg.Stretch()],
    [sg.T("Letras amarelas (todas juntas sem espaço):", font=font), sg.InputText(size=(10, 0.8), key="letras_amarelas", background_color="#fcffa3", font=font), sg.Stretch()],
    [sg.T("Letras cinzas (todas juntas sem espaço):     ", font=font), sg.InputText(size=(10, 0.8), key="letras_cinzas", background_color="#bfbfbf", font=font), sg.Stretch()],
    [
        sg.Column(layout=[[sg.Stretch()]]),
        sg.Column(layout=[[sg.InputText(size=(4, 0.8), key=x, background_color="#b0e09b", justification="center", font=font) for x in range(11)]]),
        sg.Column(layout=[[sg.Stretch()]]),
    ],
    [sg.Stretch(), sg.Button("Sugestão", key="solve", size=(10, 1), font=font), sg.Stretch()],
    [sg.HorizontalSeparator()],
    [sg.Output(key="output", size=(60, 20), font=font)],
]

# CRIA A JANELA DO PROGRAMA
WINDOW = sg.Window("Wordle Solver", layout=LAYOUT, resizable=False, size=(600, 400))

# MAIN LOOP
while True:

    # INICIALIZA A JANELA DO PROGRAMA
    EVENT, VALUE = WINDOW.read()

    # GUARDA O NUMERO DE LETRAS SELECIONADAS
    NLETRAS = VALUE["num_letters"]

    # FAZ O UPDATE DO LAYOUT QUANDO MUDA O NUMERO DE LETRAS
    if EVENT == "num_letters":
        for a in range(0, NLETRAS):
            WINDOW[a].update(visible=True)
            WINDOW[a].update(disabled=False)
        for i in range(NLETRAS, 11):
            WINDOW[i].update(visible=False)
            WINDOW[i].update(disabled=True)

    # SE O BOTAO DE SUJESTAO FOR CLICADO EXECUTA O CODIGO
    if EVENT == "solve":

        # LIMPA A JANELA DE OUTPUT
        WINDOW["output"].update("")

        # SEPARA AS LETRAS VERDES EM LISTA E DICIONARIO CONTENDO A POSICAO
        VALUES = []
        DICT = {}
        for n in range(0, NLETRAS):
            DICT[n] = VALUE[n]
            VALUES.append(VALUE[n])

        # LIMPA A LISTA PARA REMOVER OS NULOS E BRANCOS
        VALUES = [V for V in VALUES if (V not in ["", None] and len(V) == 1)]

        # LISTA AS LETRAS AMARELAS
        AMARELAS = list(VALUE["letras_amarelas"])

        # LISTA AS LETRAS CINZAS
        CINZAS = list(VALUE["letras_cinzas"])

        # SE FOI DIGITADO ALGUMA LETRA NO PROGRAMA PROCEDE
        if VALUES or AMARELAS or CINZAS:

            # LISTA DE PALAVRAS COM O NUMERO DE LETRAS SELECIONADO
            WORDS = load_words(NLETRAS)

            # GUARDA AS PALAVRAS QUE BATEM COM AS LETRAS VERDES OU AMARELAS
            MATCH = []

            # ITERA AS PALAVRAS DO DICIONARIO
            for word in WORDS:

                # CONTA A QUANTIDADE DE LETRAS DA PALAVRA QUE BATEM COM AS LETRAS VERDES
                N_MATCHS = 0

                # CONTA A QUANTIDADE DE LETRAS DA PALAVRA QUE BATEM COM AS LETRAS AMARELAS
                A_MATCHS = 0

                # ITERA AS LETRAS DA PALAVRA
                for e, l in enumerate(word):

                    # SE A LETRA DA PALAVRA FOR IGUAL A UMA LETRA VERDE COMPUTA ACERTO
                    if l == DICT[e]:
                        N_MATCHS += 1

                    # SE A LETRA DA PALAVRA FOR IGUAL A UMA LETRA AMARELA COMPUTA ACERTO
                    if l in AMARELAS:
                        A_MATCHS += 1

                # SE EXISTE LETRAS AMARELAS A CONDICAO DEVE SER FEITA COM A QUANTIDADE DE LETRAS AMARELAS E VERDES
                if AMARELAS:
                    if N_MATCHS == len(VALUES) and A_MATCHS == len(AMARELAS):
                        MATCH.append(word)

                # CASO CONTRARIO APENAS AS VERDES
                else:
                    if N_MATCHS == len(VALUES):
                        MATCH.append(word)

            # CASO TENHA ALGUMA PALAVRA NA LISTA DE ACERTOS
            if MATCH:
                FILTRO = []

                # ITERA AS PALVRAS
                for M in MATCH:

                    # IDENTIFICA QUAIS LETRAS CINZAS ESTAO NA PALAVRA
                    LETRASCINZAS = [c for c in M if c in CINZAS]

                    # CASO NAO TENHA LETRAS CINZAS PRINTA A PALAVRA
                    if not LETRASCINZAS:
                        FILTRO.append(M)

                if FILTRO:
                    for F in FILTRO:
                        print(F)

                else:
                    print("Nenhum Resultado")

            # CASO NAO TENHA ENCONTRADO PALAVRAS PRINTA O RESULTADO VAZIO
            else:
                print("Nenhum Resultado")

            # ATUALIZA A JANELA
            WINDOW.Refresh()

        # CASO NENHUMA LETRA SEJA DIGITADA NA JANELA DE INPUT EXIBE A MENSAGEM DE ERRO
        else:
            sg.PopupError("ERRO: Nenhuma letra foi inserida")

    # CASO O PROGRAMA SEJA FECHADO CORTA O MAIN LOOP
    if EVENT in (None, "Exit"):
        break

# FECHA A JANELA
WINDOW.close()
