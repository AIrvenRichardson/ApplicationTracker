from PySide6 import QtWidgets, QtCore, QtGui
import sys, datetime

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Application Record")

        self.eName = QtWidgets.QLineEdit("Company Name")
        self.eTitle = QtWidgets.QLineEdit("Role Title")
        self.eURL = QtWidgets.QLineEdit("URL")
        self.hello = "hoi"

        self.button = QtWidgets.QPushButton("Click me!")

        
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.eName, 0, 0)
        self.layout.addWidget(self.eTitle, 1, 0)
        self.layout.addWidget(self.eURL, 2, 0)
        self.layout.addWidget(self.button, 1, 3)

        self.button.clicked.connect(self.magic)
    
    @QtCore.Slot()
    def magic(self):
        x = datetime.datetime.now()
        print(self.eName.text(), self.eTitle.text(), x.strftime("%x"), self.eURL.text())




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 200)
    widget.show()

    sys.exit(app.exec())