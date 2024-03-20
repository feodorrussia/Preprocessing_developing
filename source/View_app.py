import os.path
import sys

import numpy as np
import pandas as pd
import scipy.interpolate as sc_i
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QFileDialog

import source.ui_View_app_v000_MW as MW_Design


class App(QtWidgets.QMainWindow, MW_Design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле MW_Design.py
        super().__init__()
        self.setupUi(self)
        self.ui_elements = [self.pushButton_3, self.spinBox, self.doubleSpinBox, self.doubleSpinBox_2, self.toolButton,
                            self.toolButton_2]  # , self.

        self.filename = "def.csv"
        self.comm_filename = self.filename[:-4] + "_com.txt"

        self.db_np = np.array([np.linspace(0, 100, 101), np.array([0] * 101)])
        self.db_df = pd.DataFrame(self.db_np)
        self.s_point = 0
        self.START_IND = 2
        self.length = 101

        self.db_com = {}

        self.f_autoSave = False
        self.f_autoDelete = False
        self.f_index_com = False

        X = np.linspace(0, 100, 101)
        Y = [0] * 101
        self.spinBox.setValue(self.length)

        self.sc.figure.clear()

        ax = self.sc.figure.add_subplot(111)
        ax.plot(X, Y, marker='o', markersize=3)
        ax.grid(True)
        self.sc.draw()

        self.pushButton_3.clicked.connect(lambda: self.action('open'))
        self.toolButton.clicked.connect(lambda: self.action('back'))
        self.toolButton_2.clicked.connect(lambda: self.action('forward'))

        self.spinBox.valueChanged.connect(lambda: self.action('length'))

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
        elif key == QtCore.Qt.Key.Key_W or key == QtCore.Qt.Key.Key_Up:
            self.action('mark_up')
        elif key == QtCore.Qt.Key.Key_S or key == QtCore.Qt.Key.Key_Down:
            self.action('mark_down')
        elif key == QtCore.Qt.Key.Key_Space or key == QtCore.Qt.Key.Key_Enter:
            self.action('save')

    def action(self, event='plot'):
        if event == 'index':
            new_index = self.spinBox.value() - 1
            self.s_point = max(new_index, 0)
            self.s_point = min(new_index, self.db_np.shape[0])

        if event == 'back':
            self.s_point = max(self.s_point - 1, 0)
        elif event == 'forward':
            self.s_point = min(self.s_point + 1, self.db_np.shape[0] - 1)
        elif event == 'save':
            self.save_fragment_ed()
        elif event == 'delete':
            self.delete_fragment()
        elif event == 'open':
            # self.file_widget_ac()
            self.open_file()

        D_ID = self.db_np[self.s_point][self.START_IND - 2]
        CH_ID = self.db_np[self.s_point][self.START_IND - 1]
        mark = self.db_np[self.s_point][self.START_IND]
        length = self.db_np[self.s_point][self.START_IND + 1]
        rate = self.db_np[self.s_point][self.START_IND + 2]

        y_ = self.db_np[self.s_point][self.START_IND + 3:].tolist()
        x_ = np.linspace(1, len(y_), len(y_))

        self.sc.figure.clear()

        ax = self.sc.figure.add_subplot(111)
        ax.plot(x_, y_, marker='o', markersize=3)
        ax.set_title(
            f"ID файла диагностики: {D_ID}; № канала: {CH_ID}; Оценка: {mark}\n" +
            f"Длительность: {round(length, 3)} мкс; Количество точек (исходное/текущее): {int(length * 1000 * rate) + 1}/{len(y_)}\n",
            fontdict={'fontsize': 10}, loc="left")
        ax.grid(True)

        self.plainTextEdit.clear()
        if str(self.s_point) in self.db_com.keys():
            self.f_index_com = True
            self.plainTextEdit.insertPlainText(self.db_com[str(self.s_point)])
        else:
            self.f_index_com = False

        self.list_spinBox.setValue(self.s_point + 1)
        self.label.setText(f"/{self.db_np.shape[0]}")
        self.spinBox.setMinimum(0)
        self.spinBox_2.setMaximum(len(y_))
        self.list_spinBox.setMinimum(1)
        self.list_spinBox.setMaximum(self.db_np.shape[0])
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(len(y_))
        self.doubleSpinBox.setValue(mark)

        if event == 'mark_up':
            self.doubleSpinBox.setValue(1)
        elif event == 'mark_down':
            self.doubleSpinBox.setValue(0)

        self.sc.draw()

    # activate File widget
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "CSV Files (*.csv);;All Files (*)")
        if filename and '.csv' in filename:
            self.db_df = pd.read_csv(filename)
            self.db_np = self.db_df.to_numpy()
            self.s_point = 0
            self.filename = filename
            self.comm_filename = self.filename[:-4] + "_com.txt"

            self.f_autoSave = False
            self.f_autoDelete = False

            if os.path.isfile(self.comm_filename):
                with open(self.comm_filename, 'r') as com_file:
                    comments = com_file.read().split("\n###\n")[:-1]
                    for comm in comments:
                        ind, text = comm.split(" _%%%_ ")
                        self.db_com[ind.strip()] = text
            else:
                self.db_com = {}

            self.label_5.setText(f"File: {self.filename.split('/')[-1]}")
            print(f"----\nSuccessfully open file {self.filename.split('/')[-1]}")

    # check changes
    def check_changes(self):

        # CHECKING FRAGMENTS CHANGES
        fragment_values = self.db_np[self.s_point][self.START_IND + 3:].tolist()
        left = 0
        right = len(fragment_values)
        f_changes = False
        edited_log_text = "----\nFragment edited:"

        # check edges changes
        if self.spinBox.value() != 0:
            left = self.spinBox.value()
            edited_log_text += f"\nleft edge new: {self.spinBox.value()}"
            print(f"----\nEditing fragment {self.s_point}\nLeft edge changes successfully received.")
            f_changes = True

        if self.spinBox_2.value() != len(fragment_values):
            right = self.spinBox_2.value()
            edited_log_text += f"\nright edge new: {self.spinBox_2.value()}"
            print(f"Right edge changes successfully received.")
            f_changes = True

        if f_changes:
            fragment_x = np.linspace(1, len(fragment_values), len(fragment_values))
            # interpolate
            new_values = sc_i.interp1d(
                np.linspace(fragment_x[0], fragment_x[-1], right - left), fragment_values[left:right],
                kind="quadratic")(
                np.linspace(fragment_x[0], fragment_x[-1], len(fragment_values)))

            self.db_np[self.s_point][self.START_IND + 3:] = new_values

            length = self.db_np[self.s_point][self.START_IND + 1]
            self.db_np[self.s_point][self.START_IND + 1] = (right - left) / len(fragment_values) * length
            edited_log_text += f"\nnew length: {self.db_np[self.s_point][self.START_IND + 1]} mks " \
                               f"({int(self.db_np[self.s_point][self.START_IND + 1] * 1000 * self.db_np[self.s_point][self.START_IND + 2])} points)"
            print(f"New length: {self.db_np[self.s_point][self.START_IND + 1]} mks " +
                  f"({int(self.db_np[self.s_point][self.START_IND + 1] * 1000 * self.db_np[self.s_point][self.START_IND + 2])} points)")

        # check mark changes
        if self.doubleSpinBox.value() != self.db_np[self.s_point][self.START_IND]:
            print(f"Mark changes successfully received. " +
                  f"Old: {self.db_np[self.s_point][self.START_IND]} | New: {self.doubleSpinBox.value()}")
            edited_log_text += f"\nmark: old: {self.db_np[self.s_point][self.START_IND]} | new: {self.doubleSpinBox.value()}"
            self.db_np[self.s_point][self.START_IND] = self.doubleSpinBox.value()
            f_changes = True

        if f_changes:
            text = self.plainTextEdit.toPlainText().strip()
            self.plainTextEdit.clear()
            self.plainTextEdit.insertPlainText("\n".join([text, edited_log_text]))

        # CHECKING COMMENTS CHANGES (if name of file will new, com saves to new com file)
        text = self.plainTextEdit.toPlainText().strip()
        if text != "" or (self.f_index_com and self.db_com[str(self.s_point)].strip() != text):
            self.db_com[str(self.s_point)] = text

            tot_text = ""
            for i in self.db_com.keys():
                tot_text += i + " _%%%_ " + self.db_com[i] + "\n###\n"

            self.save_comm_ed(tot_text)

    # save changes to comment files
    def save_comm_ed(self, text):
        with open(self.comm_filename, "w") as file:
            file.write(text)
        print(f"----\nComment to fragment {self.s_point} saved successfully to {self.comm_filename.split('/')[-1]}")

    # save changes to db
    def save_fragment_ed(self):
        if not self.f_autoSave:
            # version dialog window
            version_dw = VersionDialog()
            if self.f_autoDelete:
                version_dw.show_checkBox.setText("Использовать текущую версию")
            version_dw.exec()

            if version_dw.text_input.text() == "#_cancel_#":
                return

            self.check_version(version_dw)

            self.f_autoSave = version_dw.show_checkBox.isChecked()

        self.check_changes()

        self.db_df.loc[self.s_point] = self.db_np[self.s_point]
        self.db_df.to_csv(self.filename, index=False)
        print(f"----\nFragment {self.s_point} changes saved successfully to {self.filename.split('/')[-1]}")

    def delete_fragment(self):
        if self.db_np.shape[0] == 1:
            return

        if not self.f_autoDelete:
            # version dialog window
            version_dw = VersionDialog()
            version_dw.save_button.setText("Удалить")
            if self.f_autoSave:
                version_dw.show_checkBox.setText("Использовать текущую версию")
            version_dw.exec()

            if version_dw.text_input.text() == "#_cancel_#":
                return

            self.check_version(version_dw)

            self.f_autoDelete = version_dw.show_checkBox.isChecked()

        if os.path.exists(self.comm_filename) and str(self.s_point) in self.db_com.keys():
            # del comment of fragment
            self.db_com.pop(str(self.s_point))

            for key in list(filter(lambda x: int(x) > self.s_point, self.db_com.keys())):
                self.db_com[str(int(key) - 1)] = self.db_com.pop(key)

            tot_text = ""
            for i in self.db_com.keys():
                tot_text += i + " _%%%_ " + self.db_com[i] + "\n###\n"
            self.save_comm_ed(tot_text)

        if self.db_np.shape[0] == self.s_point + 1:
            self.s_point -= 1

        self.db_df = self.db_df.drop(self.s_point, axis=0)
        self.db_np = self.db_df.to_numpy()

        self.db_df.to_csv(self.filename, index=False)
        self.db_df = pd.read_csv(self.filename)
        print(f"----\nFragment {self.s_point} deleted successfully from {self.filename.split('/')[-1]}")

    def check_version(self, version_dw):
        if version_dw.text_input.text() != "" and version_dw.text_input.text() != "#_cancel_#":
            # new name
            self.filename = self.filename[:-4] + f"_v{version_dw.text_input.text()}.csv"

            # save comments
            self.comm_filename = self.comm_filename[:-8] + f"_v{version_dw.text_input.text()}_com.txt"

            if os.path.exists(self.comm_filename):
                with open(self.comm_filename, 'r') as file_r:
                    coms = file_r.read()
                with open(self.comm_filename, 'w') as file_w:
                    file_w.write(coms)

            self.label_5.setText(f"File: {self.filename.split('/')[-1]}")
            print(f"----\nFile version successfully changed to {self.filename.split('/')[-1]}")


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса App
    window.show()  # Показываем окно
    app.exec()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
