import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore, QtWidgets


# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         loader = QUiLoader()
#         self.window = loader.load(r"C:\Users\nimbus\Desktop\KAMILA\py_qt_designer\mainwindow.ui", self)
#         self.show()

# if __name__ == "__main__":

#     QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
#     app = QtWidgets.QApplication(sys.argv)
#     win = MainWindow()
#     sys.exit(app.exec())




loader = QUiLoader()
app = QApplication(sys.argv)

window = loader.load(r"C:\Users\nimbus\Desktop\KAMILA\py_qt_designer\mainwindow.ui", None)

window.show()
app.exec()