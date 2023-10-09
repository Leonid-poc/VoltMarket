import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
import tabulate

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

    def getTable(self):
        array: list[list] = [[]]
        for y in range(self.tableWidget.rowCount()):
            for x in range(self.tableWidget.columnCount()):
                temp: str = self.getTableText(x, y)
                array[y].append(temp if temp else '')
            array.append([])
        array = list(filter(any, array))
        array.insert(0, self.headers)
        res = tabulate.tabulate(array, tablefmt='grid', headers='firstrow', numalign='center')
        print(res)

    def run(self):
        if any([self.tableWidget.item(self.tableWidget.rowCount() - 1, i) for i in range(self.tableWidget.columnCount())]):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
        
    
        
# Проверка ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    
data = [
    ['id', 'name', 'number'],
    [0, 'Jeff', 1234],
    [1, 'Bob', 5678],
    [2, 'Bill', 9123]
]
results = tabulate.tabulate(data, tablefmt='grid', headers='firstrow')
print(results)

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.excepthook = except_hook
    app.exec()