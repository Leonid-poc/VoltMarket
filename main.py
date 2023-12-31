import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
import tabulate
import pyperclip

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.getTable)
        self.pushButton_2.clicked.connect(self.results)
        self.headers = ['Дата', 'Номер договора', 'УПД', 'Сумма документа', 'Неоплаченная часть', 'Дата оплаты по договору']
        pass
    
    def getTableText(self, x, y):
        text = self.tableWidget.item(y, x)
        if text == None: return ''
        return text.text()
    
    def results(self):
        col3 = 0
        col4 = 0
        for i in range(self.tableWidget.rowCount()):
            col3 += float(self.getTableText(3, i).replace(',', '.') if self.getTableText(3, i) else 0)
            col4 += float(self.getTableText(4, i).replace(',', '.') if self.getTableText(4, i) else 0)
        self.doubleSpinBox.setValue(col3)
        self.doubleSpinBox_2.setValue(col4)
        return col3, col4

    def triads(self, temp):
        temp = str(temp).replace('.', ',')
        a, rub, kop = '', '', ''
        count = 0
        if ',' in temp:
            rub, kop = temp.split(',')
        else:
            rub = temp
        for i in rub[::-1]:
            a += i
            count += 1
            if not count % 3: a += ' '
        return a[::-1] +( ',' if kop else '') + kop

    def getTable(self):
        array: list[list] = [[]]
        for y in range(self.tableWidget.rowCount()):
            for x in range(self.tableWidget.columnCount()):
                temp: str = self.getTableText(x, y)
                if not temp:
                    array[y].append('')
                    continue
                if x in (0, 5):
                    if temp.isdigit():
                        a = ''
                        for ind, elem in enumerate(temp):
                            a += elem
                            if ind in (1, 3): a += '.'
                        temp = a
                elif x in (3, 4):
                    temp = self.triads(temp)

                array[y].append(temp)
            array.append([])
        array = list(filter(any, array))
        array.insert(0, self.headers)
        align = ['center', 'center', 'center', 'right', 'right', 'center']

        columns = self.results()
        # res = tabulate.tabulate(array, tablefmt='html', headers='firstrow', numalign='center') # grid presto
        res = f"""
Уважаемый клиент! <br>
Ознакомьтесь с информацией о задолженности {self.lineEdit.text()} перед ООО "Вольтмаркет" <br>
<br>
<table border style="font-family: Times New Roman">
<thead>
"""
        for row in range(len(array)):
            res += "<tr>"
            for column in range(len(self.headers)):
                res += f'''
<t{"d" if row else "h"} style="text-align: {align[column]}{"; padding: 0px 20px" if column in (0, 1) else ""}" >{array[row][column]}</t{"d" if row else "h"}>
'''
            res += "</tr>"
            if row == 0:
                res += """
</thead>
<tbody>
"""
        res += f'''
</tbody>
</table>
<hr>
Итого <br>
Сумма Документа: {self.triads(columns[0])} рублей. <br>
Неоплаченная часть: <b style="font-size: 22px">{self.triads(columns[1])}</b> рублей.<br>
'''
        pyperclip.copy(res)

    def run(self):
        if any([self.tableWidget.item(self.tableWidget.rowCount() - 1, i) for i in range(self.tableWidget.columnCount())]):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
        
    
        
# Проверка ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    
# data = [
#     ['id', 'name', 'number'],
#     [0, 'Jeff', 1234],
#     [1, 'Bob', 5678],
#     [2, 'Bill', 9123]
# ]
# results = tabulate.tabulate(data, tablefmt='grid', headers='firstrow')
# print(results)

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.excepthook = except_hook
    app.exec()
