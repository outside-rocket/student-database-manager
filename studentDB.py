from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMainWindow, QMessageBox, QPushButton
import sys
import os
import mysql.connector
import pyperclip
import matplotlib
import json
import MySQLdb as mdb
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")

with open(os.path.expanduser('~') + "\\.studentDB\\config.json", 'r') as d:
    dat = json.load(d)
try:
    db = mdb.connect('localhost', dat['username'], dat['password'], dat['database'])
    cursor = db.cursor()
except:
    db = mdb.connect('localhost', dat['username'], dat['password'])
    cursor = db.cursor()
    cursor.execute(f"create database {dat['database']};")
    cursor.execute(f'use {dat["database"]};')
    s = ''
    for i in dat['subject']:
        s += (i + ' varchar(30)' + ', ')
    cursor.execute(f'create table names (scs int, name varchar(30));')
    cursor.execute(f'create table class_12 (scs int, name varchar(30), {s} total int, exam varchar(30));')
    for i in range(len(dat['id'])):
        cursor.execute(f'insert into names values({dat["id"][i]},"{dat["names"][i]}");')
    cursor.execute('create table exams (exam varchar(30));')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('home.ui', self)
        self.btn_1.clicked.connect(self.view_exam_screen)
        self.btn_2.clicked.connect(self.view_student_screen)
        self.btn_3.clicked.connect(self.create_entry_screen)
        self.btn_4.clicked.connect(self.edit_prev_screen)
        self.quit_btn.clicked.connect(lambda: app.closeAllWindows())

    def view_exam_screen(self):
        view_marks_scr.cb.clear()
        cursor.execute("select * from exams;")
        for i in cursor:
            view_marks_scr.cb.addItem(i[0])
        widget.setCurrentIndex(1)
        widget.setFixedHeight(600)
        widget.setFixedWidth(850)

    def view_student_screen(self):
        view_stu_scr.cb.clear()
        cursor.execute("select name from names;")
        for i in cursor:
            view_stu_scr.cb.addItem(i[0])
        widget.setCurrentIndex(2)
        widget.setFixedHeight(600)
        widget.setFixedWidth(850)

    def create_entry_screen(self):
        widget.setCurrentIndex(3)
        widget.setFixedHeight(156)
        widget.setFixedWidth(376)

    def edit_prev_screen(self):
        widget.setCurrentIndex(4)
        widget.setFixedHeight(500)
        widget.setFixedWidth(400)


class View_student(QMainWindow):
    def __init__(self):
        super(View_student, self).__init__()
        loadUi("view_stu.ui", self)
        self.scs_num = None
        self.back_btn.clicked.connect(self.home_screen)
        self.go_btn.clicked.connect(self.update_table)
        self.copy_btn.clicked.connect(self.copy_cl)

    def update_table(self):
        s = ''
        for i in dat['subject']:
            s += (i + ',')

        cursor.execute(f"select scs,exam,{s}total from class_12 where name='{self.cb.currentText()}';")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        """self.table.setRowCount(len(result))
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.table.setRowCount(len(result))"""

        self.table.setRowCount(0)
        self.table.setColumnCount(3 + len(dat['subject']))
        l = ['SCS', 'Name']
        l.extend((dat['subject']))
        l.append('Total')
        self.table.setHorizontalHeaderLabels(l)
        n = 0
        self.table.setRowCount(len(result))
        for i in result:
            for j in range(3 + len(dat['subject'])):
                print(i[0])
                self.table.setItem(n, j, QTableWidgetItem(str(i[j])))
            n += 1

        return result

    def home_screen(self):
        widget.setCurrentIndex(0)
        widget.setFixedHeight(500)
        widget.setFixedWidth(800)

    def copy_cl(self):
        c = '('
        for i in self.update_table():
            for j in i:
                c += str(j)
                c += ','
            c = c[0:len(c) - 1]
            c += ')\n('
        c = c[0:len(c) - 2]
        pyperclip.copy(c)


class Create_entry(QMainWindow):
    def __init__(self):
        super(Create_entry, self).__init__()
        loadUi("create_entry.ui", self)
        self.exam_name = None
        self.back_btn.clicked.connect(self.home_screen)
        self.continue_btn.clicked.connect(self.new_entry_screen)

    def home_screen(self):
        widget.setCurrentIndex(0)
        widget.setFixedHeight(500)
        widget.setFixedWidth(800)

    def new_entry_screen(self):
        self.exam_name = self.lineEdit.text().strip()
        if self.exam_name is None or self.exam_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Exam name cannot be empty')
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            new_entry_scr.label.setText(f"Exam: {self.exam_name}")
            new_entry_scr.table.setRowCount(0)
            new_entry_scr.table.setColumnCount(2 + len(dat['subject']))
            l = ['SCS', 'Name']
            l.extend((dat['subject']))
            new_entry_scr.table.setHorizontalHeaderLabels(l)
            cursor.execute("select scs, name from names")
            result = cursor.fetchall()
            n = 0
            new_entry_scr.table.setRowCount(len(result))
            for i in result:
                print(i[0])
                new_entry_scr.table.setItem(n, 0, QTableWidgetItem(str(i[0])))
                new_entry_scr.table.setItem(n, 1, QTableWidgetItem(i[1]))
                n += 1

            widget.setCurrentIndex(5)
            widget.setFixedHeight(500)
            widget.setFixedWidth(850)


class New_Entry(QMainWindow):
    def __init__(self):
        super(New_Entry, self).__init__()
        loadUi("new_entry.ui", self)
        self.cancelbtn.clicked.connect(self.create_entry_screen)
        self.addbtn.clicked.connect(self.add_row)
        self.delbtn.clicked.connect(self.delete_row)
        self.savebtn.clicked.connect(self.save)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def delete_row(self):
        index = self.table.currentIndex()
        deleteconfirmation = QtWidgets.QMessageBox.critical(self.parent(), "Confirm delete",
                                                            f"Do you want to delete the current row({index.row() + 1})?",
                                                            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if deleteconfirmation == QtWidgets.QMessageBox.Yes:
            self.table.removeRow(index.row())
            return
        else:
            return

    def save(self):
        print("hello0")
        em = False
        ss = False
        print("heloo1")
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                print("hello e")
                if not self.table.item(i, j):
                    em = True
                    break
            break
        print("hello2")
        for i in range(self.table.rowCount()):
            print("hello3")
            if em:
                print("hello4")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Warning")
                msg.setInformativeText('Data cannot be empty')
                msg.setWindowTitle("Warning")
                msg.exec_()
                break
            row_data = []
            for j in range(self.table.columnCount()):
                widgetitem = self.table.item(i, j)
                if widgetitem and widgetitem.text:
                    row_data.append(widgetitem.text())
                else:
                    row_data.append('None')
            print("hello5")
            s = ''
            t = 0
            for j in range(len(dat['subject'])):
                s += (row_data[2 + j] + ',')
                t += int(row_data[2 + j])
                print(t)

            cursor.execute(f"insert into class_12 values({int(row_data[0])},'{row_data[1]}'," + s + str(t) + f", '{create_entry_scr.exam_name}'" + ");")

            ss = True
        print("hello6")
        cursor.execute(f"insert into exams values('{create_entry_scr.exam_name}')")
        print("hello7")
        #cursor.reset()
        print("hello8")
        db.commit()
        print("hello9")
        if ss:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Data saved successfully!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            create_entry_scr.lineEdit.clear()
            self.create_entry_screen()

    def create_entry_screen(self):
        widget.setCurrentIndex(3)
        widget.setFixedHeight(156)
        widget.setFixedWidth(376)


class Edit_Prev(QMainWindow):
    def __init__(self):
        super(Edit_Prev, self).__init__()
        loadUi("edit_prev.ui", self)
        self.back_btn.clicked.connect(self.home_screen)
        self.continue_btn.clicked.connect(self.edit_screen)
        cursor.execute("select * from exams;")
        d = cursor.fetchall()
        self.l = []
        x = 10
        y = 10
        for i in d:
            print(i)
            r = QtWidgets.QRadioButton(i[0], self.frame)
            r.setGeometry(x, y, r.width(), r.height())
            r.setStyleSheet("QRadioButton{font : 10pt;}")
            r.adjustSize()
            y += 30
            self.l.append(r)

    def home_screen(self):
        widget.setCurrentIndex(0)
        widget.setFixedHeight(500)
        widget.setFixedWidth(800)

    def edit_screen(self):
        n = 0
        for i in self.l:
            if i.isChecked():
                self.exam_name = i.text()
                n += 1
        if n == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('Choose an exam to proceed')
            msg.setWindowTitle("Warning")
            msg.exec_()
        else:
            try:
                s = ''
                for i in dat['subject']:
                    s += (i + ',')
                cursor.execute(f"select scs, name, {s} total from class_12 where exam='{self.exam_name}';")
                result = cursor.fetchall()
                print(self.exam_name)
                '''
                edit_scr.table.setRowCount(len(result))
                for row_number, row_data in enumerate(result):
                    edit_scr.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        edit_scr.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                edit_scr.table.setRowCount(len(result))
                edit_scr.label.setText(f"Exam: {self.exam_name}")'''

                edit_scr.label.setText(f"Exam: {self.exam_name}")
                edit_scr.table.setRowCount(0)
                edit_scr.table.setColumnCount(2 + len(dat['subject']))
                l = ['SCS', 'Name']
                l.extend((dat['subject']))
                edit_scr.table.setHorizontalHeaderLabels(l)
                n = 0
                edit_scr.table.setRowCount(len(result))
                for i in result:
                    for j in range(2 + len(dat['subject'])):
                        print(i[0])
                        edit_scr.table.setItem(n, j, QTableWidgetItem(str(i[j])))
                    n += 1

                widget.setCurrentIndex(6)
                widget.setFixedHeight(500)
                widget.setFixedWidth(850)
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Warning")
                msg.setInformativeText('Something went wrong')
                msg.setWindowTitle("Warning")
                msg.exec_()


class Edit(QMainWindow):
    def __init__(self):
        super(Edit, self).__init__()
        loadUi("edit.ui", self)
        self.cancelbtn.clicked.connect(self.edit_prev_screen)
        self.addbtn.clicked.connect(self.add_row)
        self.delbtn.clicked.connect(self.delete_row)
        self.savebtn.clicked.connect(self.save)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def delete_row(self):
        index = self.table.currentIndex()
        deleteconfirmation = QtWidgets.QMessageBox.critical(self.parent(), "Confirm delete",
                                                            f"Do you want to delete the current row({index.row() + 1})?",
                                                            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if deleteconfirmation == QtWidgets.QMessageBox.Yes:
            self.table.removeRow(index.row())
            return
        else:
            return

    def save(self):
        em = False
        ss = False
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if not self.table.item(i, j):
                    em = True
                    break
                break

        for i in range(self.table.rowCount()):
            if em:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Warning")
                msg.setInformativeText('Data cannot be empty')
                msg.setWindowTitle("Warning")
                msg.exec_()
                break
            else:
                cursor.execute(f"delete from class_12 where exam='{edit_prev_scr.exam_name}'")
                _ = cursor.fetchall()
                for i in range(self.table.rowCount()):
                    row_data = []
                    for j in range(self.table.columnCount()):
                        widgetitem = self.table.item(i, j)
                        if widgetitem and widgetitem.text:
                            row_data.append(widgetitem.text())
                        else:
                            row_data.append('None')

                    s = ''
                    t = 0
                    for j in range(len(dat['subject'])):
                        s += (row_data[2 + j] + ',')
                        t += int(row_data[2 + j])
                    print("setpoint 2")
                    cursor.execute(f"insert into class_12 values({int(row_data[0])},'{row_data[1]}'," + s + str(
                        t) + f", '{edit_prev_scr.exam_name}'" + ");")
                #cursor.reset()
                db.commit()
                ss = True

        if ss:
            print("setpoint 1")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Data saved successfully!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            create_entry_scr.lineEdit.clear()
            self.edit_prev_screen()

    def edit_prev_screen(self):
        widget.setCurrentIndex(4)
        widget.setFixedHeight(500)
        widget.setFixedWidth(400)


class View_marks(QMainWindow):
    t = None

    def __init__(self):
        super(View_marks, self).__init__()
        loadUi("view_marks.ui", self)
        self.back_btn.clicked.connect(self.home_screen)
        self.go_btn.clicked.connect(self.update_table)
        self.copy_btn.clicked.connect(self.copy_cl)
        # self.show_analysis.clicked.connect(self.analysis)
        self.d = "None"
        self.t = self.cb.currentText()

    def update_table(self):
        s = ''
        for i in dat['subject']:
            s += (i + ',')
        cursor.execute(f"select scs,name,{s}total from class_12 where exam='{self.cb.currentText()}';")
        result = cursor.fetchall()
        print(result)
        self.table.setRowCount(0)
        print(len(result))

        '''for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.table.setRowCount(len(result))'''

        self.table.setColumnCount(3 + len(dat['subject']))
        l = ['SCS', 'Name']
        l.extend((dat['subject']))
        l.append('Total')
        self.table.setHorizontalHeaderLabels(l)
        n = 0
        self.table.setRowCount(len(result))
        for i in result:
            for j in range(3 + len(dat['subject'])):
                print(i[0])
                self.table.setItem(n, j, QTableWidgetItem(str(i[j])))
            n += 1

        return result

    def home_screen(self):
        widget.setCurrentIndex(0)
        widget.setFixedHeight(500)
        widget.setFixedWidth(800)

    def copy_cl(self):
        c = '('
        for i in self.update_table():
            for j in i:
                c += str(j)
                c += ','
            c = c[0:len(c) - 1]
            c += ')\n('
        c = c[0:len(c) - 2]
        pyperclip.copy(c)

    def analysis(self):
        cursor.execute(f"select scs,math,physics,chemistry,total from class_12 where exam='{self.cb.currentText()}';")
        self.d = cursor.fetchall()
        print(self.d)
        widget.setCurrentIndex(7)


"""class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)"""


"""class View_analysis(QtWidgets.QMainWindow):

    def __init__(self):
        super(View_analysis, self).__init__()
        self.title = 'Analysis'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.exam = None
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.exam = view_marks_scr.cb.currentText()
        '''        d = view_marks_scr.d
        #print(d)
        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        
        #t = [i[0] for i in d]

        sc.axes.plot([i[0] for i in d], [i[2] for i in d])'''
        '''self.setCentralWidget(sc)'''
        self.setCentralWidget(self.sc)

        bt_1 = QPushButton('Show', self)

        bt_1.clicked.connect(self.shw)
        bt = QPushButton('Close', self)
        bt.move(100, 20)
        bt.clicked.connect(self.cls)

    def cls(self):
        widget.setCurrentIndex(1)
        widget.setFixedHeight(600)
        widget.setFixedWidth(850)

    def shw(self):
        d = view_marks_scr.d

        self.sc.axes.plot([i[0] for i in d], [i[2] for i in d])

"""
"""class ViewAnalysis(QDialog):
    def __init__(self, ex):
        super().__init__()

        cursor.execute(f"select scs,name,math,physics,chemistry,total from class_12 where exam='{ex}';")
        d = cursor.fetchall()
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.setCentralWidget(sc)"""


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwin = MainWindow()
view_stu_scr = View_student()
create_entry_scr = Create_entry()
new_entry_scr = New_Entry()
edit_prev_scr = Edit_Prev()
edit_scr = Edit()
view_marks_scr = View_marks()
# analysis = View_analysis()

widget.addWidget(mainwin)  # 0
widget.addWidget(view_marks_scr)  # 1
widget.addWidget(view_stu_scr)  # 2
widget.addWidget(create_entry_scr)  # 3
widget.addWidget(edit_prev_scr)  # 4
widget.addWidget(new_entry_scr)  # 5
widget.addWidget(edit_scr)  # 6
# widget.addWidget(analysis)  # 7

widget.setFixedHeight(500)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())

except:
    pass
