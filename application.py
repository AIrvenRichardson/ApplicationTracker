from logging import config
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPalette, QColor, QIcon
import sqlite3, sys, datetime, configparser, os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Database Connection
        self.config = configparser.ConfigParser()

        if os.path.exists('cfg.ini') == False:
            self.config['DEFAULT'] = {'dbdir': ''}
            with open('cfg.ini', 'w') as configfile:
                self.config.write(configfile)

        self.config.read('cfg.ini')
        self.dir = self.config['DEFAULT']['dbdir']

        self.t0 = QtWidgets.QWidget()
        self.message = QtWidgets.QLabel("Please select database location, one will be made if there is not a database present in the directory.")
        self.fileButton = QtWidgets.QPushButton("Open Directory...")
        self.fileButton.clicked.connect(self.dirSelect)

        self.layout0 = QtWidgets.QVBoxLayout(self)
        self.layout0.addWidget(self.message)
        self.layout0.addWidget(self.fileButton)

        self.t0.setLayout(self.layout0)


        # Add Record Window
        self.t1 = QtWidgets.QWidget() # Blank widget that siomply holds a layout
        
        self.eName = QtWidgets.QLineEdit("")
        self.eTitle = QtWidgets.QLineEdit("")
        self.eURL = QtWidgets.QLineEdit("")

        self.eName.setPlaceholderText("Company Name")
        self.eTitle.setPlaceholderText("Role Title")
        self.eURL.setPlaceholderText("URL")
        
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

        self.eSearch = QtWidgets.QLineEdit("")
        self.eSearch.setPlaceholderText("Company Name to Search")
        self.sb = QtWidgets.QScrollBar()
        self.retrievedEntries = QtWidgets.QTableWidget()
        self.retrievedEntries.setVerticalScrollBar(self.sb)
        self.retrievedEntries.clicked.connect(self.selectRow)

        self.button2 = QtWidgets.QPushButton("Search")
        self.button2.clicked.connect(self.findRecord)

        self.layout2 = QtWidgets.QVBoxLayout(self)
        self.layout2.addWidget(self.eSearch)
        self.layout2.addWidget(self.button2)
        self.layout2.addWidget(self.retrievedEntries)

        self.t2.setLayout(self.layout2)

        # Update Dialog
        self.t3 = QtWidgets.QWidget()

        self.rowid = QtWidgets.QLabel("67")
        self.label = QtWidgets.QLabel("Updating Row: ")
        self.uName = QtWidgets.QLineEdit("testname")
        self.uTitle = QtWidgets.QLineEdit("testtitle")
        self.uUrl = QtWidgets.QLineEdit("testurl")
        self.uStatus = QtWidgets.QLineEdit("teststatus")

        self.updateButton = QtWidgets.QPushButton("Update Entry")
        self.updateButton.clicked.connect(self.updateRow)

        self.layout3 = QtWidgets.QGridLayout(self)
        self.layout3.addWidget(self.label, 0, 0)
        self.layout3.addWidget(self.rowid, 0, 1)
        self.layout3.addWidget(self.uName, 1, 0)
        self.layout3.addWidget(self.uTitle, 2, 0)
        self.layout3.addWidget(self.uUrl, 3, 0)
        self.layout3.addWidget(self.uStatus, 4, 0)
        self.layout3.addWidget(self.updateButton, 2, 1, 2, 1)

        self.t3.setLayout(self.layout3)

        # Main Setup
        self.setWindowTitle("ApplicationHome")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.t0, "Database")
        self.tabs.addTab(self.t1, "Add Record")
        self.tabs.addTab(self.t2, "Search/Update Records")
     
        self.mainlayout = QtWidgets.QHBoxLayout(self)
        self.mainlayout.setContentsMargins(0,0,0,0)
        self.mainlayout.addWidget(self.tabs)

        if self.dir != '':
            self.tabs.setCurrentIndex(1)
            self.con = sqlite3.connect(self.dir + "/applications.db")
            self.cur = self.con.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")
            
    
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
                         Select rowid, * FROM applications WHERE company LIKE '%{self.eSearch.text()}%'
                         """)
        
        entries = self.res.fetchall()
        if len(entries) == 0:
            return
        
        i = 0
        self.retrievedEntries.setRowCount(len(entries))
        self.retrievedEntries.setColumnCount(len(entries[0]))
        self.retrievedEntries.setHorizontalHeaderLabels(["Company", "Role", "Date", "URL", "Status", "id"])

        for entry in entries:
            name = QtWidgets.QTableWidgetItem(entry[1])
            title = QtWidgets.QTableWidgetItem(entry[2])
            date = QtWidgets.QTableWidgetItem(entry[3])
            url = QtWidgets.QTableWidgetItem(entry[4])
            status = QtWidgets.QTableWidgetItem(entry[5])
            rowid = QtWidgets.QTableWidgetItem(str(entry[0]))

            self.retrievedEntries.setItem(i, 0, name)
            self.retrievedEntries.setItem(i, 1, title)
            self.retrievedEntries.setItem(i, 2, date)
            self.retrievedEntries.setItem(i, 3, url)
            self.retrievedEntries.setItem(i, 4, status)
            self.retrievedEntries.setItem(i, 5, rowid)

            i+= 1

    @QtCore.Slot()
    def selectRow(self, index: QtCore.QModelIndex):
        row = index.row()
        
        self.rowid.setText(self.retrievedEntries.item(row,5).text())
        self.uName.setText(self.retrievedEntries.item(row,0).text())
        self.uTitle.setText(self.retrievedEntries.item(row,1).text())
        self.uUrl.setText(self.retrievedEntries.item(row,3).text())
        self.uStatus.setText(self.retrievedEntries.item(row,4).text())

        self.tabs.addTab(self.t3, "Update Entry")
        self.tabs.setCurrentIndex(self.tabs.count()-1)
    
    @QtCore.Slot()
    def updateRow(self):

        self.cur.execute (f"""
                            UPDATE applications 
                            SET company = '{self.uName.text()}', title = '{self.uTitle.text()}', url = '{self.uUrl.text()}', status = '{self.uStatus.text()}' 
                            WHERE rowid = {self.rowid.text()}
                            """)
        self.con.commit()

        self.tabs.removeTab(self.tabs.count()-1)

    def dirSelect(self):
        self.dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", "", QtWidgets.QFileDialog.Option.ShowDirsOnly)
        self.con = sqlite3.connect(self.dir + "/applications.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS applications(company text, title text, date text, url text, status text)")
        self.tabs.setCurrentIndex(1)

        self.config['DEFAULT']['dbdir'] = self.dir
        with open('cfg.ini', 'w') as configfile:
            self.config.write(configfile)

    def closeEvent(self, event):
        
        self.con.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Configure The window/widget with size and BG
    widget = MyWidget()
    widget.resize(600, 200)
    widget.setAutoFillBackground(True)
    widget.show()

    sys.exit(app.exec())