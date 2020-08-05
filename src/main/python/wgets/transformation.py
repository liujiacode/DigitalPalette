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

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QCheckBox, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QCoreApplication
from PyQt5.QtGui import QKeySequence


class Transformation(QWidget):
    """
    Transformation object based on QWidget. Init a transformation in transformation.
    """

    ps_move = pyqtSignal(tuple)
    ps_zoom = pyqtSignal(float)
    ps_home = pyqtSignal(bool)
    ps_replace = pyqtSignal(tuple)
    ps_enhance = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init transformation.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        zoom_grid_layout = QGridLayout(self)
        zoom_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        zoom_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(4)
        scroll_grid_layout.setVerticalSpacing(4)
        scroll_area.setWidget(scroll_contents)

        # move functional region.
        self._move_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._move_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._move_gbox, 0, 1, 1, 1)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↑")
        gbox_grid_layout.addWidget(btn, 0, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_up())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↓")
        gbox_grid_layout.addWidget(btn, 2, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_down())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("←")
        gbox_grid_layout.addWidget(btn, 1, 1, 1, 1)
        btn.clicked.connect(lambda x: self.move_left())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("→")
        gbox_grid_layout.addWidget(btn, 1, 3, 1, 1)
        btn.clicked.connect(lambda x: self.move_right())

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↺")
        gbox_grid_layout.addWidget(btn, 1, 2, 1, 1)
        btn.clicked.connect(lambda x: self.reset_home())

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)

        # zoom functional region.
        self._zoom_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._zoom_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._zoom_gbox, 1, 1, 1, 1)

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("+")
        gbox_grid_layout.addWidget(btn, 0, 1, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_in())

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("–")
        gbox_grid_layout.addWidget(btn, 0, 3, 1, 1)
        btn.clicked.connect(lambda x: self.zoom_out())

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 1, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 4, 1, 1)

        # replace functional region.
        self._replace_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._replace_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._replace_gbox, 3, 1, 1, 1)

        self.ckb_reserve_rep = QCheckBox(self._replace_gbox)
        self.ckb_reserve_rep.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_rep, 0, 1, 1, 3)
        self.ckb_reserve_rep.stateChanged.connect(self.sync_reserve)

        self.lab_extd_rep = QLabel(self._replace_gbox)
        gbox_grid_layout.addWidget(self.lab_extd_rep, 1, 1, 1, 3)

        self.sdr_extd_rep = QSlider(self._replace_gbox)
        self.sdr_extd_rep.setOrientation(Qt.Horizontal)
        self.sdr_extd_rep.setMaximum(1000)
        self.sdr_extd_rep.setSingleStep(5)
        self.sdr_extd_rep.setPageStep(0)
        self.sdr_extd_rep.setTickPosition(QSlider.TicksAbove)
        self.sdr_extd_rep.setTickInterval(200)
        self.sdr_extd_rep.setValue(1000)
        gbox_grid_layout.addWidget(self.sdr_extd_rep, 2, 1, 1, 3)
        self.sdr_extd_rep.valueChanged.connect(self.update_enhance)
        self.sdr_extd_rep.valueChanged.connect(self.sync_extd)

        self.lab_scale = QLabel(self._replace_gbox)
        gbox_grid_layout.addWidget(self.lab_scale, 3, 1, 1, 3)

        self.sdr_scale = QSlider(self._replace_gbox)
        self.sdr_scale.setOrientation(Qt.Horizontal)
        self.sdr_scale.setMaximum(1000)
        self.sdr_scale.setSingleStep(5)
        self.sdr_scale.setPageStep(0)
        self.sdr_scale.setTickPosition(QSlider.TicksAbove)
        self.sdr_scale.setTickInterval(200)
        self.sdr_scale.setValue(1000)
        gbox_grid_layout.addWidget(self.sdr_scale, 4, 1, 1, 3)
        self.sdr_scale.valueChanged.connect(self.update_enhance)

        self.btn_replace_rgb = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_rgb, 5, 1, 1, 3)
        self.btn_replace_rgb.clicked.connect(lambda x: self.ps_replace.emit((1, self.ckb_reserve_rep.isChecked(), self.sdr_extd_rep.value() / 1000, self.sdr_scale.value() / 1000)))

        self.btn_replace_hsv = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_hsv, 6, 1, 1, 3)
        self.btn_replace_hsv.clicked.connect(lambda x: self.ps_replace.emit((2, self.ckb_reserve_rep.isChecked(), self.sdr_extd_rep.value() / 1000, self.sdr_scale.value() / 1000)))

        self.btn_replace_cancel = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_cancel, 7, 1, 1, 3)
        self.btn_replace_cancel.clicked.connect(lambda x: self.ps_replace.emit((0, None, None)))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 8, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 8, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 8, 4, 1, 1)

        # enhance functional region.
        self._enhance_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._enhance_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._enhance_gbox, 2, 1, 1, 1)

        self.lab_link_ehs = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_link_ehs, 0, 1, 1, 3)

        self.ckb_r_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_r_ehs.setText("R")
        self.ckb_r_ehs.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_r_ehs, 1, 1, 1, 1)
        self.ckb_r_ehs.stateChanged.connect(self.uncheck_hsv("ehs"))

        self.ckb_g_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_g_ehs.setText("G")
        self.ckb_g_ehs.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_g_ehs, 1, 2, 1, 1)
        self.ckb_g_ehs.stateChanged.connect(self.uncheck_hsv("ehs"))

        self.ckb_b_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_b_ehs.setText("B")
        self.ckb_b_ehs.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_b_ehs, 1, 3, 1, 1)
        self.ckb_b_ehs.stateChanged.connect(self.uncheck_hsv("ehs"))

        self.ckb_h_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_h_ehs.setText("H")
        self.ckb_h_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_h_ehs, 2, 1, 1, 1)
        self.ckb_h_ehs.stateChanged.connect(self.uncheck_rgb("ehs"))

        self.ckb_s_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_s_ehs.setText("S")
        self.ckb_s_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_s_ehs, 2, 2, 1, 1)
        self.ckb_s_ehs.stateChanged.connect(self.uncheck_rgb("ehs"))

        self.ckb_v_ehs = QCheckBox(self._enhance_gbox)
        self.ckb_v_ehs.setText("V")
        self.ckb_v_ehs.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_v_ehs, 2, 3, 1, 1)
        self.ckb_v_ehs.stateChanged.connect(self.uncheck_rgb("ehs"))

        self.ckb_reserve_enh = QCheckBox(self._enhance_gbox)
        self.ckb_reserve_enh.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_enh, 3, 1, 1, 3)
        self.ckb_reserve_enh.stateChanged.connect(self.sync_reserve)

        self.lab_extd_ehs = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_extd_ehs, 4, 1, 1, 3)

        self.sdr_extd_ehs = QSlider(self._enhance_gbox)
        self.sdr_extd_ehs.setOrientation(Qt.Horizontal)
        self.sdr_extd_ehs.setMaximum(1000)
        self.sdr_extd_ehs.setSingleStep(5)
        self.sdr_extd_ehs.setPageStep(0)
        self.sdr_extd_ehs.setTickPosition(QSlider.TicksAbove)
        self.sdr_extd_ehs.setTickInterval(200)
        self.sdr_extd_ehs.setValue(1000)
        gbox_grid_layout.addWidget(self.sdr_extd_ehs, 5, 1, 1, 3)
        self.sdr_extd_ehs.valueChanged.connect(self.update_enhance)
        self.sdr_extd_ehs.valueChanged.connect(self.sync_extd)

        self.lab_sepr = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_sepr, 6, 1, 1, 3)

        self.sdr_sepr = QSlider(self._enhance_gbox)
        self.sdr_sepr.setOrientation(Qt.Horizontal)
        self.sdr_sepr.setMaximum(1000)
        self.sdr_sepr.setSingleStep(5)
        self.sdr_sepr.setPageStep(0)
        self.sdr_sepr.setTickPosition(QSlider.TicksAbove)
        self.sdr_sepr.setTickInterval(200)
        self.sdr_sepr.setValue(0)
        gbox_grid_layout.addWidget(self.sdr_sepr, 7, 1, 1, 3)
        self.sdr_sepr.valueChanged.connect(self.update_enhance)

        self.lab_fact = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_fact, 8, 1, 1, 3)

        self.sdr_fact = QSlider(self._enhance_gbox)
        self.sdr_fact.setOrientation(Qt.Horizontal)
        self.sdr_fact.setMaximum(1000)
        self.sdr_fact.setSingleStep(5)
        self.sdr_fact.setPageStep(0)
        self.sdr_fact.setTickPosition(QSlider.TicksAbove)
        self.sdr_fact.setTickInterval(200)
        self.sdr_fact.setValue(0)
        gbox_grid_layout.addWidget(self.sdr_fact, 9, 1, 1, 3)
        self.sdr_fact.valueChanged.connect(self.update_enhance)

        self.btn_enhs = QPushButton(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.btn_enhs, 10, 1, 1, 3)
        self.btn_enhs.clicked.connect(self.emit_enhance)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 11, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 11, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 11, 4, 1, 1)

        # inverse functional region.
        self._inverse_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._inverse_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._inverse_gbox, 4, 1, 1, 1)

        self.lab_link_inv = QLabel(self._inverse_gbox)
        gbox_grid_layout.addWidget(self.lab_link_inv, 0, 1, 1, 3)

        self.ckb_r_inv = QCheckBox(self._inverse_gbox)
        self.ckb_r_inv.setText("R")
        self.ckb_r_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_r_inv, 1, 1, 1, 1)
        self.ckb_r_inv.stateChanged.connect(self.uncheck_hsv("inv"))

        self.ckb_g_inv = QCheckBox(self._inverse_gbox)
        self.ckb_g_inv.setText("G")
        self.ckb_g_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_g_inv, 1, 2, 1, 1)
        self.ckb_g_inv.stateChanged.connect(self.uncheck_hsv("inv"))

        self.ckb_b_inv = QCheckBox(self._inverse_gbox)
        self.ckb_b_inv.setText("B")
        self.ckb_b_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_b_inv, 1, 3, 1, 1)
        self.ckb_b_inv.stateChanged.connect(self.uncheck_hsv("inv"))

        self.ckb_h_inv = QCheckBox(self._inverse_gbox)
        self.ckb_h_inv.setText("H")
        self.ckb_h_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_h_inv, 2, 1, 1, 1)
        self.ckb_h_inv.stateChanged.connect(self.uncheck_rgb("inv"))

        self.ckb_s_inv = QCheckBox(self._inverse_gbox)
        self.ckb_s_inv.setText("S")
        self.ckb_s_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_s_inv, 2, 2, 1, 1)
        self.ckb_s_inv.stateChanged.connect(self.uncheck_rgb("inv"))

        self.ckb_v_inv = QCheckBox(self._inverse_gbox)
        self.ckb_v_inv.setText("V")
        self.ckb_v_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_v_inv, 2, 3, 1, 1)
        self.ckb_v_inv.stateChanged.connect(self.uncheck_rgb("inv"))

        self.ckb_reserve_inv = QCheckBox(self._inverse_gbox)
        self.ckb_reserve_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_inv, 3, 1, 1, 3)
        self.ckb_reserve_inv.stateChanged.connect(self.sync_reserve)

        self.btn_invs = QPushButton(self._inverse_gbox)
        gbox_grid_layout.addWidget(self.btn_invs, 4, 1, 1, 3)
        self.btn_invs.clicked.connect(self.emit_inverse)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 5, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 4, 1, 1)

        # cover functional region.
        self._cover_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._cover_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._cover_gbox, 5, 1, 1, 1)

        self.lab_link_cov = QLabel(self._cover_gbox)
        gbox_grid_layout.addWidget(self.lab_link_cov, 0, 1, 1, 3)

        self.ckb_r_cov = QCheckBox(self._cover_gbox)
        self.ckb_r_cov.setText("R")
        self.ckb_r_cov.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_r_cov, 1, 1, 1, 1)
        self.ckb_r_cov.stateChanged.connect(self.uncheck_hsv("cov"))

        self.ckb_g_cov = QCheckBox(self._cover_gbox)
        self.ckb_g_cov.setText("G")
        self.ckb_g_cov.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_g_cov, 1, 2, 1, 1)
        self.ckb_g_cov.stateChanged.connect(self.uncheck_hsv("cov"))

        self.ckb_b_cov = QCheckBox(self._cover_gbox)
        self.ckb_b_cov.setText("B")
        self.ckb_b_cov.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_b_cov, 1, 3, 1, 1)
        self.ckb_b_cov.stateChanged.connect(self.uncheck_hsv("cov"))

        self.ckb_h_cov = QCheckBox(self._cover_gbox)
        self.ckb_h_cov.setText("H")
        self.ckb_h_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_h_cov, 2, 1, 1, 1)
        self.ckb_h_cov.stateChanged.connect(self.uncheck_rgb("cov"))

        self.ckb_s_cov = QCheckBox(self._cover_gbox)
        self.ckb_s_cov.setText("S")
        self.ckb_s_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_s_cov, 2, 2, 1, 1)
        self.ckb_s_cov.stateChanged.connect(self.uncheck_rgb("cov"))

        self.ckb_v_cov = QCheckBox(self._cover_gbox)
        self.ckb_v_cov.setText("V")
        self.ckb_v_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_v_cov, 2, 3, 1, 1)
        self.ckb_v_cov.stateChanged.connect(self.uncheck_rgb("cov"))

        self.ckb_reserve_cov = QCheckBox(self._cover_gbox)
        self.ckb_reserve_cov.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_cov, 3, 1, 1, 3)
        self.ckb_reserve_cov.stateChanged.connect(self.sync_reserve)

        self.btn_cover = QPushButton(self._cover_gbox)
        gbox_grid_layout.addWidget(self.btn_cover, 4, 1, 1, 3)
        self.btn_cover.clicked.connect(self.emit_cover)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 5, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 4, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 60)

    def move_up(self):
        """
        Move image up.
        """

        self.ps_move.emit((0, self._args.move_step * -1))

    def move_down(self):
        """
        Move image down.
        """

        self.ps_move.emit((0, self._args.move_step))

    def move_left(self):
        """
        Move image left.
        """

        self.ps_move.emit((self._args.move_step * -1, 0))

    def move_right(self):
        """
        Move image right.
        """

        self.ps_move.emit((self._args.move_step, 0))

    def reset_home(self):
        self.ps_home.emit(True)

    def zoom_in(self):
        self.ps_zoom.emit(self._args.zoom_step)

    def zoom_out(self):
        self.ps_zoom.emit(1 / self._args.zoom_step)

    def uncheck_rgb(self, name):
        """
        Uncheck all r, g, b boxes for inverse.
        """

        def _func_(state):
            if state:
                getattr(self, "ckb_r_{}".format(name)).setChecked(False)
                getattr(self, "ckb_g_{}".format(name)).setChecked(False)
                getattr(self, "ckb_b_{}".format(name)).setChecked(False)

        return _func_

    def uncheck_hsv(self, name):
        """
        Uncheck all h, s, v boxes for inverse.
        """

        def _func_(state):
            if state:
                getattr(self, "ckb_h_{}".format(name)).setChecked(False)
                getattr(self, "ckb_s_{}".format(name)).setChecked(False)
                getattr(self, "ckb_v_{}".format(name)).setChecked(False)

        return _func_

    def sync_reserve(self, state):
        """
        Sync enhance, inverse and replace reserve boxes.
        """

        if state != self.ckb_reserve_enh.isChecked():
            self.ckb_reserve_enh.setChecked(state)

        if state != self.ckb_reserve_inv.isChecked():
            self.ckb_reserve_inv.setChecked(state)

        if state != self.ckb_reserve_rep.isChecked():
            self.ckb_reserve_rep.setChecked(state)

        if state != self.ckb_reserve_cov.isChecked():
            self.ckb_reserve_cov.setChecked(state)

    def sync_extd(self, value):
        """
        Sync enhance and replace extd sdr.
        """

        if self.sdr_extd_ehs.value() != value:
            self.sdr_extd_ehs.setValue(value)

        if self.sdr_extd_rep.value() != value:
            self.sdr_extd_rep.setValue(value)

    def emit_enhance(self, value):
        """
        Emit enhance.
        """

        region = set()

        if self.ckb_r_ehs.isChecked() or self.ckb_g_ehs.isChecked() or self.ckb_b_ehs.isChecked():
            if self.ckb_r_ehs.isChecked():
                region.add(0)

            if self.ckb_g_ehs.isChecked():
                region.add(1)

            if self.ckb_b_ehs.isChecked():
                region.add(2)

            self.ps_enhance.emit(("enhance_rgb", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve_enh.isChecked(), self.sdr_extd_ehs.value() / 1000))

        elif self.ckb_h_ehs.isChecked() or self.ckb_s_ehs.isChecked() or self.ckb_v_ehs.isChecked():
            if self.ckb_h_ehs.isChecked():
                region.add(0)

            if self.ckb_s_ehs.isChecked():
                region.add(1)

            if self.ckb_v_ehs.isChecked():
                region.add(2)

            self.ps_enhance.emit(("enhance_hsv", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve_enh.isChecked(), self.sdr_extd_ehs.value() / 1000))

    def emit_inverse(self, value):
        """
        Emit inverse.
        """

        region = set()

        if self.ckb_r_inv.isChecked() or self.ckb_g_inv.isChecked() or self.ckb_b_inv.isChecked():
            if self.ckb_r_inv.isChecked():
                region.add(0)

            if self.ckb_g_inv.isChecked():
                region.add(1)

            if self.ckb_b_inv.isChecked():
                region.add(2)

            self.ps_enhance.emit(("inverse_rgb", region, self.ckb_reserve_inv.isChecked()))

        elif self.ckb_h_inv.isChecked() or self.ckb_s_inv.isChecked() or self.ckb_v_inv.isChecked():
            if self.ckb_h_inv.isChecked():
                region.add(0)

            if self.ckb_s_inv.isChecked():
                region.add(1)

            if self.ckb_v_inv.isChecked():
                region.add(2)

            self.ps_enhance.emit(("inverse_hsv", region, self.ckb_reserve_inv.isChecked()))

    def emit_cover(self, value):
        """
        Emit cover.
        """

        region = set()

        if self.ckb_r_cov.isChecked() or self.ckb_g_cov.isChecked() or self.ckb_b_cov.isChecked():
            if self.ckb_r_cov.isChecked():
                region.add(0)

            if self.ckb_g_cov.isChecked():
                region.add(1)

            if self.ckb_b_cov.isChecked():
                region.add(2)

            self.ps_enhance.emit(("cover_rgb", region, self.ckb_reserve_cov.isChecked()))

        elif self.ckb_h_cov.isChecked() or self.ckb_s_cov.isChecked() or self.ckb_v_cov.isChecked():
            if self.ckb_h_cov.isChecked():
                region.add(0)

            if self.ckb_s_cov.isChecked():
                region.add(1)

            if self.ckb_v_cov.isChecked():
                region.add(2)

            self.ps_enhance.emit(("cover_hsv", region, self.ckb_reserve_cov.isChecked()))

    def update_enhance(self):
        """
        Update enhance region.
        """

        self.lab_sepr.setText(self._enhance_descs[1].format(self.sdr_sepr.value() / 10))
        self.lab_fact.setText(self._enhance_descs[2].format(self.sdr_fact.value() / 10))
        self.lab_extd_ehs.setText(self._enhance_descs[6].format(self.sdr_extd_ehs.value() / 10))
        self.lab_extd_rep.setText(self._enhance_descs[6].format(self.sdr_extd_rep.value() / 10))
        self.lab_scale.setText(self._enhance_descs[7].format(self.sdr_scale.value() / 10))

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._move_gbox.setTitle(self._gbox_descs[0])
        self._zoom_gbox.setTitle(self._gbox_descs[1])

        self._replace_gbox.setTitle(self._gbox_descs[2])
        self.ckb_reserve_rep.setText(self._enhance_descs[3])
        self.btn_replace_rgb.setText(self._replace_descs[0])
        self.btn_replace_hsv.setText(self._replace_descs[1])
        self.btn_replace_cancel.setText(self._replace_descs[2])

        self._enhance_gbox.setTitle(self._gbox_descs[3])
        self.lab_link_ehs.setText(self._enhance_descs[0])
        self.ckb_reserve_enh.setText(self._enhance_descs[3])
        self.btn_enhs.setText(self._enhance_descs[4])

        self._inverse_gbox.setTitle(self._gbox_descs[4])
        self.lab_link_inv.setText(self._enhance_descs[0])
        self.ckb_reserve_inv.setText(self._enhance_descs[3])
        self.btn_invs.setText(self._enhance_descs[5])

        self._cover_gbox.setTitle(self._gbox_descs[5])
        self.lab_link_cov.setText(self._enhance_descs[0])
        self.ckb_reserve_cov.setText(self._enhance_descs[3])
        self.btn_cover.setText(self._enhance_descs[8])

        self.update_enhance()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Transformation", "Move"),
            _translate("Transformation", "Zoom"),
            _translate("Transformation", "Replace"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
            _translate("Transformation", "Cover"),
        )

        self._replace_descs = (
            _translate("Transformation", "Replace RGB"),
            _translate("Transformation", "Replace HSV"),
            _translate("Transformation", "Cancel"),
        )

        self._enhance_descs = (
            _translate("Transformation", "Link"),
            _translate("Transformation", "Space - {:.1f}%"),
            _translate("Transformation", "Factor - {:.1f}%"),
            _translate("Transformation", "Reserve Result"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
            _translate("Transformation", "Width - {:.1f}%"),
            _translate("Transformation", "Spread - {:.1f}%"),
            _translate("Transformation", "Cover"),
        )

        self._extend_descs = (
            _translate("Image", "All Images"),
            _translate("Image", "PNG Image"),
            _translate("Image", "BMP Image"),
            _translate("Image", "JPG Image"),
            _translate("Image", "TIF Image"),
        )
