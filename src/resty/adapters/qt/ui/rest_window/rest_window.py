# Form implementation generated from reading ui file 'rest_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 670)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.lbl_rest_message_text = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.lbl_rest_message_text.setFont(font)
        self.lbl_rest_message_text.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.PreventContextMenu
        )
        self.lbl_rest_message_text.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.lbl_rest_message_text.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.lbl_rest_message_text.setObjectName("lbl_rest_message_text")
        self.verticalLayout_2.addWidget(self.lbl_rest_message_text)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.lbl_remaining_rest_time = QtWidgets.QLabel(
            parent=self.centralwidget
        )
        self.lbl_remaining_rest_time.setText("")
        self.lbl_remaining_rest_time.setObjectName("lbl_remaining_rest_time")
        self.verticalLayout_2.addWidget(self.lbl_remaining_rest_time)
        self.rest_progress_bar = QtWidgets.QProgressBar(
            parent=self.centralwidget
        )
        self.rest_progress_bar.setMaximum(100)
        self.rest_progress_bar.setProperty("value", 100)
        self.rest_progress_bar.setObjectName("rest_progress_bar")
        self.verticalLayout_2.addWidget(self.rest_progress_bar)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(200, -1, 200, 30)
        self.horizontalLayout_5.setSpacing(30)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_finish_rest = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_finish_rest.setMinimumSize(QtCore.QSize(0, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_finish_rest.setFont(font)
        self.btn_finish_rest.setObjectName("btn_finish_rest")
        self.horizontalLayout_5.addWidget(self.btn_finish_rest)
        self.btn_move_rest_by_5_min = QtWidgets.QPushButton(
            parent=self.centralwidget
        )
        self.btn_move_rest_by_5_min.setMinimumSize(QtCore.QSize(0, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_move_rest_by_5_min.setFont(font)
        self.btn_move_rest_by_5_min.setObjectName("btn_move_rest_by_5_min")
        self.horizontalLayout_5.addWidget(self.btn_move_rest_by_5_min)
        self.btn_move_rest_by_10_min = QtWidgets.QPushButton(
            parent=self.centralwidget
        )
        self.btn_move_rest_by_10_min.setMinimumSize(QtCore.QSize(0, 24))
        self.btn_move_rest_by_10_min.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_move_rest_by_10_min.setFont(font)
        self.btn_move_rest_by_10_min.setObjectName("btn_move_rest_by_10_min")
        self.horizontalLayout_5.addWidget(self.btn_move_rest_by_10_min)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Resty"))
        self.lbl_rest_message_text.setText(
            _translate("MainWindow", "Time to have a break")
        )
        self.btn_finish_rest.setText(
            _translate("MainWindow", "Закончить перерыв")
        )
        self.btn_move_rest_by_5_min.setText(
            _translate("MainWindow", "Отложить перерыв на 5 мин")
        )
        self.btn_move_rest_by_10_min.setText(
            _translate("MainWindow", "Отложить перерыв на 10 мин")
        )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
