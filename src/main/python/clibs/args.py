# -*- coding: utf-8 -*-

import os
import json
import re
import time
from clibs.color_set import ColorSet


class Args(object):
    """
    Args object. Manage setting args.
    """

    def __init__(self, resources):
        """
        Init Args object.
        """

        # global args.
        self.global_hm_rules = (
            "analogous",
            "monochromatic",
            "triad",
            "tetrad",
            "pentad",
            "complementary",
            "shades",
            "custom",
        )

        self.global_overflows = (
            "cutoff",
            "return",
            "repeat",
        )

        self.global_log = True

        # load languages.
        all_langs = (
            "en", "ar", "be", "bg", "ca", "cs", "da", "de", "el", "es", 
            "et", "fi", "fr", "hr", "hu", "is", "it", "iw", "ja", "ko", 
            "lt", "lv", "mk", "nl", "no", "pl", "pt", "ro", "ru", "sh", 
            "sk", "sl", "sq", "sr", "sv", "th", "tr", "uk", "zh",
        )

        lang_paths = [(39, "default"),]

        langs_dir = os.sep.join((resources, "langs"))
        if not os.path.isdir(langs_dir):
            os.makedirs(langs_dir)

        for lang in os.listdir(langs_dir):
            if os.path.isfile(os.sep.join((langs_dir, lang))) and lang.split(".")[-1] == "qm":
                glang = re.split("\.|_|-", lang)[0]

                if glang in all_langs:
                    lang_paths.append((all_langs.index(glang), lang))

        self.lang = "default"
        self.usr_langs = tuple(lang_paths)

        # init settings.
        self.usr_store = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette"))
        self.resources = resources

        self.init_settings()

        # init setable but not initable settings.
        self.stab_ucells = tuple()
        self.stab_column = 3

        # load settings.
        if self.store_loc:
            self.load_settings(os.sep.join((self.resources, "settings.json")))

        else:
            self.load_settings(os.sep.join((self.usr_store, "settings.json")))

        # software informations.
        self.info_main_site = "https://liujiacode.github.io/DigitalPalette"
        self.info_update_site = "https://github.com/liujiacode/DigitalPalette/releases"
        self.info_version_zh = "v2.2.1-开发版"
        self.info_version_en = "v2.2.1-dev"
        self.info_author_zh = "刘佳"
        self.info_author_en = "Jia Liu"
        self.info_date_zh = "2019年12月12日"
        self.info_date_en = "Dec. 12th, 2019"

        # special system settings.
        self.sys_activated_idx = 0
        self.sys_color_set = ColorSet(self.h_range, self.s_range, self.v_range, overflow=self.overflow)
        self.sys_color_set.create(self.hm_rule)

        self.sys_category = 0
        self.sys_channel = 0

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def init_settings(self):
        """
        Init default settings.
        """

        # load default language.
        self.modify_settings("lang", "default")

        # load local store tag.
        self.press_act = False
        self.store_loc = False

        if os.path.isfile(os.sep.join((self.resources, "settings.json"))):
            try:
                with open(os.sep.join((self.resources, "settings.json")), "r") as sf:
                    uss = json.load(sf)

                    if isinstance(uss, dict) and "store_loc" in uss:
                        self.store_loc = bool(uss["store_loc"])

            except:
                pass

        # need verify and mkdirs.
        if self.store_loc:
            self.usr_color = os.sep.join((self.resources, "MyColors"))
            self.usr_image = os.sep.join((self.resources, "samples"))

        else:
            self.usr_color = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette", "MyColors"))
            self.usr_image = os.sep.join((os.path.expanduser('~'), "Pictures"))

        if not os.path.isdir(self.usr_color):
            os.makedirs(self.usr_color)

        if not os.path.isdir(self.usr_image):
            os.makedirs(self.usr_image)

        self.hm_rule = "analogous"
        self.overflow = "return"
        self.press_move = True
        self.show_hsv = True
        self.show_rgb = True

        self.h_range = (0.0, 360.0)
        self.s_range = (0.4, 1.0)
        self.v_range = (0.6, 1.0)

        self.wheel_ratio = 0.8
        self.volum_ratio = 0.8
        self.cubic_ratio = 0.9
        self.coset_ratio = 0.8

        self.s_tag_radius = 0.08
        self.v_tag_radius = 0.08

        self.zoom_step = 1.1
        self.move_step = 5

        self.circle_dist = 10

        self.positive_wid = 3
        self.negative_wid = 2
        self.wheel_ed_wid = 2

        self.positive_color = (80, 80, 80)
        self.negative_color = (200, 200, 200)
        self.wheel_ed_color = (240, 240, 240)

    def save_settings(self):
        """
        Save settings to file.
        """

        settings = {
            "version": self.info_version_en,
            "site": self.info_main_site,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }

        items = (
            "usr_color", "usr_image", "press_act", "store_loc", "hm_rule", "overflow", "lang", "press_move",
            "show_hsv", "show_rgb", "h_range", "s_range", "v_range",
            "wheel_ratio", "volum_ratio", "cubic_ratio", "coset_ratio",
            "s_tag_radius", "v_tag_radius", "zoom_step", "move_step", "circle_dist",
            "positive_wid", "negative_wid", "wheel_ed_wid",
            "positive_color", "negative_color", "wheel_ed_color",
            "stab_column",
        )

        for item in items:
            value = getattr(self, item)
            if isinstance(value, (tuple, list)):
                settings[item] = list(value)

            else:
                settings[item] = value

        stab_ucells = []

        for cslst in self.stab_ucells:
            colors = []

            for i in range(5):
                colors.append([float(x) for x in cslst[0][i]])

            stab_ucells.append([colors, str(cslst[1]), str(cslst[2])])

        settings["stab_ucells"] = stab_ucells

        if self.store_loc:
            with open(os.sep.join((self.resources, "settings.json")), "w") as sf:
                json.dump(settings, sf, indent=4)

        else:
            with open(os.sep.join((self.usr_store, "settings.json")), "w") as sf:
                json.dump(settings, sf, indent=4)

            with open(os.sep.join((self.resources, "settings.json")), "w") as sf:
                json.dump({"store_loc": False}, sf, indent=4)

    def modify_settings(self, item, value):
        items = {
            "usr_color": lambda vl: self.pfmt_path(vl, self.usr_color),
            "usr_image": lambda vl: self.pfmt_path(vl, self.usr_image),
            "press_act": lambda vl: self.pfmt_value(vl, bool, self.press_act),
            "store_loc": lambda vl: self.pfmt_value(vl, bool, self.store_loc),
            "hm_rule": lambda vl: self.pfmt_str_in_list(vl, self.global_hm_rules, self.hm_rule),
            "overflow": lambda vl: self.pfmt_str_in_list(vl, self.global_overflows, self.overflow),
            "lang": lambda vl: self.pfmt_str_in_list(vl, [x[1] for x in self.usr_langs], self.lang),
            "press_move": lambda vl: self.pfmt_value(vl, bool, self.press_move),
            "show_hsv": lambda vl: self.pfmt_value(vl, bool, self.show_hsv),
            "show_rgb": lambda vl: self.pfmt_value(vl, bool, self.show_rgb),
            "h_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 360.0), float, self.h_range),
            "s_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 1.0), float, self.s_range),
            "v_range": lambda vl: self.pfmt_num_pair_in_scope(vl, (0.0, 1.0), float, self.v_range),
            "wheel_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.wheel_ratio),
            "volum_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.volum_ratio),
            "cubic_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.cubic_ratio),
            "coset_ratio": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 1.0), float, self.coset_ratio),
            "s_tag_radius": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 0.2), float, self.s_tag_radius),
            "v_tag_radius": lambda vl: self.pfmt_num_in_scope(vl, (0.0, 0.2), float, self.v_tag_radius),
            "zoom_step": lambda vl: self.pfmt_num_in_scope(vl, (1.0, 10.0), float, self.zoom_step),
            "move_step": lambda vl: self.pfmt_num_in_scope(vl, (1, 100), int, self.move_step),
            "circle_dist": lambda vl: self.pfmt_num_in_scope(vl, (0, 50), int, self.circle_dist),
            "positive_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.positive_wid),
            "negative_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.negative_wid),
            "wheel_ed_wid": lambda vl: self.pfmt_num_in_scope(vl, (0, 20), int, self.wheel_ed_wid),
            "positive_color": lambda vl: self.pfmt_rgb_color(vl, self.positive_color),
            "negative_color": lambda vl: self.pfmt_rgb_color(vl, self.negative_color),
            "wheel_ed_color": lambda vl: self.pfmt_rgb_color(vl, self.wheel_ed_color),
            "stab_column": lambda vl: self.pfmt_num_in_scope(vl, (1, 12), int, self.stab_column),
            "stab_ucells": lambda vl: self.pfmt_stab_ucells(vl),
        }

        if item in items:
            setattr(self, item, items[item](value))

    def load_settings(self, settings_file):
        """
        Modify default settings by user settings.

        Parameters:
          uss - dict. user settings.
        """

        uss = {}
        if os.path.isfile(settings_file):
            try:
                with open(settings_file, "r") as sf:
                    uss = json.load(sf)

            except:
                pass

        if isinstance(uss, dict):
            if "version" in uss:
                if not self.check_version(uss["version"]):
                    uss = {}

            else:
                uss = {}

        else:
            uss = {}

        for item in uss:
            self.modify_settings(item, uss[item])

    # ---------- ---------- ---------- Classmethods ---------- ---------- ---------- #

    def pfmt_path(self, value, default):
        """
        Parse directory path.
        """

        try:
            ans = str(value)

            if os.path.isdir(ans):
                return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_num_pair_in_scope(self, value, scope, dtype, default):
        """
        Parse number pair in scope.
        """

        try:
            ans = (dtype(value[0]), dtype(value[1]))

            if scope[0] <= ans[0] <= scope[1] and scope[0] <= ans[1] <= scope[1] and ans[0] <= ans[1]:
                return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_str_in_list(self, value, lst, default):
        """
        Parse string in list.
        """

        try:
            ans = str(value)

            if ans in lst:
                return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_num_in_scope(self, value, scope, dtype, default):
        """
        Parse number in scope.
        """

        try:
            ans = dtype(value)

            if scope[0] <= ans <= scope[1]:
                return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_value(self, value, dtype, default):
        """
        Parse value in designed dtype.
        """

        try:
            ans = dtype(value)

            return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_rgb_color(self, value, default):
        """
        Parse value in designed color.
        """

        try:
            ans = (int(value[0]), int(value[1]), int(value[2]))

            if 0 <= ans[0] <= 255 and 0 <= ans[2] <= 255 and 0 <= ans[2] <= 255:
                return ans

        except Exception as err:
            if self.global_log:
                print(err)

        return default

    def pfmt_stab_ucells(self, value):
        """
        Parse value in designed color.
        """

        stab_ucells = []

        try:
            for cslst in value:
                colors = []

                for color in cslst[0]:
                    ans = (float(color[0]), float(color[1]), float(color[2]))

                    if 0.0 <= ans[0] <= 360.0 and 0.0 <= ans[2] <= 1.0 and 0.0 <= ans[2] <= 1.0:
                        colors.append(ans)

                    else:
                        break

                hm_rule = str(cslst[1])

                if hm_rule not in self.global_hm_rules:
                    hm_rule = ""

                if len(colors) == 5 and hm_rule:
                    stab_ucells.append((tuple(colors), hm_rule, str(cslst[2])))

        except Exception as err:
            if self.global_log:
                print(err)

        return stab_ucells

    def check_version(self, version):
        """
        Check if version is compatible.
        """

        try:
            for vre in (r"^v2\.[12].*",):
                if re.match(vre, version):
                    return True

        except Exception as err:
            if self.global_log:
                print(err)

        return False