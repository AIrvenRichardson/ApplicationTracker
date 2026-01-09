from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QPalette, QColor
import sqlite3
import sys, datetime

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Database Connection
        self.con = sqlite3.connect("applications.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")


        # Add Record Window
        self.t1 = QtWidgets.QWidget() # Blank widget that siomply holds a layout
        
        self.eName = QtWidgets.QLineEdit("Company Name")
        self.eTitle = QtWidgets.QLineEdit("Role Title")
        self.eURL = QtWidgets.QLineEdit("URL")
        
        self.button1 = QtWidgets.QPushButton("Record")
        self.button1.clicked.connect(self.addRecord)
 
        self.layout1 = QtWidgets.QGridLayout(self)
        self.layout1.addWidget(self.eName, 0, 0)
        self.layout1.addWidget(self.eTitle, 1, 0)
        self.layout1.addWidget(self.eURL, 2, 0)
        self.layout1.addWidget(self.button1, 1, 3)

        self.t1.setLayout(self.layout1)

        # Update Window
        self.t2 = QtWidgets.QWidget()

        self.eSearch = QtWidgets.QLineEdit("Company Name Here")
        self.retrievedEntries = QtWidgets.QLabel("None", alignment=QtCore.Qt.AlignCenter)
        
        self.button2 = QtWidgets.QPushButton("Search")
        self.button2.clicked.connect(self.findRecord)

        self.layout2 = QtWidgets.QVBoxLayout(self)
        self.layout2.addWidget(self.eSearch)
        self.layout2.addWidget(self.button2)
        self.layout2.addWidget(self.retrievedEntries)

        self.t2.setLayout(self.layout2)

        # Main Setup
        self.setWindowTitle("ApplicationHome")
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.t1, "Add Record")
        self.tabs.addTab(self.t2, "Update Record")
     
        self.mainlayout = QtWidgets.QHBoxLayout(self)
        self.mainlayout.setContentsMargins(0,0,0,0)
        self.mainlayout.addWidget(self.tabs)
        self.tabs.show()

    
    @QtCore.Slot()
    def addRecord(self):
        x = datetime.datetime.now()

        self.cur.execute(f"""
                INSERT INTO applications VALUES
                ('{self.eName.text()}', '{self.eTitle.text()}', '{x.strftime('%Y-%m-%d')}', '{self.eURL.text()}', 'Not Yet')
                """)
    
        # Clear out the boxes so you know it's gone through
        self.eName.setText('')
        self.eTitle.setText('')
        self.eURL.setText('')
        self.con.commit()
    
    @QtCore.Slot()
    def findRecord(self):
        self.res = self.cur.execute(f"""
                         Select * FROM applications WHERE company LIKE '%{self.eSearch.text()}%'
                         """)
        self.retrievedEntries.setText(str(self.res.fetchone()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Configure The window/widget with size and BG
    widget = MyWidget()
    widget.resize(600, 200)
    widget.setAutoFillBackground(True)
    widget.show()

    sys.exit(app.exec())