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

import time
import binascii


def export_swatch(color_list):
    """
    Export color set list in swatch type (for Adobe exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time), ...]

    Returns:
        Binary strings.
    """

    swatch_chars_v1 = "0001{:0>4x}".format(len(color_list) * 5)
    swatch_chars_v2 = "0002{:0>4x}".format(len(color_list) * 5)

    for idx in range(len(color_list)):
        for i in (2, 1, 0, 3, 4):
            h, s, v = color_list[idx][0][i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), int(s * 65535), int(v * 65535))
            swatch_chars_v1 += pr_chars

            swatch_chars_v2 += pr_chars

            name = "{}-{}-{}".format(color_list[idx][2], idx, i) if color_list[idx][2] else "DigiPale-{}-{}".format(idx, i)
            swatch_chars_v2 += "0000{:0>4x}".format(len(name) + 1)

            for n in name:
                swatch_chars_v2 += "{:0>4x}".format(ord(n))

            swatch_chars_v2 += "0000"

    swatch_chars = swatch_chars_v1 + swatch_chars_v2

    return binascii.a2b_hex(swatch_chars)

def export_gpl(color_list):
    """
    Export color set list in gpl type (for GIMP exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time), ...]

    Returns:
        Plain text strings.
    """

    gpl_chars = "GIMP Palette\n"

    for idx in range(len(color_list)):
        for i in (2, 1, 0, 3, 4):
            r, g, b = color_list[idx][0][i].rgb
            name = "{}-{}-{}".format(color_list[idx][2], idx, i) if color_list[idx][2] else "DigiPale-{}-{}".format(idx, i)
            gpl_chars += "{:<5}{:<5}{:<5}{}\n".format(r, g, b, name)

    return gpl_chars

def export_xml(color_list):
    """
    Export color set list in xml type (for Pencil exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time), ...]

    Returns:
        Plain text strings.
    """

    xml_chars = "<!DOCTYPE PencilPalette>\n<palette>\n"

    for idx in range(len(color_list)):
        for i in (2, 1, 0, 3, 4):
            r, g, b = color_list[idx][0][i].rgb
            name = "{}-{}-{}".format(color_list[idx][2], idx, i) if color_list[idx][2] else "DigiPale-{}-{}".format(idx, i)
            xml_chars += "    <Colour red='{}' green='{}' blue='{}' alpha='255' name='{}'/>\n".format(r, g, b, name)

    xml_chars += "</palette>\n"

    return xml_chars

def export_text(color_list):
    """
    Export color set list in plain text (for directly reading).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time), ...]

    Returns:
        Plain text strings.
    """

    plain_text = ""

    for idx in range(len(color_list)):
        rule_str = color_list[idx][1]
        rule_str = rule_str[0].upper() + rule_str[1:].lower()

        if color_list[idx][4][0] < 0:
            time_str = "Unknown"

        else:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(color_list[idx][4][0]))

        if color_list[idx][4][1] < 0:
            time_str += "; Unknown"

        else:
            time_str += "; {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(color_list[idx][4][1])))

        name = "{}-{}".format(color_list[idx][2], idx) if color_list[idx][2] else "DigiPale-{}".format(idx)
        plain_text += "# Name: {}\n".format(name)
        plain_text += "# Rule: {}\n".format(rule_str)
        plain_text += "# Time: {}\n".format(time_str)
        plain_text += "{:<8}{:<8}{:<8}{:<8}{:<10}{:<10}{:<10}{:<8}\n".format("# Index", "R", "G", "B", "H", "S", "V", "Hex Code")

        for i in (2, 1, 0, 3, 4):
            r, g, b = color_list[idx][0][i].rgb
            h, s, v = color_list[idx][0][i].hsv
            hex_code = "#{}".format(color_list[idx][0][i].hec)
            plain_text += "  {:<6}{:<8}{:<8}{:<8}{:<10.3f}{:<10.3f}{:<10.3f}{:<8}\n".format(i, r, g, b, h, s, v, hex_code)

        plain_text += "\n"

    return plain_text

def export_list(color_list):
    """
    Export color set list in list type (for DigitalPalette output).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc, cr_time), ...]

    Returns:
        Json List.
    """

    expt_list = []

    for color in color_list:
        color_dict = {"rule": color[1], "name": color[2], "desc": color[3], "time": list(color[4])}

        for i in (2, 1, 0, 3, 4):
            color_dict["color_{}".format(i)] = color[0][i].export()

        expt_list.append(color_dict)

    return expt_list
