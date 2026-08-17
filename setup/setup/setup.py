from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os
import json 

## saved as C:\Users\<user>\.studentDB\config.json
D = {}
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('s1.ui',self)
        self.cancel_btn.clicked.connect(self.cancel)
        self.next_btn.clicked.connect(self.s2)

    def s2(self):
        widget.setCurrentIndex(1)
    
    def cancel(self):
        quit()

class S2(QMainWindow):
    def __init__(self):
        super(S2, self).__init__()
        loadUi('s2.ui', self)
        self.back_btn.clicked.connect(self.back)
        self.next_btn.clicked.connect(self.next)
        self.cancel_btn.clicked.connect(self.cancel)

    def back(self):
        widget.setCurrentIndex(0)
    
    def next(self):
        widget.setCurrentIndex(2)
    
    def cancel(self):
        quit()

class S3(QMainWindow):
    def __init__(self):
        super(S3, self).__init__()
        loadUi('s3.ui', self)
        self.back_btn.clicked.connect(self.back)
        self.next_btn.clicked.connect(self.next)
        self.cancel_btn.clicked.connect(self.cancel)
        self.add1.clicked.connect(self.add_row1)
        self.rem1.clicked.connect(self.delete_row1)
        self.add2.clicked.connect(self.add_row2)
        self.rem2.clicked.connect(self.delete_row2)

    def back(self):
        widget.setCurrentIndex(1)
    
    def add_row1(self):
        self.table1.insertRow(self.table1.rowCount())
    
    def delete_row1(self):
        index = self.table1.currentIndex()
        self.table1.removeRow(index.row())
        return

    def add_row2(self):
        self.table2.insertRow(self.table2.rowCount())
    
    def delete_row2(self):
        index = self.table2.currentIndex()
        self.table2.removeRow(index.row())
        return
        
    def next(self):
        D['id'] = []
        D['names'] = []
        D['subject'] = []

        for i in range(self.table1.rowCount()):
            row_data1 = []
            for j in range(self.table1.columnCount()):
                widgetitem = self.table1.item(i,j)   
                if (widgetitem and widgetitem.text):
                    row_data1.append(widgetitem.text())
                else:
                    row_data1.append('None')
            D['id'].append(row_data1[0])
            D['names'].append(row_data1[1])
        for i in range(self.table2.rowCount()):
            row_data1 = []
            for j in range(self.table2.columnCount()):
                widgetitem = self.table2.item(i,j)   
                if (widgetitem and widgetitem.text):
                    row_data1.append(widgetitem.text())
                else:
                    row_data1.append('None')
            D['subject'].append(row_data1[0])

        d = QMessageBox(self)
        d.setWindowTitle("Success!")
        d.setText('The setup is successful, click "ok" to finish installations')
        d.setStandardButtons(QMessageBox.Ok)
        d.setIcon(QMessageBox.Information)
        button = d.exec()
        if button == QMessageBox.Ok:
            D['database'] = s2.l1.text().strip()
            D['username'] = s2.l2.text().strip()
            D['password'] = s2.l3.text().strip()
            if not os.path.exists(os.path.expanduser('~')+"\\.studentDB"):
                os.makedirs(os.path.expanduser('~')+"\\.studentDB")
            data = json.dumps(D, indent=4)
            with open(os.path.expanduser('~')+"\\.studentDB\\config.json", "w") as f:
                f.write(data)

            print(D)
            quit()
    
    def cancel(self):
        quit()  


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwin = MainWindow()
s2= S2()
s3=S3()


widget.addWidget(mainwin)
widget.addWidget(s2)
widget.addWidget(s3)

widget.setFixedHeight(450)
widget.setFixedWidth(700)
widget.show()

try:
    sys.exit(app.exec_())

except: 
    pass
