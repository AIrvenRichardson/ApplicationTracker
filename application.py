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

        # Search Window
        self.t2 = QtWidgets.QWidget()

        self.eSearch = QtWidgets.QLineEdit("Company Name Here")
        self.sb = QtWidgets.QScrollBar()
        self.retrievedEntries = QtWidgets.QTableWidget()
        self.retrievedEntries.setVerticalScrollBar(self.sb)
        
        # self.arealayout = QtWidgets.QVBoxLayout()
        # self.arealayout.setContentsMargins(0,0,0,0)
        # self.arealayout.setSpacing(0)
        
        # self.area = QtWidgets.QScrollArea()
        # self.area.setWidget(self.retrievedEntries)
        # self.area.setLayout(self.arealayout)

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
        
        entries = self.res.fetchall()
        if len(entries) == 0:
            return
        
        i = 0
        self.retrievedEntries.setRowCount(len(entries))
        self.retrievedEntries.setColumnCount(len(entries[0]))
        self.retrievedEntries.setHorizontalHeaderLabels(["Company", "Role", "Date", "URL", "Status"])

        for entry in entries:
            name = QtWidgets.QTableWidgetItem(entry[0])
            title = QtWidgets.QTableWidgetItem(entry[1])
            date = QtWidgets.QTableWidgetItem(entry[2])
            url = QtWidgets.QTableWidgetItem(entry[3])
            status = QtWidgets.QTableWidgetItem(entry[4])

            self.retrievedEntries.setItem(i, 0, name)
            self.retrievedEntries.setItem(i, 1, title)
            self.retrievedEntries.setItem(i, 2, date)
            self.retrievedEntries.setItem(i, 3, url)
            self.retrievedEntries.setItem(i, 4, status)

            i+= 1
        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Configure The window/widget with size and BG
    widget = MyWidget()
    widget.resize(600, 200)
    widget.setAutoFillBackground(True)
    widget.show()

    sys.exit(app.exec())