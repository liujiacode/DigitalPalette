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

import numpy as np


def rotate_point(point, theta):
    """
    Rotate point in anti-clockwise direction. Rotating center is (0, 0), theta is in angle type and r_theta is in radian type.

    Args:
        point (tuple or list): point for rotating.
        theta (int or float): rotating angle (in angle type).

    Returns:
        rotated point.
    """

    r_theta = theta * np.pi / 180
    Rz = np.array([
        [np.cos(r_theta), np.sin(r_theta) * -1],
        [np.sin(r_theta), np.cos(r_theta)     ],
    ])

    pt = Rz.dot(np.array(point))

    return pt

def rotate_point_center(center, point, theta):
    """
    Rotate point in anti-clockwise direction around given center.

    Args:
        center (tuple or list): rotating center.
        point (tuple or list): point for rotating.
        theta (int or float): rotating angle (in angle type).

    Returns:
        rotated point.
    """

    delta_point = np.array(point) - np.array(center)
    rotated_point = rotate_point(delta_point, theta)

    pt = rotated_point + np.array(center)

    return pt

def get_theta(point):
    """
    Get angle between point and x axis in anti-clockwise direction. Center is (0, 0).

    Args:
        point (tuple or list): rotated point.

    Returns:
        rotated theta.
    """

    delta_x = point[0]
    delta_y = point[1]

    if delta_x == 0:
        if delta_y > 0:
            hue = 90
        else:
            hue = 270
    else:
        _hue = np.arctan(delta_y / delta_x) * 180 / np.pi
        if delta_x > 0:
            hue = _hue if _hue > 0 else 360 + _hue
        else:
            hue = _hue + 180

    return hue

def get_theta_center(center, point):
    """
    Get angle between point and x axis in anti-clockwise direction around given center.

    Args:
        center (tuple or list): rotating center.
        point (tuple or list): rotated point.
    
    Returns:
        rotated theta.
    """

    delta_point = np.array(point) - np.array(center)

    hue = get_theta(delta_point)

    return hue

def get_outer_box(center, radius):
    """
    Get outer box of circle with raduis.

    Args:
        center (tuple or list): circle center.
        radius (int or float): circle radius.

    Returns:
        outer box.
    """

    box = np.array((center[0] - radius, center[1] - radius, 2 * radius, 2 * radius))

    return box
