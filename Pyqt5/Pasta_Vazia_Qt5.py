import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(600, 512)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(600, 512))
        self.setMaximumSize(QtCore.QSize(999999, 999999))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.setFont(font)
        self.setAutoFillBackground(True)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.gridLayout_2.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Empty)
        self.gridLayout_2.addWidget(self.pushButton, 3, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.quit)
        self.gridLayout_2.addWidget(self.pushButton_2, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.gridLayout_2.addWidget(self.listView, 6, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Verificador de Pastas Vazias"))
        self.label.setText(_translate("self", "Este programa verifica a existencia de pastas vazias\n"
        "dentro da pasta indicada.\n O programa funciona recursivamente."))
        self.label_2.setText(_translate("self", "Caminho:"))
        self.pushButton.setText(_translate("self", "Executar"))
        self.pushButton_2.setText(_translate("self", "Fechar"))
        self.label_3.setText(_translate("self", "Preview:"))

    def Empty(self):
        self.listView.clear()
        Pasta = self.lineEdit.text()
        global Lista; Lista = []
        if Pasta == "":
            QMessageBox.about(self, "ERRO", "Nenhum caminho especificado.")
        else:
            for root, dirs, files in os.walk(Pasta):
                if len(dirs) == 0 and len(files) == 0:
                    Lista.append(root)
            self.listView.addItems(Lista)

    def quit(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Janela()
    sys.exit(app.exec_())
