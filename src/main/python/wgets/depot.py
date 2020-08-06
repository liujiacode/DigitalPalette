# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details. 

Please visit https://github.com/liujiacode/DigitalPalette for more 
infomation about DigitalPalette.

Copyright © 2019-2020 by Eigenmiao. All Rights Reserved.
"""

import re
import os
import sys
import json
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QFrame, QShortcut, QMenu, QAction, QDialog, QDialogButtonBox, QPushButton, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QMimeData, QPoint, QUrl
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QCursor, QKeySequence, QPixmap, QImage, QIcon, QDrag
from cguis.design.info_dialog import Ui_InfoDialog
from cguis.resource import view_rc
from clibs.color import FakeColor, Color
from clibs.export import export_list


class Info(QDialog, Ui_InfoDialog):
    """
    Info object based on QDialog. Init color set information.
    """
    
    def __init__(self, wget, args):
        """
        Init information.
        """

        super().__init__(wget, Qt.WindowCloseButtonHint)
        self.setupUi(self)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        self._clone = None
        self._unit_cell = UnitCell(self.colors, self._args, [None, None, None, None, None], "", "", "", (-1.0, -1.0))

        color_grid_layout = QGridLayout(self.colors)
        color_grid_layout.setContentsMargins(1, 1, 1, 1)
        color_grid_layout.addWidget(self._unit_cell)

        # init buttons.
        self.buttonBox.clear()

        self._btn_1 = QPushButton()
        self._btn_1.clicked.connect(self.application)
        self.buttonBox.addButton(self._btn_1, QDialogButtonBox.AcceptRole)

        self._btn_2 = QPushButton()
        self._btn_2.clicked.connect(self.close)
        self.buttonBox.addButton(self._btn_2, QDialogButtonBox.RejectRole)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def clone_cell(self, unit_cell):
        self._clone = unit_cell

        self._unit_cell.color_set = unit_cell.color_set
        self._unit_cell.hm_rule = unit_cell.hm_rule

        if unit_cell.name:
            self.name_ledit.setText(unit_cell.name)

        else:
            self.name_ledit.setText(self._cell_descs[0])

        if unit_cell.desc:
            self.desc_tedit.setText(unit_cell.desc)

        else:
            color_signs = []

            for i in (2, 1, 0, 3, 4):
                if self._unit_cell.color_set[i]:
                    sign = Color.sign(self._unit_cell.color_set[i].hsv)
                    color_signs.append(self._color_descs[sign[0]] + self._color_descs[sign[1] + 10])

            if len(color_signs) == 5:
                self.desc_tedit.setText(self._cell_descs[2].format(*color_signs) + "\n")

            else:
                self.desc_tedit.setText("")

        self.hm_rule_label.setText(self._rule_descs[self._args.global_hm_rules.index(unit_cell.hm_rule)])

        if unit_cell.cr_time[0] < 0:
            time_str = self._cell_descs[1]

        else:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unit_cell.cr_time[0]))

        if unit_cell.cr_time[1] < 0:
            time_str += "\n{}".format(self._cell_descs[1])

        else:
            time_str += "\n{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unit_cell.cr_time[1])))

        self.cr_time_label.setText(time_str)

    def application(self):
        name = re.split(r"[\v\a\f\n\r\t]", str(self.name_ledit.text()))[0].lstrip().rstrip()
        desc = re.split(r"[\v\a\f]", str(self.desc_tedit.toPlainText()))[0].lstrip().rstrip()

        if name != self._clone.name or desc != self._clone.desc:
            self._clone.name = name
            self._clone.desc = desc
            self._clone.cr_time = (self._clone.cr_time[0], time.time())

        self._clone = None

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.setWindowTitle(self._dialog_descs[0])
        self._btn_1.setText(self._dialog_descs[1])
        self._btn_2.setText(self._dialog_descs[2])

        self.retranslateUi(self)

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._dialog_descs = (
            _translate("Info", "Information"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
        )

        self._cell_descs = (
            _translate("Info", "DigiPale Color Set"),
            _translate("Info", "Unknown"),
            _translate("Info", "This color set includes: {}, {}, {}, {} and {}."),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )

        self._color_descs = (
            _translate("DigitalPalette", "Deep "),
            _translate("DigitalPalette", "Snow "),
            _translate("DigitalPalette", "Heavy "),
            _translate("DigitalPalette", "Dull "),
            _translate("DigitalPalette", "Grey "),
            _translate("DigitalPalette", "Pale "),
            _translate("DigitalPalette", "Light "),
            _translate("DigitalPalette", "Bright "),
            _translate("DigitalPalette", "Dark "),
            _translate("DigitalPalette", "Vivid "),
            _translate("DigitalPalette", "Black"),
            _translate("DigitalPalette", "White"),
            _translate("DigitalPalette", "Red"),
            _translate("DigitalPalette", "Yellow"),
            _translate("DigitalPalette", "Green"),
            _translate("DigitalPalette", "Cyan"),
            _translate("DigitalPalette", "Blue"),
            _translate("DigitalPalette", "Magenta"),
        )


class UnitCell(QWidget):
    """
    UnitCell objet based on QWidget. Init an unit cell in depot.
    """

    def __init__(self, wget, args, hsv_set, hm_rule, name, desc, cr_time):
        """
        Init empty unit cell.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self.activated = False
        self.color_set = []

        for hsv in hsv_set:
            if hsv == None:
                self.color_set.append(None)

            else:
                self.color_set.append(FakeColor(Color.hsv2rgb(hsv), hsv, Color.hsv2hec(hsv)))

        self.color_set = tuple(self.color_set)
        self.hm_rule = str(hm_rule)
        self.cr_time = tuple(cr_time)
        self.name = re.split(r"[\v\a\f\n\r\t]", str(name))[0].lstrip().rstrip()
        self.desc = re.split(r"[\v\a\f]", str(desc))[0].lstrip().rstrip()

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        cs_wid = int(min(self.width(), self.height()) * self._args.coset_ratio / 2)

        cs_boxes = (
            (self.width() / 2 - cs_wid, self.height() / 2 - cs_wid, cs_wid, cs_wid),
            (self.width() / 2, self.height() / 2 - cs_wid, cs_wid, cs_wid),
            (self.width() / 2 - cs_wid, self.height() / 2, cs_wid, cs_wid),
            (self.width() / 2, self.height() / 2, cs_wid, cs_wid),
            (self.width() / 2 - cs_wid / 2, self.height() / 2 - cs_wid / 2, cs_wid, cs_wid),
        )

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self.activated:
            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))
            painter.setBrush(QColor(Qt.white))
            painter.drawRoundedRect(self._args.negative_wid, self._args.negative_wid, self.width() - self._args.negative_wid * 2, self.height() - self._args.negative_wid * 2, self.width() / 9, self.height() / 9)

        for idx in range(5):
            if self.activated:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.negative_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            if self.color_set[4 - idx] == None:
                painter.setBrush(QBrush(Qt.NoBrush))

            else:
                painter.setBrush(QColor(*self.color_set[4 - idx].rgb))

            painter.drawRoundedRect(*cs_boxes[idx], cs_wid / 9, cs_wid / 9)

        painter.end()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        if self.name:
            self.setToolTip(self.name)

        else:
            self.setToolTip(self._cell_descs[0])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._cell_descs = (
            _translate("Info", "DigiPale Color Set"),
        )


class Depot(QWidget):
    """
    Depot object based on QWidget. Init a color set depot in workarea.
    """

    ps_update = pyqtSignal(bool)
    ps_export = pyqtSignal(int)
    ps_status_changed = pyqtSignal(tuple)
    ps_dropped = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init color set depot.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._drop_file = None
        self._left_click = False
        self._drag_file = False
        self._start_hig = None
        self._start_pt = None
        self._current_idx = None
        self._fetched_cell = None
        self._press_key = 0

        # load translations.
        self._func_tr_()

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea(self)
        self._scroll_area.setFrameShape(QFrame.Box)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)
        grid_layout.addWidget(self._scroll_area)

        self._scroll_bar = self._scroll_area.verticalScrollBar()

        self._scroll_contents = QWidget()
        self._scroll_grid_layout = QGridLayout(self._scroll_contents)
        self._scroll_grid_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setWidget(self._scroll_contents)

        self.initialize()

        self._info = Info(self, self._args)

        self.create_menu()
        self.update_text()

        shortcut = QShortcut(QKeySequence("Del"), self)
        shortcut.activated.connect(self.delete_set)
        shortcut = QShortcut(QKeySequence("D"), self)
        shortcut.activated.connect(self.delete_set)

        shortcut = QShortcut(QKeySequence("Insert"), self)
        shortcut.activated.connect(self.insert_set)
        shortcut = QShortcut(QKeySequence("I"), self)
        shortcut.activated.connect(self.insert_set)

        shortcut = QShortcut(QKeySequence("Enter"), self)
        shortcut.activated.connect(self.detail_set)
        shortcut = QShortcut(QKeySequence("F"), self)
        shortcut.activated.connect(self.detail_set)

        shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut.activated.connect(self.clipboard_cur("rgb"))

        shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        shortcut.activated.connect(self.clipboard_cur("hsv"))

        shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        shortcut.activated.connect(self.clipboard_cur("hec"))

        shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        shortcut.activated.connect(self.clipboard_in)

        shortcut = QShortcut(QKeySequence("PgUp"), self)
        shortcut.activated.connect(self.page_up)

        shortcut = QShortcut(QKeySequence("PgDown"), self)
        shortcut.activated.connect(self.page_down)

        shortcut = QShortcut(QKeySequence("End"), self)
        shortcut.activated.connect(self.page_end)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        self._pl_wid = int((self.width() - 2) / self._args.stab_column)
        self._tot_rows = len(self._args.stab_ucells) // self._args.stab_column if len(self._args.stab_ucells) % self._args.stab_column == 0 else len(self._args.stab_ucells) // self._args.stab_column + 1

        height = self._pl_wid * self._tot_rows
        height = height if height > self._scroll_area.height() else self._scroll_area.height()

        self._scroll_contents.setMinimumSize(self._pl_wid * self._args.stab_column, height)
        self._scroll_contents.setMaximumSize(self._pl_wid * self._args.stab_column, height)

        for i in range(self._tot_rows):
            for j in range(self._args.stab_column):
                idx = self._args.stab_column * i + j

                if idx < len(self._args.stab_ucells) and isinstance(self._args.stab_ucells[idx], UnitCell):
                    self._args.stab_ucells[idx].setGeometry(self._pl_wid * j, self._pl_wid * i, self._pl_wid, self._pl_wid)

        status_idx = self._current_idx

        if status_idx == None:
            status_idx = 0

        else:
            status_idx = status_idx + 1

        self.ps_status_changed.emit((self._tot_rows, self._args.stab_column, len(self._args.stab_ucells) - 1, status_idx))

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self._press_key = 1
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Control:
            self._press_key = 2
            self.setCursor(QCursor(Qt.PointingHandCursor))
            event.accept()

        elif event.key() == Qt.Key_Space:
            self._press_key = 3
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            event.accept()

        else:
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))
            event.ignore()

    def keyReleaseEvent(self, event):
        self._press_key = 0
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.ignore()

    def mousePressEvent(self, event):
        point = np.array((event.x() - self._scroll_contents.x(), event.y() - self._scroll_contents.y()))

        col = point[0] // self._pl_wid
        row = point[1] // self._pl_wid

        if self._press_key == 2 and event.button() == Qt.LeftButton:
            color_list = []

            for unit_cell in self._args.stab_ucells[:-1]:
                if isinstance(unit_cell, UnitCell):
                    color_list.append((unit_cell.color_set, unit_cell.hm_rule, unit_cell.name, unit_cell.desc, unit_cell.cr_time))

            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "depot"}
            color_dict["palettes"] = export_list(color_list)
            color_path = os.sep.join((self._args.global_temp_dir.path(), "DigiPale_Depot_{}.dpc".format(abs(hash(str(color_dict))))))

            with open(color_path, "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4, ensure_ascii=False)

            self._drag_file = True

            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setUrls([QUrl.fromLocalFile(color_path)])
            drag.setMimeData(mimedata)
            pixmap = QPixmap(":/images/images/file_depot_128.png")
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            self._drag_file = False
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))

        elif col <= self._args.stab_column:
            idx = self._args.stab_column * row + col

            if event.button() == Qt.MidButton or (self._press_key == 3 and event.button() == Qt.LeftButton):
                if event.button() == Qt.MidButton:
                    self.setCursor(QCursor(Qt.ClosedHandCursor))

                self._start_hig = self._scroll_bar.value() + event.y()

            elif idx < len(self._args.stab_ucells):
                self.activate_idx(idx)

                if event.button() == Qt.LeftButton and idx < len(self._args.stab_ucells) - 1:
                    self._left_click = True
                    self._start_pt = np.array((event.x(), event.y()))

                    self._fetched_cell = self._args.stab_ucells[self._current_idx]
                    self._args.stab_ucells[self._current_idx] = None

                    self._fetched_cell.raise_()

            else:
                self.activate_idx(None)

        else:
            self.activate_idx(None)

        event.accept()

    def mouseMoveEvent(self, event):
        if self._press_key == 1 and self._left_click:
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "set"}
            color_dict["palettes"] = export_list([(self._fetched_cell.color_set, self._fetched_cell.hm_rule, self._fetched_cell.name, self._fetched_cell.desc, self._fetched_cell.cr_time),])
            color_path = os.sep.join((self._args.global_temp_dir.path(), "DigiPale_Set_{}.dps".format(abs(hash(str(color_dict))))))

            with open(color_path, "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4, ensure_ascii=False)

            self._drag_file = True

            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setUrls([QUrl.fromLocalFile(color_path)])
            drag.setMimeData(mimedata)
            pixmap = QPixmap(":/images/images/file_set_128.png")
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            self._args.stab_ucells[self._current_idx] = self._fetched_cell
            self._fetched_cell = None

            self._left_click = False
            self._start_pt = None

            self._drag_file = False
            self._press_key = 0
            self.setCursor(QCursor(Qt.ArrowCursor))

            self.update()
            event.accept()

        elif self._left_click:
            if isinstance(self._start_pt, np.ndarray) and np.linalg.norm(self._start_pt - np.array((event.x(), event.y()))) < self._pl_wid / 5:
                # fixed icon in small region.
                event.ignore()

            else:
                x = event.x()
                y = event.y()
                x = x if x > self._pl_wid / 5 else self._pl_wid / 5
                x = x if x < self.width() - self._pl_wid / 5 else self.width() - self._pl_wid / 5
                y = y if y > self._pl_wid / 5 else self._pl_wid / 5
                y = y if y < self.height() - self._pl_wid / 5 else self.height() - self._pl_wid / 5
                x = int(x) - self._scroll_contents.x()
                y = int(y) - self._scroll_contents.y()

                self._start_pt = None

                col = x // self._pl_wid
                row = y // self._pl_wid

                if col <= self._args.stab_column:
                    idx = self._args.stab_column * row + col

                    if idx < len(self._args.stab_ucells) - 1:
                        self._args.stab_ucells.pop(self._current_idx)
                        self._current_idx = idx

                        self._args.stab_ucells.insert(idx, None)

                self._fetched_cell.setGeometry(x - self._pl_wid / 2, y - self._pl_wid / 2, self._pl_wid, self._pl_wid)

                self.update()
                event.accept()

        elif self._start_hig != None:
            self._scroll_bar.setValue(self._start_hig - event.y())

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._press_key = 0
        self._start_hig = None

        if self._left_click:
            self._args.stab_ucells[self._current_idx] = self._fetched_cell
            self._fetched_cell = None

            self._left_click = False
            self._start_pt = None

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = (event.x() - self._scroll_contents.x(), event.y() - self._scroll_contents.y())

            col = point[0] // self._pl_wid
            row = point[1] // self._pl_wid

            if col <= self._args.stab_column:
                idx = self._args.stab_column * row + col

                if idx < len(self._args.stab_ucells):
                    self.activate_idx(idx)

                    if idx == len(self._args.stab_ucells) - 1:
                        self.attach_set()

                    else:
                        self.import_set()

                else:
                    self.activate_idx(None)

            else:
                self.activate_idx(None)

            event.accept()

        else:
            event.ignore()

    def dragEnterEvent(self, event):
        # drag file out from depot.
        if self._drag_file:
            event.ignore()
            return

        try:
            depot_file = event.mimeData().urls()[0].toLocalFile()

        except Exception as err:
            event.ignore()
            return

        if depot_file.split(".")[-1].lower() in ("dpc", "json"):
            self._drop_file = depot_file
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if self._drop_file:
            self.ps_dropped.emit((self._drop_file, False))
            self._drop_file = None

            event.accept()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def initialize(self):
        """
        Initialize Depot from self._args.stab_ucells list.
        """

        unit_cells = []

        for cset in self._args.stab_ucells:
            unit_cell = UnitCell(self._scroll_contents, self._args, cset[0], cset[1], cset[2], cset[3], cset[4])
            unit_cells.append(unit_cell)

            self._scroll_grid_layout.addWidget(unit_cell)

        empty_cell = UnitCell(self._scroll_contents, self._args, [None, None, None, None, None], "", "", "", (-1.0, -1.0))
        unit_cells.append(empty_cell)

        self._scroll_grid_layout.addWidget(empty_cell)

        self._args.stab_ucells = unit_cells
        self._current_idx = None

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell._func_tr_()
                unit_cell.update_text()

    def create_menu(self):
        """
        Create a right clicked menu.
        """

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self._menu = QMenu(self)

        self._action_import = QAction(self)
        self._action_import.triggered.connect(self.import_set)
        self._menu.addAction(self._action_import)

        self._action_export = QAction(self)
        self._action_export.triggered.connect(self.export_set)
        self._menu.addAction(self._action_export)

        self._action_delete = QAction(self)
        self._action_delete.triggered.connect(self.delete_set)
        self._menu.addAction(self._action_delete)

        self._action_detail = QAction(self)
        self._action_detail.triggered.connect(self.detail_set)
        self._menu.addAction(self._action_detail)

        self._action_attach = QAction(self)
        self._action_attach.triggered.connect(self.attach_set)
        self._menu.addAction(self._action_attach)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        if self._current_idx == None:
            self._action_import.setDisabled(True)
            self._action_export.setDisabled(True)
            self._action_delete.setDisabled(True)
            self._action_detail.setDisabled(True)
            self._action_attach.setDisabled(True)

        elif self._current_idx == len(self._args.stab_ucells) - 1:
            self._action_import.setDisabled(True)
            self._action_export.setDisabled(True)
            self._action_delete.setDisabled(True)
            self._action_detail.setDisabled(True)
            self._action_attach.setDisabled(False)

        else:
            self._action_import.setDisabled(False)
            self._action_export.setDisabled(False)
            self._action_delete.setDisabled(False)
            self._action_detail.setDisabled(False)
            self._action_attach.setDisabled(True)

        self._menu.exec_(QCursor.pos())

    def activate_idx(self, idx):
        """
        Activate unit cell at idx and set current idx to idx.
        """

        # current idx is None if all unit cells are not selected.
        # current idx is a serial number in range len(self._args.stab_ucells) if any unit cell is selected.
        # firstly deactivate old unit cell at current idx.
        if self._current_idx != None and isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].activated = False
            self._args.stab_ucells[self._current_idx].update()

        # then change current idx to given idx.
        self._current_idx = idx

        if self._current_idx != None:
            self._current_idx = self._current_idx if self._current_idx > 0 else 0
            self._current_idx = self._current_idx if self._current_idx < len(self._args.stab_ucells) -1 else len(self._args.stab_ucells) - 1

        # finally activate new unit cell at current idx.
        if self._current_idx != None and isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].activated = True
            self._args.stab_ucells[self._current_idx].update()

            upp_pos = self._scroll_contents.y() + self._args.stab_ucells[self._current_idx].y()
            low_pos = self._scroll_contents.y() + self._args.stab_ucells[self._current_idx].y() + self._args.stab_ucells[self._current_idx].height()

            if upp_pos <= 0:
                self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].y())

            elif low_pos >= self._scroll_area.height():
                # similar to the expression in func page_end.
                # please modify synchronously if necessary.
                self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].y() + self._pl_wid - self._scroll_area.height())

        status_idx = self._current_idx

        if status_idx == None:
            status_idx = 0

        else:
            status_idx = status_idx + 1

        self.ps_status_changed.emit((self._tot_rows, self._args.stab_column, len(self._args.stab_ucells) - 1, status_idx))

    def move(self, shift_x, shift_y):
        """
        Select unit cell around current idx unit cell (leftward, rightward, uppward and downward).
        """

        if not self.isVisible():
            return

        if self._current_idx == None:
            self.activate_idx(0)

        elif shift_x < 0:
            self.activate_idx(self._current_idx - 1)

        elif shift_x > 0:
            self.activate_idx(self._current_idx + 1)

        elif shift_y < 0:
            self.activate_idx(self._current_idx - self._args.stab_column)

        elif shift_y > 0:
            self.activate_idx(self._current_idx + self._args.stab_column)

    def zoom(self, ratio):
        """
        Increase or decrease columns for display.
        """

        if not self.isVisible():
            return

        stab_column = self._args.stab_column

        if ratio > 1:
            stab_column -= 1

        elif ratio < 1:
            stab_column += 1

        self._args.modify_settings("stab_column", stab_column)

        self.update()

    '''
    def home(self):
        """
        Locate current unit cell.
        """

        if not self.isVisible():
            return

        if self._current_idx == None:
            self._scroll_bar.setValue(0)
            self.update()

        else:
            self.activate_idx(self._current_idx)
        '''

    def home(self):
        """
        Home scroll page.
        """

        if not self.isVisible():
            return

        if self._scroll_bar.value() < self._pl_wid:
            self.activate_idx(0)

        else:
            self._scroll_bar.setValue(0)

        self.update()

    def page_up(self):
        """
        Up scroll page.
        """

        if not self.isVisible():
            return

        self._scroll_bar.setValue(self._scroll_bar.value() - self._scroll_area.height())
        self.update()

    def page_down(self):
        """
        Down scroll page.
        """

        if not self.isVisible():
            return

        self._scroll_bar.setValue(self._scroll_bar.value() + self._scroll_area.height())
        self.update()

    def page_end(self):
        """
        End scroll page.
        """

        if not self.isVisible():
            return

        # similar to the expression in func activate_idx.
        # please modify synchronously if necessary.
        if self._scroll_bar.value() > self._args.stab_ucells[len(self._args.stab_ucells) - 1].y() - self._scroll_area.height():
            self.activate_idx(len(self._args.stab_ucells) - 1)

        else:
            self._scroll_bar.setValue(self._scroll_contents.height())

        self.update()

    def insert_set(self):
        """
        Insert current color set (combine attach_set and import_set funcs).
        """

        if self._current_idx == len(self._args.stab_ucells) - 1:
            self.attach_set()

        else:
            self.import_set()

    def delete_set(self):
        """
        Delete current color set from depot.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)
            self._args.stab_ucells[self._current_idx].close()
            self._args.stab_ucells.pop(self._current_idx)

            self._args.stab_ucells[self._current_idx].activated = True
            self.update()

    def import_set(self):
        """
        Import current color set into color wheel.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)
            self._args.sys_color_set.import_color_set(self._args.stab_ucells[self._current_idx].color_set)
            self._args.hm_rule = self._args.stab_ucells[self._current_idx].hm_rule

            self.ps_update.emit(True)

    def export_set(self):
        """
        Export current color set from depot.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)
            self.ps_export.emit(self._current_idx)

    def detail_set(self):
        """
        Show info of color set (unit cell) at current idx.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        if isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self.activate_idx(self._current_idx)
            self._info.clone_cell(self._args.stab_ucells[self._current_idx])
            self._info.show()

    def attach_set(self):
        """
        Attach current color set into depot.
        """

        if not self.isVisible():
            return

        self.activate_idx(len(self._args.stab_ucells) - 1)

        hsv_set = (self._args.sys_color_set[0].hsv, self._args.sys_color_set[1].hsv, self._args.sys_color_set[2].hsv, self._args.sys_color_set[3].hsv, self._args.sys_color_set[4].hsv)

        unit_cell = UnitCell(self._scroll_contents, self._args, hsv_set, self._args.hm_rule, "", "", (time.time(), time.time()))
        self._scroll_grid_layout.addWidget(unit_cell)

        unit_cell._func_tr_()
        unit_cell.update_text()
        unit_cell.activated = True

        empty_cell = self._args.stab_ucells[len(self._args.stab_ucells) - 1]
        empty_cell.activated = False

        self._args.stab_ucells[len(self._args.stab_ucells) - 1] = unit_cell
        self._args.stab_ucells.append(empty_cell)

        self.update()

    def clean_up(self):
        """
        Delete all unit cells except empty cell.
        """

        for unit_cell in self._args.stab_ucells[:-1]:
            if isinstance(unit_cell, UnitCell):
                unit_cell.close()

        self._args.stab_ucells = self._args.stab_ucells[-1:]
        self._args.stab_ucells[0].activated = False
        self._current_idx = None

        self.update()

    def clipboard_in(self):
        """
        Load depot from clipboard.
        """

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                depot_file = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if depot_file.split(".")[-1].lower() in ("dpc", "json") and os.path.isfile(depot_file):
                    self.ps_dropped.emit((depot_file, False))

        else:
            try:
                color_dict = json.loads(clipboard.text(), encoding='utf-8')

            except Exception as err:
                return

            if isinstance(color_dict, dict) and "type" in color_dict and "palettes" in color_dict:
                if color_dict["type"] == "depot":
                    self.ps_dropped.emit((color_dict, True))

    def clipboard_cur(self, ctp):
        """
        Set the rgb, hsv or hec (hex code) of current color set as the clipboard data by shortcut Ctrl + r, h or c.
        """

        def _func_():
            data = "["

            if self._current_idx == None or self._args.stab_ucells[self._current_idx] == None or self._current_idx >= len(self._args.stab_ucells) - 1:
                for i in (2, 1, 0, 3, 4):
                    color = self._args.sys_color_set[i].getti(ctp)

                    if ctp == "hec":
                        color = "'#{}'".format(color)

                    data += str(color)
                    data += ", "

            else:
                for i in (2, 1, 0, 3, 4):
                    color = getattr(self._args.stab_ucells[self._current_idx].color_set[i], ctp)

                    if ctp == "hec":
                        color = "'#{}'".format(color)

                    else:
                        color = tuple(color)

                    data += str(color)
                    data += ", "

            data = data[:-2] + "]"

            mimedata = QMimeData()
            mimedata.setText(data)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mimedata)

        return _func_

    def update_all(self):
        """
        Update all unit cells and self.
        """

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell.update()

        self.update()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._action_import.setText(self._action_descs[0])
        self._action_export.setText(self._action_descs[1])
        self._action_delete.setText(self._action_descs[2])
        self._action_detail.setText(self._action_descs[3])
        self._action_attach.setText(self._action_descs[4])

        self._info._func_tr_()
        self._info.update_text()

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell._func_tr_()
                unit_cell.update_text()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Depot", "Import"),
            _translate("Depot", "Export"),
            _translate("Depot", "Delete"),
            _translate("Depot", "Detail"),
            _translate("Depot", "Attach"),
        )
