from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QDoubleSpinBox, QSpinBox, QHBoxLayout, QLabel,
                               QPushButton, QCheckBox,
                               QSizePolicy, QSpacerItem, QToolButton,
                               QVBoxLayout, QWidget, QGridLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)
        self.axes = self.figure.add_subplot(111)
        super(MplCanvas, self).__init__(self.figure)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.point_checkBox = QCheckBox(self.centralwidget)
        self.point_checkBox.setChecked(False)
        self.point_checkBox.setText("Show points")
        self.pushButton_3.setObjectName(u"point_checkBox")

        self.horizontalLayout_3.addWidget(self.point_checkBox)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.sc = MplCanvas(self.centralwidget, width=1, height=1, dpi=100)
        self.sc.setMinimumSize(QSize(0, 400))
        self.toolbar = NavigationToolbar(self.sc, self.centralwidget)

        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.sc)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(32, 0))
        self.toolButton.setArrowType(Qt.LeftArrow)

        self.horizontalLayout_7.addWidget(self.toolButton)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_8 = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(60, 0))
        self.spinBox.setMaximumSize(QSize(30, 18))
        self.spinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.spinBox)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(30, 0))
        self.label.setMaximumSize(QSize(50, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.toolButton_2 = QToolButton(self.centralwidget)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setMinimumSize(QSize(32, 0))
        self.toolButton_2.setArrowType(Qt.RightArrow)

        self.horizontalLayout_7.addWidget(self.toolButton_2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.left_spinBox = QSpinBox(self.centralwidget)
        self.left_spinBox.setObjectName(u"doubleSpinBox")
        self.left_spinBox.setMinimumSize(QSize(70, 0))
        self.left_spinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.left_spinBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setMaximumSize(QSize(100, 16777215))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_4)

        self.right_spinBox = QSpinBox(self.centralwidget)
        self.right_spinBox.setObjectName(u"doubleSpinBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.right_spinBox.sizePolicy().hasHeightForWidth())
        self.right_spinBox.setSizePolicy(sizePolicy3)
        self.right_spinBox.setMinimumSize(QSize(70, 0))
        self.right_spinBox.setMaximumSize(QSize(100, 16777215))
        self.right_spinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.right_spinBox.setMaximum(99990000.000000000000000)

        self.verticalLayout_2.addWidget(self.right_spinBox)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pushButton_3.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"File:", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"point", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"L. Edge", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"R. Edge", None))
    # retranslateUi
