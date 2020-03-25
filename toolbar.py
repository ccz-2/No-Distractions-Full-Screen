# -*- coding: utf-8 -*-
# Copyright (c) 2020 Lovac42
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from aqt import QMenu

def getMenu(parent, menuName):
    menu = None
    for a in parent.form.menubar.actions():
        if menuName == a.text():
            menu = a.menu()
            break
    if not menu:
        menu = parent.form.menubar.addMenu(menuName)
    return menu


def getSubMenu(menu, subMenuName):
    subMenu = None
    for a in menu.actions():
        if subMenuName == a.text():
            subMenu = a.menu()
            break
    if not subMenu:
        subMenu = QMenu(subMenuName, menu)
        menu.addMenu(subMenu)
    return subMenu