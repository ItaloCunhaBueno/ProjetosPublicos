import glob
import os
import sys
import time
import urllib

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from core import spotify_tools
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TORY, TYER, TPUB, APIC, USLT, COMM
from mutagen.mp3 import MP3


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'MP3 Tagger'
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(365, 425)
        self.setMinimumSize(QtCore.QSize(365, 425))
        self.setMaximumSize(QtCore.QSize(365, 425))
        self.centralwidget = QtWidgets.QWidget(self)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 200, 341, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.GenericCover = QPixmap('cover.png')  # O arquivo precisa estar na mesma pasta do script
        self.GenericCover2 = self.GenericCover.scaled(141, 141)
        self.graphicsView = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setPixmap(self.GenericCover2)
        self.graphicsView.setGeometry(QtCore.QRect(10, 230, 141, 141))
        self.graphicsView.setObjectName("graphicsView")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 380, 341, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 341, 141))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9, 0, QtCore.Qt.AlignBottom)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 160, 341, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.MP3Tagger)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.widget1)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.quit)
        self.horizontalLayout.addWidget(self.pushButton)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(160, 230, 41, 141))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.widget2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(210, 230, 141, 141))
        self.widget3.setObjectName("widget3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.widget3)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.widget3)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.widget3)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        global _translate;
        _translate = QtCore.QCoreApplication.translate
        self.label_10.setText(_translate("MainWindow", ""))
        self.label.setText(
            _translate("MainWindow", "Esta ferramenta aplica tags em arquivos mp3 baseado em informações\n"
                                     "retiradas do banco de dados do Spotify."))
        self.label_2.setText(_translate("MainWindow", "ATENÇÃO: Os arquivos devem estar na mesma pasta, nomeados no\n"
                                                      "formato 'MUSICA - ARTISTA'.\n"
                                                      "Caso haja números no nome do arquivo, os mesmos serão removidos."))
        self.label_9.setText(_translate("MainWindow", "Caminho:"))
        self.pushButton_2.setText(_translate("MainWindow", "Executar"))
        self.pushButton.setText(_translate("MainWindow", "Sair"))
        self.label_4.setText(_translate("MainWindow", "Artista:"))
        self.label_3.setText(_translate("MainWindow", "Música:"))
        self.label_5.setText(_translate("MainWindow", "Album:"))
        self.label_6.setText(_translate("MainWindow", ""))
        self.label_7.setText(_translate("MainWindow", ""))
        self.label_8.setText(_translate("MainWindow", ""))

    def quit(self):
        sys.exit()

    def MP3Tagger(self):
        Caminho = self.lineEdit.text()
        if Caminho == "":
            QMessageBox.about(self, "ERRO", "Nenhum caminho especificado.")
        else:
            File = glob.glob(Caminho + "/*.mp3")
            for i in File:  # Caminho completo do arquivo com extensão
                self.label_10.setText(_translate("MainWindow", ""))
                QtWidgets.QApplication.processEvents()
                Path = os.path.dirname(i)  # Caninho completo da pasta do arquivo
                Name1 = os.path.basename(i)  # Nome do arquivo completo com extensão
                Name2 = os.path.splitext(Name1)  # Nome do arquivo dividido na extensão
                Name3 = Name2[0].split(" - ")  # Nome do arquivo divido no artista e musica
                Name4 = ''.join(i for i in Name3[0] if not i.isdigit())  # Nome da música sem os números
                print("Caminho: " + i)
                print("Name1: " + str(Name1))
                print("Name2: " + str(Name2))
                print("Name3: " + str(Name3))
                print("Name4: " + str(Name4))
                self.label_10.setText(_translate("MainWindow", "Renomeando arquivo..."))
                QtWidgets.QApplication.processEvents()
                os.rename(i, Path + "\\" + Name3[1] + " -" + Name4 + ".mp3")  # Renomeia o arquivo
                self.label_10.setText(_translate("MainWindow", "Buscando metadados no banco de dados do Spotify..."))
                QtWidgets.QApplication.processEvents()
                meta_tags = spotify_tools.generate_metadata(Name3[1] + " -" + Name4)  # Gera as tags do mp3
                if meta_tags == None:
                    continue
                else:
                    self.label_6.setText(_translate("MainWindow", str(meta_tags['artists'][0]['name'])))
                    self.label_7.setText(_translate("MainWindow", str(meta_tags['name'])))
                    self.label_8.setText(_translate("MainWindow", str(meta_tags['album']['name'])))
                    self.label_10.setText(_translate("MainWindow", "Aplicando tags..."))
                    ScriptFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
                    IMG = open(ScriptFolder + "\\" + 'cover2.jpg', 'wb')
                    IMG.write(urllib.request.urlopen(meta_tags['album']['images'][0]['url']).read())
                    IMG.close()
                    time.sleep(1)
                    self.GenericCover3 = QPixmap('cover2.jpg')
                    self.GenericCover4 = self.GenericCover3.scaled(141, 141)
                    self.graphicsView.setPixmap(self.GenericCover4)
                    QtWidgets.QApplication.processEvents()
                    audiofile = MP3(Path + "\\" + Name3[1] + " -" + Name4 + ".mp3")
                    audiofile.tags = None  # Exclui qualquer tag antes de aplicar as novas (previne erro)
                    audiofile.add_tags(ID3=EasyID3)
                    audiofile['artist'] = meta_tags['artists'][0]['name']
                    audiofile['albumartist'] = meta_tags['artists'][0]['name']
                    audiofile['album'] = meta_tags['album']['name']
                    audiofile['title'] = meta_tags['name']
                    audiofile['tracknumber'] = [meta_tags['track_number'],
                                                meta_tags['total_tracks']]
                    audiofile['discnumber'] = [meta_tags['disc_number'], 0]
                    audiofile['date'] = meta_tags['release_date']
                    audiofile['originaldate'] = meta_tags['release_date']
                    audiofile['media'] = meta_tags['type']
                    audiofile['author'] = meta_tags['artists'][0]['name']
                    audiofile['lyricist'] = meta_tags['artists'][0]['name']
                    audiofile['arranger'] = meta_tags['artists'][0]['name']
                    audiofile['performer'] = meta_tags['artists'][0]['name']
                    audiofile['website'] = meta_tags['external_urls']['spotify']
                    audiofile['length'] = str(meta_tags['duration_ms'] / 1000.0)
                    if meta_tags['publisher']:
                        audiofile['encodedby'] = meta_tags['publisher']
                    if meta_tags['genre']:
                        audiofile['genre'] = meta_tags['genre']
                    if meta_tags['copyright']:
                        audiofile['copyright'] = meta_tags['copyright']
                    if meta_tags['external_ids']['isrc']:
                        audiofile['isrc'] = meta_tags['external_ids']['isrc']
                    audiofile.save(v2_version=3)

                    # For supported id3 tags:
                    # https://github.com/quodlibet/mutagen/blob/master/mutagen/id3/_frames.py
                    # Each class represents an id3 tag
                    audiofile = ID3(Path + "\\" + Name3[1] + " -" + Name4 + ".mp3")
                    year, *_ = meta_tags['release_date'].split('-')
                    audiofile['TORY'] = TORY(encoding=3, text=year)
                    audiofile['TYER'] = TYER(encoding=3, text=year)
                    audiofile['TPUB'] = TPUB(encoding=3, text=meta_tags['publisher'])
                    audiofile['COMM'] = COMM(encoding=3, text=meta_tags['external_urls']['spotify'])
                    if meta_tags['lyrics']:
                        audiofile['USLT'] = USLT(encoding=3, desc=u'Lyrics', text=meta_tags['lyrics'])
                    try:
                        albumart = urllib.request.urlopen(meta_tags['album']['images'][0]['url'])
                        audiofile['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3,
                                                 desc=u'Cover', data=albumart.read())
                        albumart.close()
                    except IndexError:
                        pass
                    audiofile.save(v2_version=3)
                    self.label_10.setText(_translate("MainWindow", "Concluído."))
                    QtWidgets.QApplication.processEvents()
                    time.sleep(2)  # pausa dramática
                    # Some com os textos:
                    self.label_10.setText(_translate("MainWindow", ""))
                    QtWidgets.QApplication.processEvents()
            QMessageBox.about(self, "Concluído", "Operação concluída.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
