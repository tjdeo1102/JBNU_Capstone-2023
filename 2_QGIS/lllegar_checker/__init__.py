# -*- coding: utf-8 -*-
"""
/***************************************************************************
 lllegarAreaChecker
                                 A QGIS plugin
 This plugin checks illegal areas
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-12-04
        copyright            : (C) 2023 by Capstone(OSK2) / JeonBukNationalUniversity&&LX
        email                : tjdeo1102@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load lllegarAreaChecker class from file lllegarAreaChecker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    import sys
    import os

    # 현재 모듈의 경로를 가져와서 외부 라이브러리 폴더를 추가합니다.
    plugin_dir = os.path.dirname(__file__)
    libs_dir = os.path.join(plugin_dir, 'libs')

    # 외부 라이브러리 폴더를 sys.path에 추가합니다.
    sys.path.append(libs_dir)

    from .lllegar_checker import lllegarAreaChecker

    return lllegarAreaChecker(iface)
