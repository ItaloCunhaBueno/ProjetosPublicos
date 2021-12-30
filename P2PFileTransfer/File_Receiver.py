import os
from pathlib import Path
from flask import Flask, send_file, request, make_response
from werkzeug.utils import secure_filename
import click
import logging
import socket

# DESABILITA O LOGGING DO FLASK
log = logging.getLogger("werkzeug")
log.disabled = True

# DEFINE A PASTA DE DOWNLOADS DO WINDOWS ONDE OS ARQUIVOS SERÃO SALVOS
DOWNLOADS_FOLDER = Path(f"{Path.home()}/Downloads")
if not DOWNLOADS_FOLDER.exists():
    DOWNLOADS_FOLDER.mkdir(parents=True)

# CRIA O SERVIDOR
app = Flask(__name__)

# FUNÇÃO PARA PRINTAR A BARRA DE PROGRESSO DOS ARQUIVOS
def progressBar(current, total, arquivo, barLength=20):
    """
    FUNÇÃO PARA PRINTAR A BARRA DE PROGRESSO DO ARQUIVO
    """
    percent = round(float(current) * 100 / total, 2)
    arrow = "█" * int(percent / 100 * barLength)
    spaces = "░" * (barLength - len(arrow))
    click.echo("\rRecebendo '{3}': |{0}{1}| {2}%".format(arrow, spaces, percent, arquivo), nl=False)


# ROTA DE ENTRADA PARA O SERVIDOR
@app.route("/")
@app.route("/index")
def index():

    # ENVIA A PÁGINA index.html PARA O CLIENTE
    return send_file("index.html")


# DEFINE A ROTA PARA O ARQUIVO DE DOWNLOAD
@app.route("/upload", methods=["POST"])
def upload():

    # ARQUIVO RECEBIDO
    file = request.files["file"]

    # DEFINE O CAMINHO DE SALVAMENTO DO ARQUIVO
    save_path = os.path.join(DOWNLOADS_FOLDER, secure_filename(file.filename))

    # RETORNA O CHUNK ATUAL DO ARQUIVO SENDO RECEBIDO
    current_chunk = int(request.form["dzchunkindex"])

    # RETORNA UM ERRO CASO O ARQUIVO JA EXISTA NA PASTA E CONTENHA DADOS
    if os.path.exists(save_path) and current_chunk == 0:

        # CODIGOS 400 E 500 DIZEM AO DROPZONE QUE UM ERRO OCORREU
        return make_response(("ERRO: Arquivo já existe.", 400))

    # ESCREVE O ARQUIVO NA PASTA DE DOWNLOADS
    try:
        with open(save_path, "ab") as f:
            f.seek(int(request.form["dzchunkbyteoffset"]))
            f.write(file.stream.read())

    # RETORNA UMA MENSAGEM DE ERRO CASO O PROCESSO FALHE
    except OSError:

        # LOG.EXCEPTION WILL INCLUDE THE TRACEBACK SO WE CAN SEE WHAT'S WRONG
        click.echo("ERRO: Não foi possível salvar o arquivo.")
        return make_response(("ERRO: Não foi possível salvar o arquivo.", 500))

    # DEFINE O TOTAL DE CHUNKS DO ARQUIVO
    total_chunks = int(request.form["dztotalchunkcount"])

    # VERIFICA SE O ARQUIVO FOI RECEBIDO POR COMPLETO
    if current_chunk + 1 == total_chunks:

        # EMITE UMA MENSAGEM DE ERRO CASO O TAMANHO DO ARQUIVO SALVO SEJA DIFERENTE DO ARQUIVO ENVIADO
        if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
            progressBar(total_chunks, total_chunks, file.filename)
            click.echo(f"Arquivo '{file.filename}' completo, mas seu tamanho difere do original. Tamanho salvo é {os.path.getsize(save_path)} mas deveria ser {request.form['dztotalfilesize']}.")
            return make_response(("ERRO: Tamanho difere.", 500))

        # CASO TUDO OCORRA BEM, EMITE UMA MENSAGEM DE SUCESSO
        else:
            progressBar(total_chunks, total_chunks, file.filename)
            click.echo(f"\nArquivo '{file.filename}' recebido com sucesso.")
            return make_response(("Arquivo enviado com sucesso!", 200))

    # ATUALIZA A BARRA DE PROGRESSO DO ARQUIVO SENDO RECEBIDO
    else:
        progressBar(current_chunk + 1, total_chunks, file.filename)

    return make_response(("Pedaço enviado.", 200))


# ESCOLHE O IP DO SERVIDOR
def chooseIP():
    # LISTA TODOS OS IPs DO SERVIDOR E ATRIBUI UMA LETRA A ELE
    LETRAS = "abcdefghijklmnopqrstuvwxyz"
    IPs = sorted([i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None) if ":" not in i[4][0]])
    IPs = dict(zip(LETRAS, IPs))

    # SE A REDE POSSUIR MAIS DE UM IP, PERGUNTA AO USUÁRIO QUAL ELE DESEJA USAR
    if len(IPs) > 1:

        # PRINTA MENSAGEM COM TODOS OS IPS
        click.echo("#" * 80)
        click.echo("# Foram encontrados multiplos IPs na sua rede, por favor, escolha o IP do servidor:")

        for letra, ip in IPs.items():
            click.echo(f"# {letra}) {ip}")

        click.echo("#" * 80)
        # SOLICITA O INPUT DO IP DESEJADO
        IP = input("# Digite a letra: ")

        # CASO O INPUT SEJA INVÁLIDO, FECHA O PROGRAMA
        if IP not in IPs:
            click.echo("# Letra inválida.")
            input("# Pressione ENTER para sair.")
            exit()

        IP = IPs[IP]

    # CASO NÃO HAJA MAIS DE UM IP, O SERVIDOR SERÁ O PRIMEIRO IP DA REDE
    else:
        IP = IPs[LETRAS[0]]

    return IP


# SE O ARQUIVO FOR EXECUTADO DIRETAMENTE, INICIA O SERVIDOR
if __name__ == "__main__":

    # ESCOLHE O IP DO SERVIDOR
    SERVERIP = chooseIP()

    # IMPORTA O SERVIDOR WSGI
    from waitress import serve

    # PRINTA ALGUMAS MENSAGENS
    MENSAGEM = f"""\n################################################################################
# Compartilhe este endereço para receber os arquivos: 'http://{SERVERIP}:1337/'")
# Os arquivos são recebidos na pasta '{DOWNLOADS_FOLDER}'
# Para fechar o servidor, pressione CTRL+C ou apenas feche esta janela.
################################################################################"""
    print(MENSAGEM)

    # INICIA O SERVIDOR
    serve(app, host=SERVERIP, port=1337)
