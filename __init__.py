# No Distractions Full Screen
# v2.3 2/9/2020
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
pad_cards = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
#aqt.utils.showText(str(hide_cursor))
config = mw.addonManager.getConfig(__name__)

#sets up menu to display previous settings
def recheckBoxes():
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    display_mode = config['display_mode']
    onTop = config['stay_on_top']

    if op == 1:
        mouseover_default.setChecked(True)
    elif op == 0:
        mouseover_hidden.setChecked(True)
    else:
        mouseover_translucent.setChecked(True)

    if cursorIdleTimer >= 0:
        enable_cursor_hide.setChecked(True)

    if display_mode == 'windowed':
        windowed.setChecked(True)
    else:
        fs.setChecked(True)
        keep_on_top.setEnabled(False)

    if onTop == True:
        keep_on_top.setChecked(True)

#updates settings on menu action
def user_settings():
    if mouseover_default.isChecked():
        op = 1
    elif mouseover_hidden.isChecked():
        op = 0
    else:
        op = .5
    config['answer_button_opacity'] = op

    if enable_cursor_hide.isChecked():
        cursorIdleTimer = 10000
    else:
        cursorIdleTimer = -1
    config['cursor_idle_timer'] = cursorIdleTimer

    if fs.isChecked():
        display_mode = 'full_screen'
        keep_on_top.setEnabled(False) #greys out windowed options
    else:
        display_mode = 'windowed'
        keep_on_top.setEnabled(True) #greys out windowed options

    config['display_mode'] = display_mode

    if keep_on_top.isChecked():
        onTop = True
    else:
        onTop = False
    config['stay_on_top'] = onTop

    mw.addonManager.writeConfig(__name__, config)

#CSS/JS injection
def reviewer_wrapper(*args):
    height = mw.reviewer.bottom.web.height() #passed to js to calc card padding
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    mw.reviewer.bottom.web.eval(f"var op = {op}; {reformat}")
    mw.reviewer.bottom.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(f"var height = {height}; {pad_cards}")

#PyQt manipulation
first_time = True
ndfs_enabled = False
def toggle_full_screen():
        global first_time
        global ndfs_enabled
        global og_reviewer
        global config
        global fs_window
        global window_flags
        config = mw.addonManager.getConfig(__name__)

        if not ndfs_enabled:
            ndfs_enabled = True
            og_reviewer = Reviewer._initWeb #stores initial reviewer before wrap
            window_flags = mw.windowFlags() #stores initial flags

            Reviewer._initWeb = wrap(og_reviewer, reviewer_wrapper) #tried to use triggers instead but is called prematurely upon suspend/bury
            
            if config['display_mode'] == 'full_screen':
                mw.showFullScreen()
            if config['stay_on_top'] and not mw.isFullScreen():
                mw.setWindowFlags(Qt.WindowStaysOnTopHint)
                mw.show()

            mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.

            #Builds new widget for window
            fs_window = QWidget()
            fs_layout = QGridLayout(fs_window)
            fs_layout.setContentsMargins(QMargins(0,0,0,0))
            fs_layout.setSpacing(0)
            fs_layout.addWidget(mw.reviewer.web,1,1)

            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            fs_layout.addWidget(mw.reviewer.bottom.web,1,1,Qt.AlignBottom)

            mw.toolbar.web.setFixedHeight(0)
            fs_layout.addWidget(mw.toolbar.web,1,1,Qt.AlignTop) #need to add or breaks (garbagecollected)

            mw.mainLayout.addWidget(fs_window)
            mw.reset()
        else:
            ndfs_enabled = False #must be set before reset or endless recursion with statechange hook
            Reviewer._initWeb = og_reviewer #reassigns initial constructor
            mw.showNormal()
            mw.mainLayout.removeWidget(fs_window)
            mw.mainLayout.addWidget(mw.toolbar.web)
            mw.mainLayout.addWidget(mw.reviewer.web)
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)            
            mw.toolbar.web.adjustHeightToFit()
            mw.menuBar().setMaximumHeight(9999)

            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
            mw.setWindowFlags(window_flags) #reassigns initial flags
            mw.show()
            mw.reset()

# Limits full screen to just review
def stateChange(new_state, old_state, *args):
    #aqt.utils.showText(str(new_state) + " " + str(old_state))
    if 'review' in new_state.lower():
        fullscreen.setDisabled(False)
        fullscreen.setText('Toggle Full Screen')
    else:
        if ndfs_enabled:
            toggle_full_screen()
        fullscreen.setDisabled(True)
        fullscreen.setText('Toggle Full Screen (Only during review)')

#end full screen when review ends
addHook("afterStateChange", stateChange)

def esc():
    aqt.utils.showText("hi")
    if ndfs_enabled:
        toggle_full_screen()

#add menus
try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(('View'), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(),
        mw.addon_view_menu
    )

menu = QMenu(('Full Screen'), mw)
mw.addon_view_menu.addMenu(menu)

fullscreen = QAction('Toggle Full Screen (Only in review)', mw)
fullscreen.triggered.connect(toggle_full_screen)
fullscreen.setShortcut('F11')
fullscreen.setDisabled(True) #re-enabled in stateChange
menu.addAction(fullscreen)

display = QActionGroup(mw)
display_menu = QMenu('Display Mode', menu)
menu.addMenu(display_menu)

fs = QAction('Full Screen', display)
fs.setCheckable(True)
fs.setChecked(True)
display_menu.addAction(fs)
fs.triggered.connect(user_settings)

windowed = QAction('Windowed', display)
windowed.setCheckable(True)
display_menu.addAction(windowed)
windowed.triggered.connect(user_settings)

keep_on_top = QAction('    Always On Top', mw)
keep_on_top.setCheckable(True)
display_menu.addAction(keep_on_top)
keep_on_top.triggered.connect(user_settings)


menu.addSeparator()

mouseover = QActionGroup(mw)

mouseover_default = QAction('Do Not Hide Answer Buttons', mouseover)
mouseover_default.setCheckable(True)
menu.addAction(mouseover_default)
mouseover_default.setChecked(True)
mouseover_default.triggered.connect(user_settings)

mouseover_hidden = QAction('Hide Answer Buttons Until Mouseover', mouseover)
mouseover_hidden.setCheckable(True)
menu.addAction(mouseover_hidden)
mouseover_hidden.triggered.connect(user_settings)

mouseover_translucent = QAction('Translucent Answer Buttons Until Mouseover', mouseover)
mouseover_translucent.setCheckable(True)
menu.addAction(mouseover_translucent)
mouseover_translucent.triggered.connect(user_settings)

enable_cursor_hide = QAction('Enable Idle Cursor Hide', mw)
enable_cursor_hide.setCheckable(True)
enable_cursor_hide.setChecked(True)
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

menu.addSeparator()
menu.addAction(enable_cursor_hide)

recheckBoxes()
