# No Distractions Full Screen
# Made by Quip13 (random.emailforcrap@gmail.com)
# v2.2 2/4/2020

from aqt.qt import *
from aqt import *
from aqt.reviewer import Reviewer
from anki.buildinfo import version
from anki.hooks import *
import time
import types

#read files
reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
config = mw.addonManager.getConfig(__name__)

#sets up menu to display previous settings
def recheckBoxes():
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer (v2.1.20+)']
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
    config['cursor_idle_timer (v2.1.20+)'] = cursorIdleTimer
    mw.addonManager.writeConfig(__name__, config)

#injects CSS and JS into widgets
def reformat_screen(*args):
    config = mw.addonManager.getConfig(__name__) #check config
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer (v2.1.20+)']
    #aqt.utils.showText("Blah" + str(mw.isFullScreen()))
    if mw.isFullScreen():
        mw.reviewer.bottom.web.page().runJavaScript(f"var op = {op}; {reformat}")
        mw.reviewer.bottom.web.page().runJavaScript(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
        mw.reviewer.web.page().runJavaScript(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")

#PyQt manipulation
def toggle_full_screen():
        if not mw.isFullScreen():
            mw.showFullScreen()
            mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
            mw.toolbar.web.setFixedHeight(0) #Removes Decks Add etc.s
            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            mw.mainLayout.removeWidget(mw.reviewer.bottom.web) #Removes bottom bar from layout (makes it float)
            reformat_screen()
        elif mw.isFullScreen():
            mw.showNormal()
            mw.reset()
            mw.menuBar().setMaximumHeight(9999)
            mw.toolbar.web.adjustHeightToFit()
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice

# Limits full screen to just review
def stateChange(new_state, *args):
    if new_state == 'review':
        fullscreen.setDisabled(False)
        fullscreen.setText('Toggle Full Screen')
    elif new_state != 'review':
        if mw.isFullScreen():
            toggle_full_screen()
        fullscreen.setDisabled(True)
        fullscreen.setText('Toggle Full Screen (Only in review)')

#end full screen when review ends
addHook("afterStateChange", stateChange)
#addHook("reset", reformat_screen)
addHook("prepareQA",reformat_screen)

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
fullscreen.setDisabled(True) #re-enabled when state == review
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
recheckBoxes()

#Only works after 2.1.20 due to hook
if int(version.replace(".", "")) >= 2120:
    try:
        mw.submenu.addSeparator()
        mw.submenu.addAction(enable_cursor_hide)

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
        #gui_hooks.state_did_reset.append(reformat_screen)
        #gui_hooks.card_did_render.append(reformat_screen) #hopefully resolves UI not updating on bury/suspend
    except:
        pass