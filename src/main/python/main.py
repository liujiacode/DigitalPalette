# -*- coding: utf-8 -*-

__LICENSE__ = """
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details.
"""

__COPYRIGHT__ = """
Copyright © 2019-2020 by Eigenmiao. All Rights Reserved.
"""

__WEBSITE__ = """
https://github.com/liujiacode/DigitalPalette
"""

__VERSION__ = """
v2.2.10-x1d1s1-pre
"""

__AUTHOR__ = """
Eigenmiao (eigenmiao@outlook.com)
"""

__DATE__ = """
August 23, 2020
"""

import os
import sys
import json
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QMessageBox, QShortcut, QPushButton
from PyQt5.QtCore import QCoreApplication, QUrl, QTranslator, QByteArray, QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QKeySequence
from cguis.design.main_window import Ui_MainWindow
from cguis.resource import view_rc
from clibs.args import Args
from wgets.wheel import Wheel
from wgets.image import Image
from wgets.depot import Depot
from wgets.cube import CubeTable
from wgets.rule import Rule
from wgets.mode import Mode
from wgets.operation import Operation
from wgets.script import Script
from wgets.channel import Channel
from wgets.transformation import Transformation
from wgets.settings import Settings


class DigitalPalette(QMainWindow, Ui_MainWindow):
    """
    DigitalPalette main window framework.
    """

    def __init__(self, resources, sys_argv):
        """
        Init main window.
        """

        super().__init__()
        self.setupUi(self)

        # load args.
        self._args = Args(resources)

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_128.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)
        self.setMinimumSize(640, 480)

        self._setup_workarea()
        self._setup_result()
        self._setup_rule()
        self._setup_mode()
        self._setup_operation()
        self._setup_script()
        self._setup_channel()
        self._setup_transformation()
        self._setup_settings()

        # set dock window integrations.
        self.tabifyDockWidget(self.script_dock_widget, self.operation_dock_widget)
        self.tabifyDockWidget(self.transformation_dock_widget, self.mode_dock_widget)
        self.tabifyDockWidget(self.channel_dock_widget, self.rule_dock_widget)

        # set dock window visibilities.
        self.rule_dock_widget.visibilityChanged.connect(lambda x: self.actionRule.setChecked(self.rule_dock_widget.isVisible()))
        self.channel_dock_widget.visibilityChanged.connect(lambda x: self.actionChannel.setChecked(self.channel_dock_widget.isVisible()))
        self.operation_dock_widget.visibilityChanged.connect(lambda x: self.actionOperation.setChecked(self.operation_dock_widget.isVisible()))
        self.script_dock_widget.visibilityChanged.connect(lambda x: self.actionScript.setChecked(self.script_dock_widget.isVisible()))
        self.mode_dock_widget.visibilityChanged.connect(lambda x: self.actionMode.setChecked(self.mode_dock_widget.isVisible()))
        self.transformation_dock_widget.visibilityChanged.connect(lambda x: self.actionTransformation.setChecked(self.transformation_dock_widget.isVisible()))
        self.result_dock_widget.visibilityChanged.connect(lambda x: self.actionResult.setChecked(self.result_dock_widget.isVisible()))

        # set menu actions.
        self.actionOpen.triggered.connect(self._wget_operation.open_btn.click)
        self.actionSave.triggered.connect(self._wget_operation.save_btn.click)
        self.actionImport.triggered.connect(self._wget_operation.import_btn.click)
        self.actionExport.triggered.connect(self._wget_operation.export_btn.click)
        self.actionQuit.triggered.connect(self.close)

        self.actionCreate.triggered.connect(self._wget_operation.create_btn.click)
        self.actionLocate.triggered.connect(self._wget_operation.locate_btn.click)
        self.actionAttach.triggered.connect(self._wget_operation.attach_btn.click)
        self.actionSettings.triggered.connect(self._wget_settings.showup)

        self.actionWheel.triggered.connect(lambda x: self._inner_create(False)(False))
        self.actionImage.triggered.connect(lambda x: self._inner_locate(False)(False))
        self.actionDepot.triggered.connect(lambda x: self._inner_attach(False)(False))

        self.actionRule.triggered.connect(self._inner_show_or_hide(self.rule_dock_widget))
        self.actionChannel.triggered.connect(self._inner_show_or_hide(self.channel_dock_widget))
        self.actionOperation.triggered.connect(self._inner_show_or_hide(self.operation_dock_widget))
        self.actionScript.triggered.connect(self._inner_show_or_hide(self.script_dock_widget))
        self.actionMode.triggered.connect(self._inner_show_or_hide(self.mode_dock_widget))
        self.actionTransformation.triggered.connect(self._inner_show_or_hide(self.transformation_dock_widget))
        self.actionResult.triggered.connect(self._inner_show_or_hide(self.result_dock_widget))
        self.actionAll.triggered.connect(self._inner_all_show_or_hide)

        self.actionHomepage.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_main_site)))
        self.actionUpdate.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_update_site)))
        self.actionAbout.triggered.connect(lambda x: self._show_about())

        # set main window shortcuts.
        shortcut = QShortcut(QKeySequence("Alt+H"), self)
        shortcut.activated.connect(self.actionHomepage.trigger)
        shortcut = QShortcut(QKeySequence("F1"), self)
        shortcut.activated.connect(self.actionHomepage.trigger)

        shortcut = QShortcut(QKeySequence("Alt+U"), self)
        shortcut.activated.connect(self.actionUpdate.trigger)
        shortcut = QShortcut(QKeySequence("F2"), self)
        shortcut.activated.connect(self.actionUpdate.trigger)

        shortcut = QShortcut(QKeySequence("Alt+B"), self)
        shortcut.activated.connect(self.actionAbout.trigger)
        shortcut = QShortcut(QKeySequence("F3"), self)
        shortcut.activated.connect(self.actionAbout.trigger)

        shortcut = QShortcut(QKeySequence("Alt+O"), self)
        shortcut.activated.connect(self._wget_operation.open_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut.activated.connect(self._wget_operation.open_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+S"), self)
        shortcut.activated.connect(self._wget_operation.save_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self._wget_operation.save_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+I"), self)
        shortcut.activated.connect(self._wget_operation.import_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        shortcut.activated.connect(self._wget_operation.import_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+E"), self)
        shortcut.activated.connect(self._wget_operation.export_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        shortcut.activated.connect(self._wget_operation.export_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+Q"), self)
        shortcut.activated.connect(self.close)
        shortcut = QShortcut(QKeySequence("Esc"), self)
        shortcut.activated.connect(self.close)

        shortcut = QShortcut(QKeySequence("Alt+T"), self)
        shortcut.activated.connect(self._wget_settings.showup)
        shortcut = QShortcut(QKeySequence("`"), self)
        shortcut.activated.connect(self._wget_settings.showup)

        shortcut = QShortcut(QKeySequence("Alt+C"), self)
        shortcut.activated.connect(self._wget_operation.create_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut.activated.connect(self._wget_operation.create_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+L"), self)
        shortcut.activated.connect(self._wget_operation.locate_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        shortcut.activated.connect(self._wget_operation.locate_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+A"), self)
        shortcut.activated.connect(self._wget_operation.attach_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        shortcut.activated.connect(self._wget_operation.attach_btn.click)

        # set cube table shortcuts.
        shortcut = QShortcut(QKeySequence("Shift+R"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_all("rgb"))

        shortcut = QShortcut(QKeySequence("Shift+H"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_all("hsv"))

        shortcut = QShortcut(QKeySequence("Shift+X"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_all("hec"))

        shortcut = QShortcut(QKeySequence("R"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_act("rgb"))

        shortcut = QShortcut(QKeySequence("H"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_act("hsv"))

        shortcut = QShortcut(QKeySequence("X"), self)
        shortcut.activated.connect(self._wget_cube_table.clipboard_act("hec"))

        shortcut = QShortcut(QKeySequence("1"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(2))
        shortcut = QShortcut(QKeySequence("6"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(2))

        shortcut = QShortcut(QKeySequence("2"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(1))
        shortcut = QShortcut(QKeySequence("7"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(1))

        shortcut = QShortcut(QKeySequence("3"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(0))
        shortcut = QShortcut(QKeySequence("8"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(0))

        shortcut = QShortcut(QKeySequence("4"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(3))
        shortcut = QShortcut(QKeySequence("9"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(3))

        shortcut = QShortcut(QKeySequence("5"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(4))
        shortcut = QShortcut(QKeySequence("0"), self)
        shortcut.activated.connect(self._wget_cube_table.active_by_num(4))

        # set transformation shortcuts.
        shortcut = QShortcut(QKeySequence("Up"), self)
        shortcut.activated.connect(self._wget_transformation.move_up)

        shortcut = QShortcut(QKeySequence("Down"), self)
        shortcut.activated.connect(self._wget_transformation.move_down)

        shortcut = QShortcut(QKeySequence("Left"), self)
        shortcut.activated.connect(self._wget_transformation.move_left)

        shortcut = QShortcut(QKeySequence("Right"), self)
        shortcut.activated.connect(self._wget_transformation.move_right)

        shortcut = QShortcut(QKeySequence("Home"), self)
        shortcut.activated.connect(self._wget_transformation.reset_home)

        shortcut = QShortcut(QKeySequence("="), self)
        shortcut.activated.connect(self._wget_transformation.zoom_in)
        shortcut = QShortcut(QKeySequence("+"), self)
        shortcut.activated.connect(self._wget_transformation.zoom_in)
        shortcut = QShortcut(QKeySequence("*"), self)
        shortcut.activated.connect(self._wget_transformation.zoom_in)

        shortcut = QShortcut(QKeySequence("-"), self)
        shortcut.activated.connect(self._wget_transformation.zoom_out)
        shortcut = QShortcut(QKeySequence("_"), self)
        shortcut.activated.connect(self._wget_transformation.zoom_out)
        shortcut = QShortcut(QKeySequence("/"), self)
        shortcut.activated.connect(self._wget_transformation.zoom_out)

        # install translator.
        self._tr = QTranslator()
        self._app = QApplication.instance()
        self._install_translator()

        # focus on wheel.
        self._wget_wheel.setFocus()

        if len(sys_argv) > 1:
            try:
                if sys_argv[1].split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff"):
                    self._inner_locate(False)(False)
                    self._wget_image.open_image(sys_argv[1])

                else:
                    with open(sys_argv[1], "r", encoding='utf-8') as f:
                        color_dict = json.load(f)

                        if isinstance(color_dict, dict) and "type" in color_dict:
                            if color_dict["type"] == "depot":
                                self._inner_attach(False)(False)
                                self._wget_operation.dp_open(sys_argv[1])

                            elif color_dict["type"] == "set":
                                self._wget_operation.dp_import(sys_argv[1])

            except Exception as err:
                pass

        # show args loading errors.
        if self._args.load_settings_failed:
            self._wget_operation.warning(self._wget_operation.main_errs[self._args.load_settings_failed - 1])

        # restore main window state.
        self._default_state = self.saveState()
        self._default_size = self.size()

        if self._args.main_win_state and self._args.main_win_geometry:
            try:
                state = QByteArray.fromBase64(bytes(self._args.main_win_state, 'ascii'))
                self.restoreState(state)

                geometry = QByteArray.fromBase64(bytes(self._args.main_win_geometry, 'ascii'))
                self.restoreGeometry(geometry)

            except Exception as err:
                pass

        self.actionRule.setChecked(self.rule_dock_widget.isVisible())
        self.actionChannel.setChecked(self.channel_dock_widget.isVisible())
        self.actionOperation.setChecked(self.operation_dock_widget.isVisible())
        self.actionScript.setChecked(self.script_dock_widget.isVisible())
        self.actionMode.setChecked(self.mode_dock_widget.isVisible())
        self.actionTransformation.setChecked(self.transformation_dock_widget.isVisible())
        self.actionResult.setChecked(self.result_dock_widget.isVisible())

        # install stylesheet.
        """
        with open(os.sep.join((resources, "styles", "dark", "style.qss"))) as qf:
            self._app.setStyleSheet(qf.read())
        """

    def _setup_workarea(self):
        """
        Setup workarea (wheel, image or depot).
        """

        def _wheel_status(value):
            """
            Show information about wheel behavior in statusbar.
            """

            color_sign = self._color_descs[value[0]] + self._color_descs[value[1] + 10]
            self.statusbar.showMessage(self._status_descs[4].format(color_sign))

        def _image_status(value):
            """
            Show information about image behavior in statusbar.
            """

            if len(value) == 2:
                self.statusbar.showMessage(self._status_descs[1].format(*value))

            elif len(value) == 4:
                self.statusbar.showMessage(self._status_descs[2].format(*value))

            else:
                color_sign = self._color_descs[value[4][0]] + self._color_descs[value[4][1] + 10]
                self.statusbar.showMessage(self._status_descs[5].format(*value[:4], color_sign))

        def _depot_status(value):
            """
            Show information about depot behavior in statusbar.
            """

            self.statusbar.showMessage(self._status_descs[3].format(*value))

        central_widget_grid_layout = QGridLayout(self.central_widget)
        central_widget_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_wheel = Wheel(self.central_widget, self._args)
        self._wget_image = Image(self.central_widget, self._args)
        self._wget_depot = Depot(self.central_widget, self._args)

        self._wget_wheel.ps_status_changed.connect(_wheel_status)
        self._wget_image.ps_status_changed.connect(_image_status)
        self._wget_depot.ps_status_changed.connect(_depot_status)

        self._wget_wheel.show()
        self._wget_image.hide()
        self._wget_depot.hide()

        central_widget_grid_layout.addWidget(self._wget_wheel)
        central_widget_grid_layout.addWidget(self._wget_image)
        central_widget_grid_layout.addWidget(self._wget_depot)

    def _setup_result(self):
        """
        Setup result (cube).
        """

        result_grid_layout = QGridLayout(self.result_dock_contents)
        result_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_cube_table = CubeTable(self.result_dock_contents, self._args)
        result_grid_layout.addWidget(self._wget_cube_table)

        self._wget_wheel.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_wheel.ps_index_changed.connect(lambda x: self._wget_cube_table.update_index())

        self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())

        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_image.update_color_loc())

    def _setup_rule(self):
        """
        Setup rule.
        """

        rule_grid_layout = QGridLayout(self.rule_dock_contents)
        rule_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_rule = Rule(self.rule_dock_contents, self._args)
        rule_grid_layout.addWidget(self._wget_rule)

        self._wget_rule.ps_rule_changed.connect(lambda x: self._wget_cube_table.modify_rule())
        self._wget_image.ps_modify_rule.connect(lambda x: self._wget_rule.update_rule())

    def _setup_mode(self):
        """
        Setup mode.
        """

        mode_grid_layout = QGridLayout(self.mode_dock_contents)
        mode_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_mode = Mode(self.mode_dock_contents, self._args)
        mode_grid_layout.addWidget(self._wget_mode)

        self._wget_mode.ps_mode_changed.connect(lambda x: self._wget_cube_table.modify_box_visibility())

    def _setup_operation(self):
        """
        Setup operation.
        """

        operation_grid_layout = QGridLayout(self.operation_dock_contents)
        operation_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_operation = Operation(self.operation_dock_contents, self._args)
        operation_grid_layout.addWidget(self._wget_operation)

        self._wget_operation.ps_create.connect(self._inner_create(True))
        self._wget_operation.ps_locate.connect(self._inner_locate(True))
        self._wget_operation.ps_attach.connect(self._inner_attach(True))

        self._wget_operation.ps_update.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_operation.ps_update.connect(lambda x: self._wget_rule.update_rule())
        self._wget_operation.ps_opened.connect(lambda x: self._wget_depot.initialize())

        self._wget_depot.ps_update.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_depot.ps_update.connect(lambda x: self._wget_rule.update_rule())
        self._wget_depot.ps_export.connect(self._wget_operation.exec_export)

        self._wget_wheel.ps_dropped.connect(lambda x: self._inner_import(x))
        self._wget_depot.ps_dropped.connect(lambda x: self._inner_open(x))
        self._wget_depot.ps_appended.connect(lambda x: self._inner_append(x))

    def _setup_script(self):
        """
        Setup script.
        """

        script_grid_layout = QGridLayout(self.script_dock_contents)
        script_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_script = Script(self.script_dock_contents, self._args)
        script_grid_layout.addWidget(self._wget_script)

        self._wget_script.ps_filter.connect(lambda x: self._wget_image.open_image("", script=x))
        self._wget_script.ps_crop.connect(self._wget_image.crop_image)
        self._wget_script.ps_freeze.connect(self._wget_image.freeze_image)
        self._wget_script.ps_print.connect(self._wget_image.print_image)
        self._wget_script.ps_extract.connect(self._wget_image.extract_image)

    def _setup_channel(self):
        """
        Setup channel.
        """

        channel_grid_layout = QGridLayout(self.channel_dock_contents)
        channel_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_channel = Channel(self.channel_dock_contents, self._args)
        channel_grid_layout.addWidget(self._wget_channel)

        self._wget_channel.ps_channel_changed.connect(lambda x: self._wget_image.open_category())
        self._wget_image.ps_image_changed.connect(lambda x: self._wget_channel.reset())
        self._wget_image.ps_recover_channel.connect(lambda x: self._wget_channel.recover())

    def _setup_transformation(self):
        """
        Setup transformation.
        """

        transformation_grid_layout = QGridLayout(self.transformation_dock_contents)
        transformation_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_transformation = Transformation(self.transformation_dock_contents, self._args)
        transformation_grid_layout.addWidget(self._wget_transformation)

        self._wget_transformation.ps_home.connect(lambda x: self._wget_image.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_image.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_image.zoom(x, "default"))

        self._wget_transformation.ps_home.connect(lambda x: self._wget_depot.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_depot.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_depot.zoom(x))

        self._wget_transformation.ps_replace.connect(self._wget_image.replace_color)
        self._wget_transformation.ps_enhance.connect(self._wget_image.enhance_image)

    def _setup_settings(self):
        """
        Setup settings.
        """

        def _restore_layout(value):
            """
            Restore to original layout.
            """

            self.restoreState(self._default_state)
            self.resize(self._default_size)

        self._wget_settings = Settings(self, self._args)

        self._wget_settings.ps_rule_changed.connect(lambda x: self._wget_cube_table.modify_rule())
        self._wget_settings.ps_lang_changed.connect(lambda x: self._install_translator())
        self._wget_settings.ps_settings_changed.connect(lambda x: self._inner_update())
        self._wget_settings.ps_clean_up.connect(lambda x: self._wget_depot.clean_up())
        self._wget_settings.ps_restore_layout.connect(_restore_layout)

    def _inner_create(self, act):
        """
        For connection in _setup_operation with create sign.
        """

        def _func_(value):
            if self._wget_wheel.isVisible() and act:
                self._wget_cube_table.create_set()

            else:
                self._wget_wheel.show()
                self._wget_image.hide()
                self._wget_depot.hide()
                # self.statusbar.showMessage(self._status_descs[0])

                if self._args.press_act and act:
                    self._wget_cube_table.create_set()

            self._wget_wheel.setFocus()

        return _func_

    def _inner_locate(self, act):
        """
        For connection in _setup_operation with locate sign.
        """

        def _func_(value):
            if self._wget_image.isVisible() and act:
                self._wget_image.open_image_dialog()

            else:
                self._wget_wheel.hide()
                self._wget_image.show()
                self._wget_depot.hide()
                # self.statusbar.showMessage(self._status_descs[0])

                if self._args.press_act and act:
                    self._wget_image.open_image_dialog()

            self._wget_image.setFocus()

        return _func_

    def _inner_attach(self, act):
        """
        For connection in _setup_operation with attach sign.
        """

        def _func_(value):
            if self._wget_depot.isVisible() and act:
                self._wget_depot.attach_set()

            else:
                self._wget_wheel.hide()
                self._wget_image.hide()
                self._wget_depot.show()
                # self.statusbar.showMessage(self._status_descs[0])

                if self._args.press_act and act:
                    self._wget_depot.attach_set()

            self._wget_depot.setFocus()

        return _func_

    def _inner_update(self):
        """
        Update setable wgets.
        """

        self._args.sys_color_set.set_overflow(self._args.overflow)
        self._args.sys_color_set.set_hsv_ranges(self._args.h_range, self._args.s_range, self._args.v_range)
        self._wget_wheel.update()
        self._wget_image.update_all()
        self._wget_depot.update_all()
        self._wget_cube_table.update_all()
        self._wget_cube_table.modify_box_visibility()
        self._wget_rule.update_rule()
        self._wget_mode.update_mode()

        self.update()

    def _inner_show_or_hide(self, wget):
        """
        Change hidden wget to shown state and change shown wget to hidden state.
        """

        def _func_():
            if wget.isVisible():
                wget.hide()

            else:
                wget.show()

            # self.statusbar.showMessage(self._status_descs[0])

        return _func_

    def _inner_all_show_or_hide(self):
        """
        Change all hidden wget to shown state and change shown wget to hidden state.
        """

        if self.rule_dock_widget.isVisible() and self.channel_dock_widget.isVisible() and self.operation_dock_widget.isVisible() and self.script_dock_widget.isVisible() and self.mode_dock_widget.isVisible() and self.transformation_dock_widget.isVisible() and self.result_dock_widget.isVisible():
            self.rule_dock_widget.hide()
            self.channel_dock_widget.hide()
            self.operation_dock_widget.hide()
            self.script_dock_widget.hide()
            self.mode_dock_widget.hide()
            self.transformation_dock_widget.hide()
            self.result_dock_widget.hide()

        else:
            self.rule_dock_widget.show()
            self.channel_dock_widget.show()
            self.operation_dock_widget.show()
            self.script_dock_widget.show()
            self.mode_dock_widget.show()
            self.transformation_dock_widget.show()
            self.result_dock_widget.show()

        # self.statusbar.showMessage(self._status_descs[0])

    def _inner_open(self, depot_file):
        """
        Open a depot file.
        """

        self._wget_operation.dp_open(depot_file[0], direct_dict=depot_file[1])

        self.update()

    def _inner_import(self, set_file):
        """
        Import a set file.
        """

        self._wget_operation.dp_import(set_file[0], direct_dict=set_file[1])

        self.update()

    def _inner_append(self, set_file):
        """
        Append a set file.
        """

        color_list = self._wget_operation.dp_import(set_file[0], direct_dict=set_file[1], return_set=True)

        # The color list is none if dp_import failed, thus should be discarded.
        # Func attach_set(None) represent add color set from wheel.
        if color_list:
            self._wget_depot.attach_set(color_list=color_list)

        # self.update() is completed by self._wget_depot.attach_set(color_list=color_list) above.
        # self.update()

    def _install_translator(self):
        """
        Translate DigitalPalette interface.
        """

        self._app.removeTranslator(self._tr)

        if self._args.lang != "default":
            lang = os.sep.join((self._args.resources, "langs", self._args.lang))
            self._tr.load(lang)
            self._app.installTranslator(self._tr)

        self._func_tr_()
        self._wget_image._func_tr_()
        self._wget_depot._func_tr_()
        self._wget_rule._func_tr_()
        self._wget_channel._func_tr_()
        self._wget_operation._func_tr_()
        self._wget_transformation._func_tr_()
        self._wget_mode._func_tr_()
        self._wget_script._func_tr_()
        self._wget_settings.retranslateUi(self._wget_settings)
        self._wget_settings._func_tr_()
        self.retranslateUi(self)

        self._wget_depot.update_text()
        self._wget_rule.update_text()
        self._wget_channel.update_text()
        self._wget_operation.update_text()
        self._wget_transformation.update_text()
        self._wget_mode.update_text()
        self._wget_script.update_text()
        self._wget_settings.update_text()

        # set window title.
        if self._args.lang[:2].lower() == "zh":
            self.setWindowTitle("DigitalPalette {}".format("-".join((self._args.info_version_zh.split("-")[0], self._args.info_version_zh.split("-")[2]))))

        else:
            self.setWindowTitle("DigitalPalette {}".format("-".join((self._args.info_version_en.split("-")[0], self._args.info_version_en.split("-")[2]))))

        # set ready status.
        self.setStatusTip(self._status_descs[0])

        self.update()

    def _show_about(self):
        """
        Show DigitalPalette information.
        """

        info = "DigitalPalette\n"
        info += "---------- ---------- ----------\n"

        if self._args.lang[:2].lower() == "zh":
            info += self._info_descs[1].format(self._args.info_version_zh) + "\n"
            info += self._info_descs[2].format(self._args.info_author_zh) + "\n"
            info += self._info_descs[3].format(self._args.info_date_zh) + "\n"

        else:
            info += self._info_descs[1].format(self._args.info_version_en) + "\n"
            info += self._info_descs[2].format(self._args.info_author_en) + "\n"
            info += self._info_descs[3].format(self._args.info_date_en) + "\n"

        info += "---------- ---------- ----------\n"
        info += "{}\n".format(self._info_descs[4])
        info += "---------- ---------- ----------\n"
        info += "{}\n".format(self._info_descs[5])
        info += "---------- ---------- ----------\n"
        info += "{}\n".format(self._info_descs[9])
        info += "---------- ---------- ----------\n"
        info += "{}\n".format(self._info_descs[8].format(QT_VERSION_STR, PYQT_VERSION_STR))

        box = QMessageBox(self)
        box.setWindowTitle(self._info_descs[0])
        box.setText(info)
        box.setIconPixmap(QPixmap(":/images/images/icon_full_128.png"))

        ok_btn = QPushButton()
        ok_btn.setText(self._info_descs[6])
        box.addButton(ok_btn, QMessageBox.RejectRole)
        box.setDefaultButton(ok_btn)

        visit_btn = QPushButton()
        visit_btn.clicked.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_main_site)))
        visit_btn.setText(self._info_descs[7])
        box.addButton(visit_btn, QMessageBox.AcceptRole)

        box.exec_()

    def closeEvent(self, event):
        """
        Actions before close DigitalPalette.
        """

        self._args.main_win_state = bytes(self.saveState().toBase64()).decode("ascii")
        self._args.main_win_geometry = bytes(self.saveGeometry().toBase64()).decode("ascii")

        self._args.save_settings()
        self._args.remove_temp_dir()

        self._wget_wheel.close()
        self._wget_image.close()
        self._wget_depot.close()

        event.accept()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._info_descs = (
            _translate("DigitalPalette", "About"),
            _translate("DigitalPalette", "Version: {}"),
            _translate("DigitalPalette", "Author: {}"),
            _translate("DigitalPalette", "Update: {}"),
            _translate("DigitalPalette", "All Rights Reserved."),
            _translate("DigitalPalette", "DigitalPalette is a free software, which is distributed in the hope that it will be useful, but without any warranty. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License 3.0 (GPL 3.0) for more details."),
            _translate("DigitalPalette", "OK"),
            _translate("DigitalPalette", "Visit Website"),
            _translate("DigitalPalette", "DigitalPalette uses Qt version {} (PyQt version {}) licensed under GNU General Public License. Please see qt.io/licensing for an overview of Qt licensing."),
            _translate("DigitalPalette", "All images (including logo and sample images, etc.), documents and translations in DigitalPalette code repository are licensed under Creative Commons Attribution-NonCommercial-ShareAlike License 4.0 (CC BY-NC-SA 4.0) unless stating additionally."),
        )

        self._status_descs = (
            _translate("DigitalPalette", "Ready."),
            _translate("DigitalPalette", "Image Size: {} x {}."),
            _translate("DigitalPalette", "Image Size: {} x {}. Position: {} %, {} %."),
            _translate("DigitalPalette", "Depot Volume: Row {}, Col {}; Total {}, Index {}."),
            _translate("DigitalPalette", "Current Color: {}."),
            _translate("DigitalPalette", "Image Size: {} x {}. Position: {} %, {} %. Current Color: {}."),
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

        _QColorDialog = (
            _translate("QColorDialog", "Hu&e:"),
            _translate("QColorDialog", "&Sat:"),
            _translate("QColorDialog", "&Val:"),
            _translate("QColorDialog", "&Red:"),
            _translate("QColorDialog", "&Green:"),
            _translate("QColorDialog", "Bl&ue:"),
            _translate("QColorDialog", "A&lpha channel:"),
            _translate("QColorDialog", "&HTML:"),
            _translate("QColorDialog", "Cursor at %1, %2\nPress ESC to cancel"),
            _translate("QColorDialog", "Select Color"),
            _translate("QColorDialog", "&Pick Screen Color"),
            _translate("QColorDialog", "&Basic colors"),
            _translate("QColorDialog", "&Custom colors"),
            _translate("QColorDialog", "&Add to Custom Colors"),
        )

        _QPlatformTheme = (
            _translate("QPlatformTheme", "OK"),
            _translate("QPlatformTheme", "Save"),
            _translate("QPlatformTheme", "Save All"),
            _translate("QPlatformTheme", "Open"),
            _translate("QPlatformTheme", "&Yes"),
            _translate("QPlatformTheme", "Yes to &All"),
            _translate("QPlatformTheme", "&No"),
            _translate("QPlatformTheme", "N&o to All"),
            _translate("QPlatformTheme", "Abort"),
            _translate("QPlatformTheme", "Retry"),
            _translate("QPlatformTheme", "Ignore"),
            _translate("QPlatformTheme", "Close"),
            _translate("QPlatformTheme", "Cancel"),
            _translate("QPlatformTheme", "Discard"),
            _translate("QPlatformTheme", "Help"),
            _translate("QPlatformTheme", "Apply"),
            _translate("QPlatformTheme", "Reset"),
            _translate("QPlatformTheme", "Restore Defaults"),
        )

        _QLineEdit = (
            _translate("QLineEdit", "&Undo"),
            _translate("QLineEdit", "&Redo"),
            _translate("QLineEdit", "Cu&t"),
            _translate("QLineEdit", "&Copy"),
            _translate("QLineEdit", "&Paste"),
            _translate("QLineEdit", "Delete"),
            _translate("QLineEdit", "Select All"),
        )

        _QAbstractSpinBox = (
            _translate("QAbstractSpinBox", "&Select All"),
            _translate("QAbstractSpinBox", "&Step up"),
            _translate("QAbstractSpinBox", "Step &down"),
        )


if __name__ == "__main__":
    appctxt = ApplicationContext()
    DP = DigitalPalette(appctxt.get_resource('.'), sys.argv)
    DP.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
