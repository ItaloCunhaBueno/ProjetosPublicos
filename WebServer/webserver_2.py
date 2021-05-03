import os
from http.server import SimpleHTTPRequestHandler
import socket
import PySimpleGUIQt as sg
from concurrent.futures import ThreadPoolExecutor
from  threading import enumerate
import ctypes
import webbrowser
import base64
import socketserver

class SimpleHTTPAuthHandler(SimpleHTTPRequestHandler):
    """Main class to present webpages and authentication."""
    username = ''
    password = ''

    def __init__(self, request, client_address, server):
        key = '{}:{}'.format(self.username, self.password).encode('ascii')
        self.key = base64.b64encode(key)
        self.valid_header = b'Basic ' + self.key
        super().__init__(request, client_address, server)

    def do_HEAD(self):
        """head method"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_authhead(self):
        """do authentication"""
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Test\"")
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Present frontpage with user authentication."""
        auth_header = self.headers.get('Authorization', '').encode('ascii')
        if auth_header is None:
            self.do_authhead()
            self.wfile.write(b"no auth header received")
        elif auth_header == self.valid_header:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_authhead()
            self.wfile.write(auth_header)
            self.wfile.write(b"not authenticated")


def serve_http(ip="", port=80, start_dir=None, handler_class=SimpleHTTPAuthHandler):
    """setting up server"""
    httpd = socketserver.TCPServer((ip, port), handler_class)

    if start_dir:
        os.chdir(start_dir)

    httpd.serve_forever()

def serverstart(dir, ip, port, username, password):
    """
    Start http server with basic authentication current directory.
    """
    SimpleHTTPAuthHandler.username = username
    SimpleHTTPAuthHandler.password = password
    serve_http(ip=ip, port=port, start_dir=dir, handler_class=SimpleHTTPAuthHandler)

sg.theme("Reddit")
sg.SetOptions(button_color=("000000", "000000"), button_element_size=(8, 0.9), auto_size_buttons=True, auto_size_text=True)

Layout = [[sg.T("ONLINE FILE SHARING SYSTEM", font="Arial 12 bold", justification="center")],
          [sg.T()],
          [sg.CBox("REQUEST AUTHENTICATION", key='auth', enable_events=True)],
          [sg.T(' USER:', text_color="grey", key='text_user'), sg.I(key='user', size=(10, 0.9), disabled=True), sg.T(""), sg.T(""), sg.T(""), sg.T(""), sg.T("")],
          [sg.T(' PASSWORD:', text_color="grey", key='text_pass'), sg.I(key='pass', size=(10, 0.9), disabled=True), sg.T(""), sg.T(""), sg.T(""), sg.T(""), sg.T("")],
          [sg.T(" FOLDER:    "), sg.I(key="pasta", size=(46, 0.9)), sg.FolderBrowse("BROWSE", size=(10, 0.95))],
          [sg.T(size=(20,1)), sg.B("RUN", size=(8, 0.9)), sg.B("STOP", disabled=True, size=(8, 0.9)), sg.B("EXIT", size=(8, 0.9))],
          [sg.Output(background_color="Black", text_color="White")]]

window = sg.Window('File Sharing System', resizable=False, size=(600, 300)).layout(Layout)

def terminate_thread(thread):
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def run(pasta, user, password):
    ip = "localhost"
    porta = 8080
    os.chdir(pasta)
    files = os.listdir(pasta)
    folderlist = []
    filelist = []
    for file in files:
        if os.path.isfile(file):
            filelist.append(file)
        else:
            folderlist.append(file)
    folderlist = sorted(folderlist)
    filelist = sorted(filelist)
    files = folderlist + filelist
    global index_generated
    if not "index.html" in files:
        index_generated = True
        with open("index.html", "w+") as index:
            index.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n')
            index.write('<html><head>\n')
            index.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
            index.write('<title>File List</title>\n')
            index.write('</head>\n')
            index.write('<style>\n')
            index.write('body {background-color:#00ffec;\n')
            index.write('color:#002c33}\n')
            index.write('table, th, td {\n')
            index.write('  border: 1px solid #00e5d4;\n')
            index.write('  border-collapse: collapse;\n')
            index.write('  padding: 2px;\n')
            index.write('  margin-left: auto;\n')
            index.write('  margin-right: auto;\n')
            index.write('}\n')
            index.write('</style>\n')
            index.write('<body>\n')
            index.write('<h1></h1>\n')
            index.write('<table>\n')
            index.write('	<tr align="center"; style="background-color:#ff9a00">\n')
            index.write('		<th>File</th>\n')
            index.write('		<th>Type</th>\n')
            index.write('		<th>Size</th>\n')
            index.write('	</tr>\n')
            for file in files:
                if os.path.isfile(file):
                    size = round((os.stat(file).st_size / 1024), 3)
                    filetype = os.path.splitext(file)[1].upper()
                    index.write('<tr><td><a href="{0}">{0}</a></td><td>{1}</td><td>{2} Kb</td>\n'.format(file, filetype, size))
                else:
                    filetype = "FOLDER"
                    index.write('<tr><td><a href="{0}">{0}</a></td><td>{1}</td><td>.</td>\n'.format(file, filetype))
            index.write('<hr>\n')
            index.write('</body></html>\n')
    else:
        index_generated = False
    print("========================")
    print("Serving HTTP on: http://{0}:{1}/".format(ip, porta))
    print("STATUS: RUNNING...")
    webbrowser.open('http://{0}:{1}'.format(ip, porta), new=0, autoraise=True)
    window["STOP"].Update(disabled=False)
    window["RUN"].Update(disabled=True)
    window.Refresh()
    serverstart(pasta, ip, porta, user, password)



def kill():
    ThreadPoolExecutor().shutdown(wait=False)
    if len(enumerate()) > 1:
        for t in enumerate()[1:]:
            terminate_thread(t)
        if index_generated is True:
            if os.path.isfile("index.html"):
                os.remove("index.html")
        print("========================")
        print("STATUS: STOPPED")
        window["STOP"].Update(disabled=True)
        window["RUN"].Update(disabled=False)
    window.Refresh()

while True:
    event, values = window.read()
    if event in [sg.WIN_CLOSED, 'EXIT']:
        kill()
        break
    if event == "RUN":
        pasta = window["pasta"].Get()
        Username = window["user"].Get()
        Password = window["pass"].Get()
        reqaut = window['auth'].Get()
        if os.path.isdir(pasta):
            if reqaut:
                ThreadPoolExecutor().submit(run, pasta, Username, Password)
            else:
                ThreadPoolExecutor().submit(run, pasta, "", "")
        else:
            sg.PopupOK("ERROR: No folder selected or folder does not exist.", non_blocking=False, keep_on_top=True)

    if event == "STOP":
        kill()

    if event == "auth":
        reqaut = window['auth'].Get()
        if reqaut is True:
            window['text_user'].Update(text_color="black")
            window['text_pass'].Update(text_color="black")
            window['user'].Update(disabled=False)
            window['pass'].Update(disabled=False)
            window.Refresh()
        else:
            window['text_user'].Update(text_color="grey")
            window['text_pass'].Update(text_color="grey")
            window['user'].Update(disabled=True)
            window['pass'].Update(disabled=True)
            window.Refresh()

window.close()