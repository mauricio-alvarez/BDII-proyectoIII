

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot
from sympy import divisors
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from source import *

class Ui_Widget(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(995, 769)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 420, 871, 311))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=MainWindow)
        self.label.setGeometry(QtCore.QRect(30, 10, 361, 291))
        self.label.setText("")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(450, 60, 281, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(parent=MainWindow)
        self.label_2.setGeometry(QtCore.QRect(450, 40, 191, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(450, 120, 71, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(parent=MainWindow)
        self.label_3.setGeometry(QtCore.QRect(450, 100, 81, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(parent=MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(750, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_dialog)
        self.pushButton_2 = QtWidgets.QPushButton(parent=MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 160, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.find_similar_images) # <--- connect the button to the function
        self.label_4 = QtWidgets.QLabel(parent=MainWindow)
        self.label_4.setGeometry(QtCore.QRect(60, 380, 291, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Widget"))
        self.label_2.setText(_translate("MainWindow", "Ruta de Imagen"))
        self.label_3.setText(_translate("MainWindow", "Top K"))
        self.pushButton.setText(_translate("MainWindow", "Buscar"))
        self.pushButton_2.setText(_translate("MainWindow", "Analizar"))
        self.label_4.setText(_translate("MainWindow", "Resultados"))

    @pyqtSlot()
    def open_dialog(self):
      fname = QtWidgets.QFileDialog.getOpenFileName(
          self,
          "Open File",
          "${HOME}",
          "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
      )
      self.lineEdit.setText(fname[0])
      self.label.setPixmap(QtGui.QPixmap(fname[0]))
      self.label.setScaledContents(True) # <--- this is what you need to scale the image

    def find_similar_images(self):
        self.clearLayout(self.gridLayout)
        vectores = loadNVectors("../faceEncodings.bin",13175)
        pathDict = loadJson("../faceEncodings_metadata.json")
        kd = Kdtree()
        kd.searchknn(vectores[2],8)
        values = kd.recoverImgs(pathDict)
        #get values from vector
        #values=["hola","hola1","hola2","hola3","hola4","hola5","hola6","hola1","hola2","hola3","hola4","hola5","hola6","hola1","hola2","hola3","hola4","hola5","hola6"]

        top_k = int(self.lineEdit_2.text())
        div = divisors(top_k)
        if len(div)%2==0:
            n = div[int(len(div)/2)]
            m = div[int(len(div)/2)-1]
        else:
            n = m = div[int(len(div)//2)]
        positions = [(i, j) for i in range(n) for j in range(m)]

        for position, path in zip(positions, values):
            temp = QtWidgets.QLabel(parent=MainWindow)
            temp.setPixmap(QtGui.QPixmap(path))
            #temp.setText(path)
            temp.setScaledContents(True)
            self.gridLayout.addWidget(temp, *position)
      
    def clearLayout(self, layout):
      while layout.count():
        child = layout.takeAt(0)
        if child.widget():
          child.widget().deleteLater()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Widget()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
