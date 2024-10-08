# Form implementation generated from reading ui file 'rest_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RestWindow(object):

    def setupUi(self, RestWindow):
        RestWindow.setObjectName("RestWindow")
        RestWindow.resize(1200, 670)
        RestWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        RestWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(parent=RestWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_move_rest_to_full_half_hour = QtWidgets.QPushButton(
            parent=self.centralwidget
        )
        self.btn_move_rest_to_full_half_hour.setObjectName(
            "btn_move_rest_to_full_half_hour"
        )
        self.horizontalLayout_6.addWidget(self.btn_move_rest_to_full_half_hour)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
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
        self.verticalLayout.addWidget(self.lbl_rest_message_text)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(spacerItem2)
        self.lbl_remaining_rest_time = QtWidgets.QLabel(
            parent=self.centralwidget
        )
        self.lbl_remaining_rest_time.setText("")
        self.lbl_remaining_rest_time.setObjectName("lbl_remaining_rest_time")
        self.verticalLayout.addWidget(self.lbl_remaining_rest_time)
        self.rest_progress_bar = QtWidgets.QProgressBar(
            parent=self.centralwidget
        )
        self.rest_progress_bar.setMaximum(100)
        self.rest_progress_bar.setProperty("value", 100)
        self.rest_progress_bar.setObjectName("rest_progress_bar")
        self.verticalLayout.addWidget(self.rest_progress_bar)
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
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        RestWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RestWindow)
        QtCore.QMetaObject.connectSlotsByName(RestWindow)

    def retranslateUi(self, RestWindow):
        _translate = QtCore.QCoreApplication.translate
        RestWindow.setWindowTitle(_translate("RestWindow", "Resty"))
        self.btn_move_rest_to_full_half_hour.setText(
            _translate("RestWindow", "!")
        )
        self.lbl_rest_message_text.setText(
            _translate("RestWindow", "Time to have a break")
        )
        self.btn_finish_rest.setText(
            _translate("RestWindow", "Закончить перерыв")
        )
        self.btn_move_rest_by_5_min.setText(
            _translate("RestWindow", "Отложить перерыв на 5 мин")
        )
        self.btn_move_rest_by_10_min.setText(
            _translate("RestWindow", "Отложить перерыв на 10 мин")
        )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RestWindow = QtWidgets.QMainWindow()
    ui = Ui_RestWindow()
    ui.setupUi(RestWindow)
    RestWindow.show()
    sys.exit(app.exec())
