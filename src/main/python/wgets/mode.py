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

from PyQt5.QtWidgets import QWidget, QCheckBox, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QCoreApplication


class Mode(QWidget):
    """
    Mode object based on QWidget. Init a mode in mode.
    """

    ps_mode_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init mode.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        mode_grid_layout = QGridLayout(self)
        mode_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        mode_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        # display functional region.
        self._display_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._display_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._display_gbox, 0, 1, 1, 1)

        self._cbox_rgb = QCheckBox(self._display_gbox)
        self._cbox_rgb.setText("RGB")
        gbox_grid_layout.addWidget(self._cbox_rgb, 0, 1, 1, 1)
        self._cbox_rgb.stateChanged.connect(self.modify_state("rgb"))

        self._cbox_hsv = QCheckBox(self._display_gbox)
        self._cbox_hsv.setText("HSV")
        gbox_grid_layout.addWidget(self._cbox_hsv, 1, 1, 1, 1)
        self._cbox_hsv.stateChanged.connect(self.modify_state("hsv"))

        self.update_mode()

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 60)

    def modify_state(self, tag):
        """
        Modify stored shown state set by cbox.
        """

        def _func_(state):
            setattr(self._args, "show_{}".format(tag), bool(state))

            self.ps_mode_changed.emit(True)

        return _func_

    def update_mode(self):
        """
        Update mode cbox by self._args.show_rgb and show_hsv.
        """

        self._cbox_rgb.setChecked(self._args.show_rgb)
        self._cbox_hsv.setChecked(self._args.show_hsv)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._display_gbox.setTitle(self._gbox_descs[0])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Mode", "Display"),
        )
