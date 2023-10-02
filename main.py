import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.clicked.connect(self.run)
        pass
    
    def getTableText(self, x, y):
        text = self.tableWidget.item(y, x)
        if text == None: return text
        return text.text()
    
    def run(self):
        if any([self.tableWidget.item(self.tableWidget.rowCount() - 1, i) for i in range(self.tableWidget.columnCount())]):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
        
    
        
# Проверка ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    
# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.excepthook = except_hook
    app.exec()