import webview
import sys
from os import chdir, path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def startserver():
    if getattr(sys, 'frozen', False):
        RUNPATH = path.dirname(sys.executable)
    elif __file__:
        RUNPATH = path.dirname(__file__)
    chdir(RUNPATH)
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

Thread1 = threading.Thread(target=startserver)
Thread1.daemon = True
Thread1.start()
webview.create_window('WEBMAP', 'http://localhost:8000')
webview.start(http_server=True, gui="cef")




