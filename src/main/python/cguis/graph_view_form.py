# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph_view_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_graph_view(object):
    def setupUi(self, graph_view):
        graph_view.setObjectName("graph_view")
        graph_view.resize(600, 399)
        self.cobox_chl = QtWidgets.QComboBox(graph_view)
        self.cobox_chl.setGeometry(QtCore.QRect(50, 10, 35, 20))
        self.cobox_chl.setMinimumSize(QtCore.QSize(35, 20))
        self.cobox_chl.setMaximumSize(QtCore.QSize(35, 20))
        self.cobox_chl.setObjectName("cobox_chl")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.gview = QtWidgets.QGraphicsView(graph_view)
        self.gview.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.gview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gview.setObjectName("gview")
        self.cobox_gph = QtWidgets.QComboBox(graph_view)
        self.cobox_gph.setGeometry(QtCore.QRect(10, 10, 35, 20))
        self.cobox_gph.setMinimumSize(QtCore.QSize(35, 20))
        self.cobox_gph.setMaximumSize(QtCore.QSize(35, 20))
        self.cobox_gph.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.cobox_gph.setObjectName("cobox_gph")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.pbtn_zoom_in = QtWidgets.QPushButton(graph_view)
        self.pbtn_zoom_in.setGeometry(QtCore.QRect(90, 10, 20, 20))
        self.pbtn_zoom_in.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_zoom_in.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_zoom_in.setObjectName("pbtn_zoom_in")
        self.pbtn_move_up = QtWidgets.QPushButton(graph_view)
        self.pbtn_move_up.setGeometry(QtCore.QRect(120, 10, 20, 20))
        self.pbtn_move_up.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_move_up.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_move_up.setObjectName("pbtn_move_up")
        self.pbtn_move_down = QtWidgets.QPushButton(graph_view)
        self.pbtn_move_down.setGeometry(QtCore.QRect(120, 50, 20, 20))
        self.pbtn_move_down.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_move_down.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_move_down.setObjectName("pbtn_move_down")
        self.pbtn_return_home = QtWidgets.QPushButton(graph_view)
        self.pbtn_return_home.setGeometry(QtCore.QRect(120, 30, 20, 20))
        self.pbtn_return_home.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_return_home.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_return_home.setObjectName("pbtn_return_home")
        self.pbtn_move_right = QtWidgets.QPushButton(graph_view)
        self.pbtn_move_right.setGeometry(QtCore.QRect(150, 30, 20, 20))
        self.pbtn_move_right.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_move_right.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_move_right.setObjectName("pbtn_move_right")
        self.pbtn_move_left = QtWidgets.QPushButton(graph_view)
        self.pbtn_move_left.setGeometry(QtCore.QRect(90, 30, 20, 20))
        self.pbtn_move_left.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_move_left.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_move_left.setObjectName("pbtn_move_left")
        self.pbtn_zoom_out = QtWidgets.QPushButton(graph_view)
        self.pbtn_zoom_out.setGeometry(QtCore.QRect(150, 10, 20, 20))
        self.pbtn_zoom_out.setMinimumSize(QtCore.QSize(20, 20))
        self.pbtn_zoom_out.setMaximumSize(QtCore.QSize(20, 20))
        self.pbtn_zoom_out.setObjectName("pbtn_zoom_out")
        self.gview.raise_()
        self.cobox_chl.raise_()
        self.cobox_gph.raise_()
        self.pbtn_zoom_in.raise_()
        self.pbtn_move_up.raise_()
        self.pbtn_move_down.raise_()
        self.pbtn_return_home.raise_()
        self.pbtn_move_right.raise_()
        self.pbtn_move_left.raise_()
        self.pbtn_zoom_out.raise_()

        self.retranslateUi(graph_view)
        QtCore.QMetaObject.connectSlotsByName(graph_view)

    def retranslateUi(self, graph_view):
        _translate = QtCore.QCoreApplication.translate
        graph_view.setWindowTitle(_translate("graph_view", "Form"))
        self.cobox_chl.setItemText(0, _translate("graph_view", "A"))
        self.cobox_chl.setItemText(1, _translate("graph_view", "1"))
        self.cobox_chl.setItemText(2, _translate("graph_view", "2"))
        self.cobox_chl.setItemText(3, _translate("graph_view", "3"))
        self.cobox_gph.setItemText(0, _translate("graph_view", "N"))
        self.cobox_gph.setItemText(1, _translate("graph_view", "V"))
        self.cobox_gph.setItemText(2, _translate("graph_view", "H"))
        self.cobox_gph.setItemText(3, _translate("graph_view", "F"))
        self.pbtn_zoom_in.setText(_translate("graph_view", "+"))
        self.pbtn_move_up.setText(_translate("graph_view", "U"))
        self.pbtn_move_down.setText(_translate("graph_view", "D"))
        self.pbtn_return_home.setText(_translate("graph_view", "H"))
        self.pbtn_move_right.setText(_translate("graph_view", "R"))
        self.pbtn_move_left.setText(_translate("graph_view", "L"))
        self.pbtn_zoom_out.setText(_translate("graph_view", "-"))


