# !/usr/bin/env python

# Copyright (C) 2007 Giampaolo Rodola' <g.rodola@gmail.com>.
# Use of this source code is governed by MIT license that can be
# found in the LICENSE file.

"""
A FTP server which handles every connection in a separate thread.
Useful if your handler class contains blocking calls or your
filesystem is too slow.
"""
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('italo', 'italo', r'C:\Users\Italo\Desktop\Nova pasta (2)')
    authorizer.add_anonymous(r'C:\Users\Italo\Desktop\Nova pasta (2)')
    handler = FTPHandler
    handler.authorizer = authorizer
    ip = socket.gethostbyname(socket.gethostname())
    print("http://{0}:8080/".format(ip))
    server = ThreadedFTPServer((ip, 8080), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()