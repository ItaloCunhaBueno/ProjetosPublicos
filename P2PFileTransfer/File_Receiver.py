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


# GUARDA O IP DO SERVIDOR
def serverIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    URL = s.getsockname()[0]
    s.close()
    return URL


# SE O ARQUIVO FOR EXECUTADO DIRETAMENTE, INICIA O SERVIDOR
if __name__ == "__main__":

    # IMPORTA O SERVIDOR WSGI
    from waitress import serve

    # PRINTA ALGUMAS MENSAGENS
    print("\n")
    print("#" * 80)
    print(f"# Compartilhe este endereço para receber os arquivos: 'http://{serverIP()}:1337/'")
    print(f"# Os arquivos são recebidos na pasta '{DOWNLOADS_FOLDER}'")
    print("# Para fechar o servidor, pressione CTRL+C ou apenas feche esta janela.")
    print("#" * 80)
    print("\n")

    # INICIA O SERVIDOR
    serve(app, host="0.0.0.0", port=1337)
