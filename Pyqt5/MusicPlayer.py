import os
import sys
import time
import pygame
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread
from mutagen.id3 import ID3
from mutagen.mp3 import MP3


class Ui_Form(QWidget):
    def setupUi(self, Form):
        self.Threadclass = SecondThread()
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.setEnabled(True)
        Form.resize(310, 510)
        Form.setMinimumSize(QtCore.QSize(310, 510))
        Form.setMaximumSize(QtCore.QSize(310, 510))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        Form.setFont(font)
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Form.setAutoFillBackground(True)
        Form.setStyle(QStyleFactory.create('Fusion'))
        Form.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QtWidgets.QToolBox(Form)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtWidgets.QFrame.Box)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.toolBox.setObjectName("toolBox")
        self.toolBoxPage1 = QtWidgets.QWidget()
        self.toolBoxPage1.setObjectName("toolBoxPage1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.toolBoxPage1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.IMAGE = QtWidgets.QLabel(self.toolBoxPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IMAGE.sizePolicy().hasHeightForWidth())
        self.IMAGE.setSizePolicy(sizePolicy)
        self.IMAGE.setMinimumSize(QtCore.QSize(250, 250))
        self.IMAGE.setMaximumSize(QtCore.QSize(250, 250))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.IMAGE.setFont(font)
        self.IMAGE.setFrameShape(QtWidgets.QFrame.Box)
        self.IMAGE.setScaledContents(True)
        self.IMAGE.setAlignment(QtCore.Qt.AlignCenter)
        self.IMAGE.setWordWrap(True)
        self.IMAGE.setObjectName("IMAGE")
        self.verticalLayout.addWidget(self.IMAGE)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.PREV_BUTTON = QtWidgets.QPushButton(self.toolBoxPage1)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.PREV_BUTTON.setFont(font)
        self.PREV_BUTTON.setDefault(False)
        self.PREV_BUTTON.setFlat(False)
        self.PREV_BUTTON.setObjectName("PREV_BUTTON")
        self.PREV_BUTTON.clicked.connect(self.prevsong)
        self.gridLayout.addWidget(self.PREV_BUTTON, 0, 0, 1, 1)
        self.PLAY_BUTTON = QtWidgets.QPushButton(self.toolBoxPage1)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.PLAY_BUTTON.setFont(font)
        self.PLAY_BUTTON.setDefault(False)
        self.PLAY_BUTTON.setFlat(False)
        self.PLAY_BUTTON.setObjectName("PLAY_BUTTON")
        self.PLAY_BUTTON.clicked.connect(self.playpause)
        self.gridLayout.addWidget(self.PLAY_BUTTON, 0, 1, 1, 1)
        self.NEXT_BUTTON = QtWidgets.QPushButton(self.toolBoxPage1)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.NEXT_BUTTON.setFont(font)
        self.NEXT_BUTTON.setDefault(False)
        self.NEXT_BUTTON.setFlat(False)
        self.NEXT_BUTTON.setObjectName("NEXT_BUTTON")
        self.NEXT_BUTTON.clicked.connect(self.nextsong)
        self.gridLayout.addWidget(self.NEXT_BUTTON, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.SONG_NAME = QtWidgets.QLabel(self.toolBoxPage1)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.SONG_NAME.setFont(font)
        self.SONG_NAME.setFrameShape(QtWidgets.QFrame.Box)
        self.SONG_NAME.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SONG_NAME.setMidLineWidth(0)
        self.SONG_NAME.setScaledContents(True)
        self.SONG_NAME.setAlignment(QtCore.Qt.AlignCenter)
        self.SONG_NAME.setWordWrap(True)
        self.SONG_NAME.setObjectName("SONG_NAME")
        self.verticalLayout.addWidget(self.SONG_NAME)
        global PROGRESS_BAR; PROGRESS_BAR = QtWidgets.QProgressBar(self.toolBoxPage1)
        PROGRESS_BAR.setProperty("value", 0)
        PROGRESS_BAR.setAlignment(QtCore.Qt.AlignCenter)
        PROGRESS_BAR.setTextVisible(False)
        PROGRESS_BAR.setOrientation(QtCore.Qt.Horizontal)
        PROGRESS_BAR.setInvertedAppearance(False)
        PROGRESS_BAR.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        PROGRESS_BAR.setObjectName("PROGRESS_BAR")
        self.verticalLayout.addWidget(PROGRESS_BAR)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.toolBox.addItem(self.toolBoxPage1, "")
        self.toolBoxPage2 = QtWidgets.QWidget()
        self.toolBoxPage2.setObjectName("toolBoxPage2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.toolBoxPage2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton = QtWidgets.QPushButton(self.toolBoxPage2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.toolButton.setFont(font)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.FolderSelect)
        self.horizontalLayout.addWidget(self.toolButton)
        spacerItem = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.toolBoxPage2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ClearPlaylist)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.SONG_LIST = QtWidgets.QListWidget(self.toolBoxPage2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.SONG_LIST.sizePolicy().hasHeightForWidth())
        global songlist;
        songlist = []
        self.SONG_LIST.setSizePolicy(sizePolicy)
        self.SONG_LIST.setObjectName("SONG_LIST")
        self.SONG_LIST.addItems(songlist)
        QtWidgets.QApplication.processEvents()
        self.verticalLayout_3.addWidget(self.SONG_LIST)
        self.toolBox.addItem(self.toolBoxPage2, "")
        self.verticalLayout_2.addWidget(self.toolBox)
        global index;
        index = 0
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        global _translate;
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FRAME"))
        self.IMAGE.setText(_translate("Form", "NO COVER"))
        self.PREV_BUTTON.setText(_translate("Form", "|<<"))
        self.PLAY_BUTTON.setText(_translate("Form", ">"))
        self.NEXT_BUTTON.setText(_translate("Form", ">>|"))
        self.SONG_NAME.setText(_translate("Form", ""))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage1), _translate("Form", "PLAYER"))
        self.toolButton.setText(_translate("Form", "..."))
        self.pushButton.setText(_translate("Form", "Clear Playlist"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage2), _translate("Form", "PLAYLIST"))


    def songinfo(self):
        global index
        try:
            audio = ID3(songlist[index])
            artist_name = audio['TPE1'].text[0]
            title = audio['TIT2'].text[0]
            ScriptFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
            IMG = open(ScriptFolder + "\\" + 'cover.jpg', 'wb')
            IMG.write(audio['APIC:Cover'].data)
            IMG.close()
            self.SONG_NAME.setText(_translate("Form", str(artist_name + " - " + title)))
            self.Cover = QPixmap(ScriptFolder + "\\" + 'cover.jpg')
            self.Cover2 = self.Cover.scaled(150, 150)
            self.IMAGE.setPixmap(self.Cover)
        except:
            self.IMAGE.setText(_translate("Form", "NO COVER"))
            self.SONG_NAME.setText(_translate("Form", str(songlist[index])))
        QtWidgets.QApplication.processEvents()

    def FolderSelect(self):
        global index
        global songlist
        MusicFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        try:
            os.chdir(MusicFolder)
            for i in os.listdir(MusicFolder):
                if i.endswith(".mp3"):
                    songlist.append(i)

            self.SONG_LIST.addItems(songlist)
            pygame.mixer.music.load(songlist[index])
            pygame.mixer.music.play()
            self.PLAY_BUTTON.setText(_translate("Form", "||"))
            self.n = 0
            self.songinfo()
            self.Threadclass.terminate()
            PROGRESS_BAR.setProperty("value", 0)
            QtWidgets.QApplication.processEvents()
            self.Threadclass.start()
            QtWidgets.QApplication.processEvents()
        except:
            pass

    def playpause(self):
        global songlist
        if songlist == []:
            self.FolderSelect()

        elif self.n == 0:
            pygame.mixer.music.pause()
            self.Threadclass.sleep()
            self.PLAY_BUTTON.setText(_translate("Form", ">"))
            QtWidgets.QApplication.processEvents()
            self.n = 1
        elif self.n == 1:
            pygame.mixer.music.unpause()
            self.Threadclass.usleep()
            self.PLAY_BUTTON.setText(_translate("Form", "||"))
            QtWidgets.QApplication.processEvents()
            self.n = 0

    def nextsong(self):
        global index
        if index < (len(songlist) - 1):
            index += 1
            try:
                pygame.mixer.music.load(songlist[index])
                pygame.mixer.music.play()
                self.PLAY_BUTTON.setText(_translate("Form", "||"))
                self.n = 0
                self.songinfo()
                self.Threadclass.terminate()
                PROGRESS_BAR.setProperty("value", 0)
                QtWidgets.QApplication.processEvents()
                self.Threadclass.start()
                QtWidgets.QApplication.processEvents()
            except:
                pass
        elif index == len(songlist):
            pass

    def prevsong(self):
        global index
        if index == 0:
            pass
        elif index == len(songlist) or index < len(songlist):
            index -= 1
            try:
                pygame.mixer.music.load(songlist[index])
                pygame.mixer.music.play()
                self.PLAY_BUTTON.setText(_translate("Form", "||"))
                self.n = 0
                self.songinfo()
                self.Threadclass.terminate()
                PROGRESS_BAR.setProperty("value", 0)
                QtWidgets.QApplication.processEvents()
                self.Threadclass.start()
                QtWidgets.QApplication.processEvents()
            except:
                pass

    def ClearPlaylist(self):
        self.SONG_LIST.clear()
        del songlist[:]
        pygame.mixer.music.stop()
        self.Threadclass.terminate()
        PROGRESS_BAR.setProperty("value", 0)
        self.IMAGE.setText(_translate("Form", "NO COVER"))
        self.SONG_NAME.setText(_translate("Form", ""))
        QtWidgets.QApplication.processEvents()

class SecondThread(QtCore.QThread):

    def __init__(self):
        super(SecondThread, self).__init__()

    def run(self):
        PROGRESS_BAR.setProperty("value", 0)
        QtWidgets.QApplication.processEvents()
        arquivomp3 = MP3(songlist[index])
        MP3Time = arquivomp3.info.length
        MP3Time100 = MP3Time / 100
        barvalue = 0
        for i in range(1, 101):
            if barvalue == 100:
                PROGRESS_BAR.setProperty("value", barvalue)
                time.sleep(1)
                Ui_Form.nextsong(Ui_Form())
            else:
                PROGRESS_BAR.setProperty("value", barvalue)
                QtWidgets.QApplication.processEvents()
                barvalue += 1
                print(barvalue)
                time.sleep(MP3Time100)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    try:
        pygame.mixer.init()
    except:
        QMessageBox.about(QWidget(), "ERRO", "Nenhum dispositivo de audio encontrado.")
        sys.exit()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
