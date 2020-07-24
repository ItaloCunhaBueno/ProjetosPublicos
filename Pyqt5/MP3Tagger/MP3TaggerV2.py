import glob
import os
import time
import urllib

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QStyleFactory
from core import spotify_tools
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TORY, TYER, TPUB, APIC, USLT, COMM
from mutagen.mp3 import MP3


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(670, 500)
        Frame.setBackgroundRole(QtGui.QPalette.Light)
        Frame.setAutoFillBackground(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setMinimumSize(QtCore.QSize(670, 500))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        Frame.setFont(font)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_2 = QtWidgets.QGridLayout(Frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Artista = QtWidgets.QLabel(Frame)
        self.Artista.setScaledContents(False)
        self.Artista.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.Artista.setWordWrap(True)
        self.Artista.setObjectName("Artista")
        self.Artista.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Artista, 16, 3, 1, 1)
        self.Musica = QtWidgets.QLabel(Frame)
        self.Musica.setScaledContents(False)
        self.Musica.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.Musica.setWordWrap(True)
        self.Musica.setObjectName("Musica")
        self.Musica.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Musica, 15, 3, 1, 1)
        self.Song_Musica = QtWidgets.QLabel(Frame)
        self.Song_Musica.setScaledContents(False)
        self.Song_Musica.setWordWrap(True)
        self.Song_Musica.setObjectName("Song_Musica")
        self.Song_Musica.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Song_Musica, 15, 4, 1, 3)
        self.Descri = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Descri.sizePolicy().hasHeightForWidth())
        self.Descri.setSizePolicy(sizePolicy)
        self.Descri.setScaledContents(False)
        self.Descri.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.Descri.setWordWrap(True)
        self.Descri.setObjectName("Descri")
        self.gridLayout_2.addWidget(self.Descri, 0, 0, 1, 7)
        self.lineEdit = QtWidgets.QLineEdit(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setToolTip("")
        self.lineEdit.setStatusTip("")
        self.lineEdit.setWhatsThis("")
        self.lineEdit.setAccessibleName("")
        self.lineEdit.setAccessibleDescription("")
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 6, 0, 1, 7)
        self.Descri_2 = QtWidgets.QLabel(Frame)
        self.Descri_2.setScaledContents(False)
        self.Descri_2.setWordWrap(True)
        self.Descri_2.setObjectName("Descri_2")
        self.Descri_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout_2.addWidget(self.Descri_2, 1, 0, 1, 7)
        self.Song_Artista = QtWidgets.QLabel(Frame)
        self.Song_Artista.setScaledContents(False)
        self.Song_Artista.setWordWrap(True)
        self.Song_Artista.setObjectName("Song_Artista")
        self.Song_Artista.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Song_Artista, 16, 4, 1, 3)
        self.Song_Album = QtWidgets.QLabel(Frame)
        self.Song_Album.setScaledContents(False)
        self.Song_Album.setWordWrap(True)
        self.Song_Album.setObjectName("Song_Album")
        self.Song_Album.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Song_Album, 17, 4, 1, 3)
        self.Album = QtWidgets.QLabel(Frame)
        self.Album.setScaledContents(False)
        self.Album.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.Album.setWordWrap(True)
        self.Album.setObjectName("Album")
        self.Album.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout_2.addWidget(self.Album, 17, 3, 1, 1)
        self.Descri_Caminho = QtWidgets.QLabel(Frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Descri_Caminho.setFont(font)
        self.Descri_Caminho.setTextFormat(QtCore.Qt.AutoText)
        self.Descri_Caminho.setScaledContents(False)
        self.Descri_Caminho.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.Descri_Caminho.setWordWrap(True)
        self.Descri_Caminho.setObjectName("Descri_Caminho")
        self.gridLayout_2.addWidget(self.Descri_Caminho, 3, 0, 1, 7)
        self.Linha = QtWidgets.QFrame(Frame)
        self.Linha.setFrameShape(QtWidgets.QFrame.HLine)
        self.Linha.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Linha.setObjectName("Linha")
        self.gridLayout_2.addWidget(self.Linha, 9, 0, 1, 7)
        self.Info = QtWidgets.QLabel(Frame)
        self.Info.setAlignment(QtCore.Qt.AlignCenter)
        self.Info.setObjectName("Info")
        self.gridLayout_2.addWidget(self.Info, 19, 0, 1, 7)
        self.GenericCover = QPixmap('cover.png')  # O arquivo precisa estar na mesma pasta do script
        self.GenericCover2 = self.GenericCover.scaled(250, 250)
        self.IMAGEM = QtWidgets.QLabel(Frame)
        self.IMAGEM.setPixmap(self.GenericCover2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IMAGEM.sizePolicy().hasHeightForWidth())
        self.IMAGEM.setSizePolicy(sizePolicy)
        self.IMAGEM.setSizeIncrement(QtCore.QSize(1, 1))
        self.IMAGEM.setBaseSize(QtCore.QSize(1, 1))
        self.IMAGEM.setScaledContents(False)
        self.IMAGEM.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.IMAGEM.setWordWrap(True)
        self.IMAGEM.setObjectName("IMAGEM")
        self.gridLayout_2.addWidget(self.IMAGEM, 15, 0, 3, 3)
        self.But_Exec = QtWidgets.QPushButton(Frame)
        self.But_Exec.setObjectName("But_Exec")
        self.But_Exec.clicked.connect(self.MP3Tagger)
        self.gridLayout_2.addWidget(self.But_Exec, 8, 0, 1, 3)
        self.But_Sair = QtWidgets.QPushButton(Frame)
        self.But_Sair.setObjectName("But_Sair")
        self.But_Sair.clicked.connect(self.quit)
        self.gridLayout_2.addWidget(self.But_Sair, 8, 4, 1, 3)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        global _translate;
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "MP3Tagger"))
        self.Artista.setText(_translate("Frame", "Artista:"))
        self.Musica.setText(_translate("Frame", "Música:"))
        self.Song_Musica.setText(_translate("Frame", ""))
        self.Descri.setText(_translate("Frame",
                                       "Esta ferramenta aplica tags em arquivos mp3 baseado em informações retiradas do banco de dados do Spotify."))
        self.Descri_2.setText(_translate("Frame",
                                         "ATENÇÃO: Os arquivos devem estar na mesma pasta, nomeados no formato \'MUSICA - ARTISTA\'. Caso haja números no nome do arquivo, os mesmos serão removidos."))
        self.Song_Artista.setText(_translate("Frame", ""))
        self.Song_Album.setText(_translate("Frame", ""))
        self.Album.setText(_translate("Frame", "Album:"))
        self.Descri_Caminho.setText(_translate("Frame", "Caminho:"))
        self.Info.setText(_translate("Frame", ""))
        self.But_Exec.setText(_translate("Frame", "Executar"))
        self.But_Sair.setText(_translate("Frame", "Sair"))

    def quit(self):
        sys.exit()

    def MP3Tagger(self):
        Caminho = self.lineEdit.text()
        if Caminho == "":
            QMessageBox.about(self, "ERRO", "Nenhum caminho especificado.")
        else:
            File = glob.glob(Caminho + "/*.mp3")
            for i in File:  # Caminho completo do arquivo com extensão
                self.Info.setText(_translate("MainWindow", ""))
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
                self.Info.setText(_translate("MainWindow", "Renomeando arquivo..."))
                QtWidgets.QApplication.processEvents()
                os.rename(i, Path + "\\" + Name2[0] + ".mp3")  # Renomeia o arquivo
                self.Info.setText(_translate("MainWindow", "Buscando metadados no banco de dados do Spotify..."))
                QtWidgets.QApplication.processEvents()
                meta_tags = spotify_tools.generate_metadata(Name2[0])  # Gera as tags do mp3
                if meta_tags == None:
                    continue
                else:
                    self.Song_Artista.setText(_translate("MainWindow", str(meta_tags['artists'][0]['name'])))
                    self.Song_Musica.setText(_translate("MainWindow", str(meta_tags['name'])))
                    self.Song_Album.setText(_translate("MainWindow", str(meta_tags['album']['name'])))
                    self.Info.setText(_translate("MainWindow", "Aplicando tags..."))
                    ScriptFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
                    IMG = open(ScriptFolder + "\\" + 'cover2.jpg', 'wb')
                    IMG.write(urllib.request.urlopen(meta_tags['album']['images'][0]['url']).read())
                    IMG.close()
                    time.sleep(1)
                    self.GenericCover3 = QPixmap('cover2.jpg')
                    self.GenericCover4 = self.GenericCover3.scaled(250, 250)
                    self.IMAGEM.setPixmap(self.GenericCover4)
                    QtWidgets.QApplication.processEvents()
                    audiofile = MP3(Path + "\\" + Name2[0] + ".mp3")
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
                    audiofile = ID3(Path + "\\" + Name2[0] + ".mp3")
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
                    self.Info.setText(_translate("MainWindow", "Concluído."))
                    QtWidgets.QApplication.processEvents()
                    time.sleep(2)  # pausa dramática
                    # Some com os textos:
                    self.Info.setText(_translate("MainWindow", ""))
                    QtWidgets.QApplication.processEvents()
            QMessageBox.about(QWidget(), "Concluído", "Operação concluída.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
