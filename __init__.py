# No Distractions Full Screen
# v2.2.3 2/9/2020
# Copyright (c) 2020 Quip13 (random.emailforcrap@gmail.com)
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from aqt.qt import *
from aqt import *
from aqt.reviewer import Reviewer
from anki.hooks import *

#read files
reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
#aqt.utils.showText(str(hide_cursor))
config = mw.addonManager.getConfig(__name__)

#sets up menu to display previous settings
def recheckBoxes():
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    if op == 1:
        mouseover_default.setChecked(True)
    elif op == 0:
        mouseover_hidden.setChecked(True)
    else:
        mouseover_translucent.setChecked(True)
    if cursorIdleTimer >= 0:
        enable_cursor_hide.setChecked(True)

#updates settings on menu action
def user_settings():
    if mouseover_default.isChecked():
        op = 1
    if mouseover_hidden.isChecked():
        op = 0
    if mouseover_translucent.isChecked():
        op = .5
    config['answer_button_opacity'] = op

    if enable_cursor_hide.isChecked():
        cursorIdleTimer = 10000
    if not enable_cursor_hide.isChecked():
        cursorIdleTimer = -1
    config['cursor_idle_timer'] = cursorIdleTimer
    mw.addonManager.writeConfig(__name__, config)

#appends CSS and JS into widgets
def reviewer_wrapper(*args):
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    mw.reviewer.bottom.web.eval(f"var op = {op}; {reformat}")
    mw.reviewer.bottom.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")

#PyQt manipulation
first_time = True
def toggle_full_screen():
        global first_time
        global og_reviewer
        if first_time:
            og_reviewer = Reviewer._initWeb #stores initial reviewer on first toggle
        if not mw.isFullScreen():
            Reviewer._initWeb = wrap(og_reviewer, reviewer_wrapper) #tried to use triggers instead but is called prematurely upon suspend/bury
            mw.showFullScreen()
            mw.reset()
            mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
            mw.toolbar.web.setFixedHeight(0) #Removes Decks Add etc.s
            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            mw.mainLayout.removeWidget(mw.reviewer.bottom.web) #Removes bottom bar from layout (makes it float)

        elif mw.isFullScreen():
            Reviewer._initWeb = og_reviewer #calls initial reviewer
            mw.showNormal()
            mw.reset()
            mw.menuBar().setMaximumHeight(9999)
            mw.toolbar.web.adjustHeightToFit()
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
        first_time = False

# Limits full screen to just review
def stateChange(new_state, *args):
    if new_state == 'review':
        fullscreen.setDisabled(False)
        fullscreen.setText('Toggle Full Screen')
    elif new_state != 'review':
        if mw.isFullScreen():
            toggle_full_screen()
        fullscreen.setDisabled(True)
        fullscreen.setText('Toggle Full Screen (Only during review)')

#end full screen when review ends
addHook("afterStateChange", stateChange)

#add menus
try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(('View'), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(),
        mw.addon_view_menu
    )

mw.submenu = QMenu(('Full Screen'), mw)
mw.addon_view_menu.addMenu(mw.submenu)

fullscreen = QAction('Toggle Full Screen (Only in review)', mw)
fullscreen.triggered.connect(toggle_full_screen)
fullscreen.setShortcut('F11')
fullscreen.setDisabled(True) #re-enabled in stateChange
mw.submenu.addAction(fullscreen)

mw.submenu.addSeparator()

mouseover = QActionGroup(mw)

mouseover_default = QAction('Do Not Hide Answer Buttons', mouseover)
mouseover_default.setCheckable(True)
mw.submenu.addAction(mouseover_default)
mouseover_default.triggered.connect(user_settings)

mouseover_hidden = QAction('Hide Answer Buttons Until Mouseover', mouseover)
mouseover_hidden.setCheckable(True)
mw.submenu.addAction(mouseover_hidden)
mouseover_hidden.triggered.connect(user_settings)

mouseover_translucent = QAction('Translucent Answer Buttons Until Mouseover', mouseover)
mouseover_translucent.setCheckable(True)
mw.submenu.addAction(mouseover_translucent)
mouseover_translucent.triggered.connect(user_settings)

enable_cursor_hide = QAction('Enable Idle Cursor Hide', mw)
enable_cursor_hide.setCheckable(True)
enable_cursor_hide.triggered.connect(user_settings)

try:
    #For Anki v2.1.20 (uses new hook)
    def hide_cursor_hook(handled, msg, context):
        if msg == "cursor_hide":
            QGuiApplication.setOverrideCursor(Qt.BlankCursor)
            return True, None
        elif msg == "cursor_show":
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
            return True, None
        else:
            return handled
    gui_hooks.webview_did_receive_js_message.append(hide_cursor_hook)
except:
    def linkHandler_wrapper(self, url):
        if url == "cursor_hide":
            QGuiApplication.setOverrideCursor(Qt.BlankCursor)
        elif url == "cursor_show":
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
    Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler_wrapper, pos = 'before')

mw.submenu.addSeparator()
mw.submenu.addAction(enable_cursor_hide)

recheckBoxes()
