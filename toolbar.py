# Copyright (c) 2020  Lovac42
#           (c) 2021- ijgnd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from aqt import QMenu


def getMenu(parent, menu_name):
    menubar = parent.form.menubar
    for a in menubar.actions():
        if menu_name == a.text():
            return a.parent()
    else:
        return menubar.addMenu(menu_name)


def getAction(parent, actionName):
    menubar = parent.form.menubar
    for a in menubar.actions():
        if actionName == a.text():
            return a
    else:
        return menubar.addAction(actionName)
