from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QPalette, QColor
import sqlite3
import sys, datetime

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Application Record")

        self.eName = QtWidgets.QLineEdit("Company Name")
        self.eTitle = QtWidgets.QLineEdit("Role Title")
        self.eURL = QtWidgets.QLineEdit("URL")

        self.button = QtWidgets.QPushButton("Record")

        
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.eName, 0, 0)
        self.layout.addWidget(self.eTitle, 1, 0)
        self.layout.addWidget(self.eURL, 2, 0)
        self.layout.addWidget(self.button, 1, 3)

        #Database Connection
        self.con = sqlite3.connect("applications.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")

        self.button.clicked.connect(self.addRecord)
    
    @QtCore.Slot()
    def addRecord(self):
        x = datetime.datetime.now()

        self.cur.execute(f"""
                INSERT INTO applications VALUES
                ('{self.eName.text()}', '{self.eTitle.text()}', '{x.strftime('%Y-%m-%d')}', '{self.eURL.text()}', 'not yet')
                """)
    
        self.con.commit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Configure The window/widget with size and BG
    widget = MyWidget()
    widget.resize(600, 200)
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("gray"))
    widget.setPalette(palette)
    widget.show()

    sys.exit(app.exec())