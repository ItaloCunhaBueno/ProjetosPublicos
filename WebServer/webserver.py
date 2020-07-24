import os
from http.server import HTTPServer, CGIHTTPRequestHandler
import socket
import PySimpleGUIQt as sg
from concurrent.futures import ThreadPoolExecutor
from  threading import enumerate
import ctypes
import webbrowser

sg.theme("Reddit")
sg.SetOptions(button_color=("000000", "000000"), button_element_size=(8, 0.9), auto_size_buttons=True, auto_size_text=True)

Layout = [[sg.T("ONLINE FILE SHARING SYSTEM", font="Arial 12 bold", justification="center")],
          [sg.T()],
          [sg.T("FOLDER:", size=(7, 1), justification="center"), sg.I(key="pasta", size=(46, 0.9)), sg.FolderBrowse("BROWSE", size=(10, 0.95))],
          [sg.T(size=(20,1)), sg.B("RUN", size=(8, 0.9)), sg.B("STOP", disabled=True, size=(8, 0.9)), sg.B("EXIT", size=(8, 0.9))],
          [sg.Output(background_color="Black", text_color="White")]]

window = sg.Window('File Sharing System', resizable=False, size=(600, 300)).layout(Layout)

def terminate_thread(thread):
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def run(pasta):
    ip = socket.gethostbyname(socket.gethostname())
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
            index.write('table, th, td {\n')
            index.write('  border: 1px solid black;\n')
            index.write('  border-collapse: collapse;\n')
            index.write('  padding: 2px;\n')
            index.write('  text-align: left;\n')
            index.write('  margin-left: auto;\n')
            index.write('  margin-right: auto;\n')
            index.write('}\n')
            index.write('</style>\n')
            index.write('<body>\n')
            index.write('<h1>File list:</h1>\n')
            index.write('<table>\n')
            index.write('	<tr>\n')
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
    server_object = HTTPServer(server_address=(ip, porta), RequestHandlerClass=CGIHTTPRequestHandler)
    print("========================")
    print("Serving HTTP on: http://{0}:{1}/".format(ip, porta))
    print("STATUS: RUNNING...")
    webbrowser.open('http://{0}:{1}'.format(ip, porta), new=0, autoraise=True)
    window["STOP"].Update(disabled=False)
    window["RUN"].Update(disabled=True)
    window.Refresh()
    server_object.serve_forever()


def kill():
    ThreadPoolExecutor().shutdown(wait=False)
    if len(enumerate()) > 1:
        for t in enumerate()[1:]:
            terminate_thread(t)
        if index_generated is True:
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
        if os.path.isdir(pasta):
            ThreadPoolExecutor().submit(run, pasta)
        else:
            sg.PopupOK("ERROR: No folder selected or folder does not exist.", non_blocking=False, keep_on_top=True)

    if event == "STOP":
        kill()

window.close()