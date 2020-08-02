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

import os
import time
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from clibs.export import export_list, export_text, export_swatch, export_gpl, export_xml
from clibs.color import Color


class Operation(QWidget):
    """
    Operation object based on QWidget. Init a operation in operation.
    """

    ps_create = pyqtSignal(bool)
    ps_locate = pyqtSignal(bool)
    ps_update = pyqtSignal(bool)
    ps_attach = pyqtSignal(bool)
    ps_opened = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init operation.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        operation_grid_layout = QGridLayout(self)
        operation_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        operation_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        # file functional region.
        self._file_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._file_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._file_gbox, 0, 1, 1, 1)

        self.open_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.open_btn, 2, 1, 1, 1)
        self.open_btn.clicked.connect(self.exec_open)

        self.save_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.save_btn, 3, 1, 1, 1)
        self.save_btn.clicked.connect(self.exec_save)

        self.import_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.import_btn, 0, 1, 1, 1)
        self.import_btn.clicked.connect(self.exec_import)

        self.export_btn = QPushButton(self._file_gbox)
        gbox_grid_layout.addWidget(self.export_btn, 1, 1, 1, 1)
        self.export_btn.clicked.connect(self.exec_export)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 4, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 4, 2, 1, 1)

        # view functional region.
        self._view_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._view_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._view_gbox, 1, 1, 1, 1)

        self.create_btn = QPushButton(self._view_gbox)
        gbox_grid_layout.addWidget(self.create_btn, 0, 1, 1, 1)
        self.create_btn.clicked.connect(self.exec_create)

        self.locate_btn = QPushButton(self._view_gbox)
        gbox_grid_layout.addWidget(self.locate_btn, 1, 1, 1, 1)
        self.locate_btn.clicked.connect(self.exec_locate)

        self.attach_btn = QPushButton(self._view_gbox)
        gbox_grid_layout.addWidget(self.attach_btn, 2, 1, 1, 1)
        self.attach_btn.clicked.connect(self.exec_attach)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 145)

    def exec_open(self, value):
        """
        Exec open operation.
        """

        cb_filter = "{} (*.dpc);; {} (*.json)".format(self._file_descs[4], self._file_descs[0])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[5], self._args.usr_color, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self.dp_open(cb_file[0])

    def dp_open(self, depot_file, direct_dict=False):
        """
        Open a color depot file.
        """

        color_dict = {}

        if direct_dict:
            color_dict = depot_file

        else:
            with open(depot_file, "r", encoding='utf-8') as f:
                try:
                    color_dict = json.load(f)

                except Exception as err:
                    self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return

                if not isinstance(color_dict, dict):
                    self.warning(self._operation_errs[2])
                    return

        if "version" in color_dict:
            vid = self._args.check_version_d(color_dict["version"])

            if vid == 0 or vid > 1:
                self.warning(self._operation_errs[3])
                return

        else:
            self.warning(self._operation_errs[4])
            return

        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "depot":
                color_dict = color_dict["palettes"]

            elif color_dict["type"] == "set":
                self.warning(self._operation_errs[15])
                return

            else:
                self.warning(self._operation_errs[11])
                return

        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return

        color_list = []
        finished_errs = []

        try:
            for color_idx in range(len(color_dict)):
                color = color_dict[color_idx]
                hsv_set = []

                try:
                    for i in range(5):
                        if "hsv" in color["color_{}".format(i)]:
                            hsv_set.append(tuple(Color.fmt_hsv(color["color_{}".format(i)]["hsv"]).tolist()))

                        elif "rgb" in color["color_{}".format(i)]:
                            hsv_set.append(tuple(Color.rgb2hsv(color["color_{}".format(i)]["rgb"]).tolist()))

                        elif "hex code" in color["color_{}".format(i)]:
                            hsv_set.append(tuple(Color.hec2hsv(color["color_{}".format(i)]["hex code"]).tolist()))

                        else:
                            finished_errs.append("[id {}] hsv value is not found.".format(color_idx + 1))

                    if "name" in color:
                        cr_name = str(color["name"])

                    else:
                        cr_name = ""

                    if "desc" in color:
                        cr_desc = str(color["desc"])

                    else:
                        cr_desc = ""

                    if "time" in color:
                        cr_time = [float(color["time"][0]), float(color["time"][1])]

                    else:
                        cr_time = (-1.0, -1.0)

                    if len(hsv_set) == 5:
                        if "rule" in color:
                            if color["rule"] in self._args.global_hm_rules:
                                color_list.append((tuple(hsv_set), color["rule"], cr_name, cr_desc, cr_time))

                            else:
                                finished_errs.append("[id {}] unknown rule: {}.".format(color_idx + 1, color["rule"]))

                        else:
                            finished_errs.append("[id {}] rule value is not found.".format(color_idx + 1))

                    else:
                        finished_errs.append("[id {}] colors are not complete.".format(color_idx + 1))

                except Exception as err:
                    finished_errs.append("[id {}] {}".format(color_idx + 1, str(err)))

        except Exception as err:
            self.warning(self._operation_errs[13] + "\n{}\n{}".format(self._operation_errs[17], err))
            return

        if finished_errs:
            self.warning(self._operation_errs[14] + "\n{}\n{}".format(self._operation_errs[17], "; ".join(finished_errs)))

        for unit_cell in self._args.stab_ucells:
            if hasattr(unit_cell, "close"):
                unit_cell.close()

        self._args.stab_ucells = tuple(color_list)
        self.ps_opened.emit(True)

    def exec_save(self, value):
        """
        Exec save operation.
        """

        name = "{}".format(time.strftime("DigiPale_Depot_%Y_%m_%d.dpc", time.localtime()))

        cb_filter = "{} (*.dpc);; {} (*.txt);; {} (*.aco);; {} (*.gpl);; {} (*.xml)".format(self._file_descs[4], self._file_descs[1], self._file_descs[2], self._file_descs[5], self._file_descs[6])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[6], os.sep.join((self._args.usr_color, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self.dp_save(cb_file[0], value)

    def dp_save(self, depot_file, value):
        """
        Save a color depot file.
        """

        # load color set from unit cells, which is different from export.
        color_list = []

        for unit_cell in self._args.stab_ucells[:-1]:
            if unit_cell != None:
                color_list.append((unit_cell.color_set, unit_cell.hm_rule, unit_cell.name, unit_cell.desc, unit_cell.cr_time))

        # process start.
        if depot_file.split(".")[-1].lower() == "dpc":
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "depot"}
            color_dict["palettes"] = export_list(color_list)

            with open(depot_file, "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4)

        elif depot_file.split(".")[-1].lower() == "txt":
            with open(depot_file, "w") as f:
                f.write("# DigitalPalette Color Depot Export\n")
                f.write("# Please refer to website {} for more information.\n".format(self._args.info_main_site))
                f.write("# Version: {}\n".format(self._args.info_version_en))
                f.write("# Total: {}\n\n".format(len(color_list)))
                f.write(export_text(color_list))

        elif depot_file.split(".")[-1].lower() == "aco":
            with open(depot_file, "wb") as f:
                f.write(export_swatch(color_list))

        elif depot_file.split(".")[-1].lower() == "gpl":
            with open(depot_file, "w") as f:
                f.write(export_gpl(color_list))

        elif depot_file.split(".")[-1].lower() == "xml":
            with open(depot_file, "w") as f:
                f.write(export_xml(color_list))

        else:
            self.warning(self._operation_errs[10])

    def exec_import(self, value):
        """
        Exec import operation.
        """

        cb_filter = "{} (*.dps);; {} (*.json)".format(self._file_descs[3], self._file_descs[0])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[0], self._args.usr_color, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self.dp_import(cb_file[0])

    def dp_import(self, set_file, direct_dict=False):
        """
        Import a color set file.
        """

        color_dict = {}

        if direct_dict:
            color_dict = set_file

        else:
            with open(set_file, "r", encoding='utf-8') as f:
                try:
                    color_dict = json.load(f)

                except Exception as err:
                    self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                    return

                if not isinstance(color_dict, dict):
                    self.warning(self._operation_errs[2])
                    return

        if "version" in color_dict:
            vid = self._args.check_version_s(color_dict["version"])

            if vid == 0 or vid > 1:
                self.warning(self._operation_errs[3])
                return

        else:
            self.warning(self._operation_errs[4])
            return

        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "set":
                color_dict = color_dict["palettes"][0]

            elif color_dict["type"] == "depot":
                self.warning(self._operation_errs[16])
                return

            else:
                self.warning(self._operation_errs[11])
                return

        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return

        color_set = []

        for i in range(5):
            if "color_{}".format(i) in color_dict:
                if "hsv" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hsv"]
                        color_set.append(Color(hsv, tp="hsv", overflow=self._args.sys_color_set.get_overflow()))

                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return

                elif "rgb" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["rgb"]
                        color_set.append(Color(hsv, tp="rgb", overflow=self._args.sys_color_set.get_overflow()))

                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return

                elif "hex code" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hex code"]
                        color_set.append(Color(hsv, tp="hec", overflow=self._args.sys_color_set.get_overflow()))

                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return

                else:
                    self.warning(self._operation_errs[6] + "\n{}\n{}".format(self._operation_errs[17], "hsv"))
                    return

            else:
                self.warning(self._operation_errs[7] + "\n{}\n{}".format(self._operation_errs[17], "color_{}".format(i)))
                return

        if "rule" in color_dict:
            if color_dict["rule"] in self._args.global_hm_rules:
                self._args.hm_rule = color_dict["rule"]
                self._args.sys_color_set.import_color_set(color_set)

            else:
                self.warning(self._operation_errs[8] + "\n{}\n{}".format(self._operation_errs[17], color_dict["rule"]))
                return

        else:
            self.warning(self._operation_errs[9] + "\n{}\n{}".format(self._operation_errs[17], "rule"))
            return

        self.ps_update.emit(True)

    def exec_export(self, value):
        """
        Exec export operation.
        """

        name = "{}".format(time.strftime("DigiPale_Set_%Y_%m_%d.dps", time.localtime()))

        cb_filter = "{} (*.dps);; {} (*.txt);; {} (*.aco);; {} (*.gpl);; {} (*.xml)".format(self._file_descs[3], self._file_descs[1], self._file_descs[2], self._file_descs[5], self._file_descs[6])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[1], os.sep.join((self._args.usr_color, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self.dp_export(cb_file[0], value)

    def dp_export(self, set_file, value):
        """
        Export a color set file.
        """

        # load color set from sys or depot, which is different from save.
        color_set = None
        hm_rule = None
        desc = ""

        if isinstance(value, bool):
            color_set = self._args.sys_color_set
            hm_rule = self._args.hm_rule
            cr_name = ""
            cr_desc = ""
            cr_time = (time.time(), time.time())

        else:
            color_set = self._args.stab_ucells[value].color_set
            hm_rule = self._args.stab_ucells[value].hm_rule
            cr_name = self._args.stab_ucells[value].name
            cr_desc = self._args.stab_ucells[value].desc
            cr_time = self._args.stab_ucells[value].cr_time

        color_list = [(color_set, hm_rule, cr_name, cr_desc, cr_time),]

        # process start.
        if set_file.split(".")[-1].lower() == "dps":
            color_dict = {"version": self._args.info_version_en, "site": self._args.info_main_site, "type": "set"}
            color_dict["palettes"] = export_list(color_list)

            with open(set_file, "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4)

        elif set_file.split(".")[-1].lower() == "txt":
            with open(set_file, "w") as f:
                f.write("# DigitalPalette Color Set Export\n")
                f.write("# Please refer to website {} for more information.\n".format(self._args.info_main_site))
                f.write("# Version: {}\n".format(self._args.info_version_en))
                f.write("# Total: {}\n\n".format(len(color_list)))
                f.write(export_text(color_list))

        elif set_file.split(".")[-1].lower() == "aco":
            with open(set_file, "wb") as f:
                f.write(export_swatch(color_list))

        elif set_file.split(".")[-1].lower() == "gpl":
            with open(set_file, "w") as f:
                f.write(export_gpl(color_list))

        elif set_file.split(".")[-1].lower() == "xml":
            with open(set_file, "w") as f:
                f.write(export_xml(color_list))

        else:
            self.warning(self._operation_errs[10])

    def exec_create(self, value):
        """
        Exec create operation.
        """

        self.ps_create.emit(True)

    def exec_locate(self, value):
        """
        Exec loacate operation.
        """

        self.ps_locate.emit(True)

    def exec_attach(self, value):
        """
        Exec attach operation.
        """

        self.ps_attach.emit(True)

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._operation_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._operation_errs[18], QMessageBox.AcceptRole)

        box.exec_()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._file_gbox.setTitle(self._gbox_descs[0])
        self.import_btn.setText(self._operation_descs[0])
        self.export_btn.setText(self._operation_descs[1])
        self.create_btn.setText(self._operation_descs[2])
        self.locate_btn.setText(self._operation_descs[3])
        self.attach_btn.setText(self._operation_descs[4])

        self._view_gbox.setTitle(self._gbox_descs[1])
        self.open_btn.setText(self._operation_descs[5])
        self.save_btn.setText(self._operation_descs[6])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("MainWindow", "File"),
            _translate("MainWindow", "View"),
        )

        self._operation_descs = (
            _translate("MainWindow", "Import"),
            _translate("MainWindow", "Export"),
            _translate("MainWindow", "Create"),
            _translate("MainWindow", "Locate"),
            _translate("MainWindow", "Attach"),
            _translate("MainWindow", "Open"),
            _translate("MainWindow", "Save"),
        )

        self._file_descs = (
            _translate("Operation", "DigiPale Json File"),
            _translate("Operation", "Plain Text File"),
            _translate("Operation", "Adobe Swatch File"),
            _translate("Operation", "DigiPale Set File"),
            _translate("Operation", "DigiPale Depot File"),
            _translate("Operation", "GIMP Palette File"),
            _translate("Operation", "Pencil Palette File"),
        )

        self._operation_errs = (
            _translate("Operation", "Error"),
            _translate("Operation", "Import color file error. Color file is broken."),
            _translate("Operation", "Import color format error. Data is not in dict type."),
            _translate("Operation", "Import color version error. Version does not match."),
            _translate("Operation", "Import color version error. Version does not exist."),
            _translate("Operation", "Import color set error. Color set is broken."),
            _translate("Operation", "Import color set error. HSV tags do not exist."),
            _translate("Operation", "Import color set error. Color tags do not exist."),
            _translate("Operation", "Import harmony rule error. Rule does not match."),
            _translate("Operation", "Import harmony rule error. Rule does not exist."),
            _translate("Operation", "Export Color file error. Extension does not match."),
            _translate("Operation", "Import color type error. Type does not match."),
            _translate("Operation", "Import color type error. Type does not exist."),
            _translate("Operation", "Import color depot error."),
            _translate("Operation", "Import some color sets into depot error. These color sets are discarded."),
            _translate("Operation", "Import color type error. This is a color set file, please use 'Import'."),
            _translate("Operation", "Import color type error. This is a color depot file, please use 'Open'."),
            _translate("Operation", "Detail:"),
            _translate("Operation", "OK"),
        )

        self.main_errs = (
            _translate("Operation", "Could not load settings. Settings file is broken. Old settings file has been backed up as 'settings.json.old'."),
            _translate("Operation", "Could not load settings. Version does not match. Old settings file has been backed up as 'settings.json.old'."),
            _translate("Operation", "Could not load settings. Version does not exist. Old settings file has been backed up as 'settings.json.old'."),
        )
