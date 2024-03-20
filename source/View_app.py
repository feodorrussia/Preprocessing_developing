import sys

import numpy as np
import pandas as pd
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QFileDialog

import source.ui_View_app_v000_MW as MW_Design


def increase_lims(lim):
    percent = 0.01
    return lim + (lim * percent if lim >= 0 else lim * (-1) * percent)


class App(QtWidgets.QMainWindow, MW_Design.Ui_MainWindow):
    def __init__(self, df: pd.DataFrame = None):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле MW_Design.py
        super().__init__()
        self.setupUi(self)
        self.ui_elements = [self.pushButton_3, self.spinBox, self.left_spinBox, self.right_spinBox, self.toolButton,
                            self.toolButton_2]  # , self.

        if df is not None:
            self.filename = "None (data from program)"
            self.db_np = df.to_numpy()
            self.db_df = df.copy()
        else:
            self.filename = "def.csv"

            self.db_np = np.column_stack([np.linspace(0, 100, 101), np.array([0] * 101)])
            self.db_df = pd.DataFrame(self.db_np, columns=["t", "ch0"])

        self.columns = self.db_df.columns
        self.SIGNAL_LENGTH = self.db_np.shape[0]
        self.Y_LIM = [increase_lims(self.db_df[self.columns[1:]].min().min()),
                      increase_lims(self.db_df[self.columns[1:]].max().max())]
        self.step = 101

        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(self.SIGNAL_LENGTH)
        self.spinBox.setValue(self.step)

        self.left_spinBox.setMinimum(0)
        self.left_spinBox.setMaximum(self.step)
        self.left_spinBox.setValue(0)

        self.right_spinBox.setMinimum(0)
        self.right_spinBox.setMaximum(self.SIGNAL_LENGTH)
        self.right_spinBox.setValue(self.step)

        self.action("plot")

        self.pushButton_3.clicked.connect(lambda: self.action('open'))
        self.toolButton.clicked.connect(lambda: self.action('back'))
        self.toolButton_2.clicked.connect(lambda: self.action('forward'))

        self.spinBox.valueChanged.connect(lambda: self.action('step'))

        self.left_spinBox.valueChanged.connect(lambda: self.action('length'))
        self.right_spinBox.valueChanged.connect(lambda: self.action('length'))

        self.label_5.setText(f"File: {self.filename.split('/')[-1]}")

        self.clearWindowFocus()

    def clearWindowFocus(self):
        for elem in self.ui_elements:
            elem.clearFocus()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == QtCore.Qt.Key.Key_Escape:
            self.clearWindowFocus()
        elif key == QtCore.Qt.Key.Key_A or key == QtCore.Qt.Key.Key_Left:
            self.action('back')
        elif key == QtCore.Qt.Key.Key_D or key == QtCore.Qt.Key.Key_Right:
            self.action('forward')

    def action(self, event='plot'):
        if event == 'step':
            self.step = self.spinBox.value()
        if event == 'back':
            self.left_spinBox.setValue(max(self.left_spinBox.value() - self.step, 0))
            self.right_spinBox.setValue(min(self.right_spinBox.value() - self.step, self.SIGNAL_LENGTH))
        elif event == 'forward' and self.right_spinBox.value() != self.SIGNAL_LENGTH:
            self.left_spinBox.setValue(min(self.left_spinBox.value() + self.step, self.SIGNAL_LENGTH))
            self.right_spinBox.setValue(min(self.right_spinBox.value() + self.step, self.SIGNAL_LENGTH))
        elif event == 'open':
            self.open_file()

        self.sc.figure.clear()
        ax = self.sc.figure.add_subplot(111)

        x_ = np.array(self.db_df[self.columns[0]])[self.left_spinBox.value():self.right_spinBox.value()]
        for col in self.columns[1:]:
            y_ = np.array(self.db_df[col])[self.left_spinBox.value():self.right_spinBox.value()]
            if self.point_checkBox.isChecked():
                ax.plot(x_, y_, marker='o', markersize=2, label=col)
            else:
                ax.plot(x_, y_, label=col)

        ax.set_title(f"Pu-pu-pu",
                     fontdict={'fontsize': 10}, loc="left")
        ax.legend()
        ax.set_ylim(self.Y_LIM)
        x_min = np.array(self.db_df[self.columns[0]])[self.left_spinBox.value()]
        x_max = np.array(self.db_df[self.columns[0]])[self.right_spinBox.value()]
        try:
            ax.set_xticks(np.round(np.arange(x_min, x_max + 1e-3, (x_max - x_min) / 8), 5))
        except ValueError as e:
            pass
        ax.grid(True)

        self.left_spinBox.setMaximum(self.right_spinBox.value())
        self.right_spinBox.setMinimum(self.left_spinBox.value())

        self.sc.draw()

        # activate File widget

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "CSV Files (*.csv);;All Files (*)")
        if filename and '.csv' in filename:
            self.db_df = pd.read_csv(filename)
            self.db_np = self.db_df.to_numpy()

            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(self.db_np.shape[0])
            self.spinBox.setValue(self.step)

            self.left_spinBox.setMinimum(0)
            self.left_spinBox.setMaximum(self.step)
            self.left_spinBox.setValue(0)

            self.right_spinBox.setMinimum(0)
            self.right_spinBox.setMaximum(self.db_np.shape[1])
            self.right_spinBox.setValue(self.step)

            self.filename = filename

            self.label_5.setText(f"File: {self.filename.split('/')[-1]}")
            print(f"----\nSuccessfully open file {self.filename.split('/')[-1]}")


def main(df=None):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App(df)  # Создаём объект класса App
    window.show()  # Показываем окно
    app.exec()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
