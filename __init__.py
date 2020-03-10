# No Distractions Full Screen
# v2.3.5 2/20/2020
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

#aqt.utils.showText(str("test"))

from aqt.qt import *
from aqt import *
from aqt.webview import AnkiWebView
from aqt.reviewer import Reviewer
from anki.hooks import *
from anki.utils import isMac, isWin
import math
#read files
reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
pad_cards = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()

#sets up menu to display previous settings
def recheckBoxes():
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    last_toggle = config['last_toggle']
    onTop = config['stay_on_top']
    shortcut = config['hotkey']

    if op == 1:
        mouseover_default.setChecked(True)
    elif op == 0:
        mouseover_hidden.setChecked(True)
    else:
        mouseover_translucent.setChecked(True)

    if cursorIdleTimer >= 0:
        enable_cursor_hide.setChecked(True)

    if last_toggle == 'windowed':
        windowed.setShortcut(shortcut)
        fullscreen.setShortcut('')
    else:
        fullscreen.setShortcut(shortcut)
        windowed.setShortcut('')

    if onTop == True:
        keep_on_top.setChecked(True)

#updates settings on menu action
def user_settings():
    config = mw.addonManager.getConfig(__name__)
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

    if keep_on_top.isChecked():
        onTop = True
    else:
        onTop = False
    config['stay_on_top'] = onTop

    mw.addonManager.writeConfig(__name__, config)


def resizeEvent_overload(event):
    mw.reviewer.web.resize(mw.size())
    print('hi')

mw.reviewer.web.resizeEvent = resizeEvent_overload

def resizeBottom(*args):
    mw.reviewer.bottom.web.adjustHeightToFit()
    bottomAdjustWidthToFit()

#Adapted from _onHeight in webview.py
def onWidth(qvar):
        if qvar is None:
            return

        scaleFactor = mw.reviewer.bottom.web.zoomFactor()
        if scaleFactor == 1:
            scaleFactor = mw.pm.uiScale()

        width = math.ceil(qvar * scaleFactor)
        mw.reviewer.bottom.web.setFixedWidth(width)

def bottomAdjustWidthToFit():
    mw.reviewer.bottom.web.evalWithCallback('getMinWidth();', onWidth)

#CSS/JS injection
def reviewer_wrapper(*args):
    height = mw.reviewer.bottom.web.height() #passed to js to calc card padding
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    color = config['answer_button_border_color']
    mw.reviewer.bottom.web.eval(f"var op = {op}; var color = '{color}'; {reformat}")
    mw.reviewer.bottom.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(f"var height = {height}; {pad_cards}")

#PyQt manipulation
ndfs_enabled = False
def toggle():
        global ndfs_enabled
        global og_reviewer
        global config
        global fs_window
        global og_window_flags
        global og_window_state
        global og_resizeEvent
        global window_flags_set
        config = mw.addonManager.getConfig(__name__)
        window_flags_set = False

        if not ndfs_enabled:   
            ndfs_enabled = True
            og_resizeEvent = mw.reviewer.web.resizeEvent
            og_window_state = mw.windowState()
            og_reviewer = Reviewer._initWeb #stores initial reviewer before wrap
            og_window_flags = mw.windowFlags() #stores initial flags

            Reviewer._initWeb = wrap(og_reviewer, reviewer_wrapper) #tried to use triggers instead but is called prematurely upon suspend/bury
            
            if config['last_toggle'] == 'full_screen':
                if isMac: #kicks out of OSX maximize
                    mw.showNormal()
                mw.showFullScreen()
            if config['stay_on_top'] and not mw.isFullScreen():
                mw.setWindowFlags(og_window_flags | Qt.WindowStaysOnTopHint)
                window_flags_set = True
                mw.show()

            #Builds new widget for window
            fs_window = QWidget()
            fs_layout = QGridLayout(fs_window)
            fs_layout.setContentsMargins(QMargins(0,0,0,0))
            fs_layout.setSpacing(0)
            fs_layout.addWidget(mw.toolbar.web,1,1)#,Qt.AlignTop) #need to add or breaks (garbagecollected)
            fs_layout.addWidget(mw.reviewer.web,2,1)

            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            fs_layout.addWidget(mw.reviewer.bottom.web,2,1,Qt.AlignBottom)

            #mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
            mw.toolbar.web.hide()

            mw.mainLayout.addWidget(fs_window)

            mw.test =  QDockWidget("hi1")
            mw.test.setWidget(mw.reviewer.bottom.web)
            mw.test.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
            mw.test.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetVerticalTitleBar)
            mw.addDockWidget(Qt.BottomDockWidgetArea, mw.test)

            mw.test.setObjectName('hi1')
            mw.test.setStyleSheet("QDockWidget#"+str(mw.test.objectName())+" {background-color:transparent}")
            #mw.setStyleSheet("QMainWindow::separator{height: 0px;}")
            mw.test.setAttribute(Qt.WA_TranslucentBackground);

            mw.reset()

            if config['cursor_idle_timer'] >= 0:
                mw.installEventFilter(loseFocusEventFilter)
        else:
            ndfs_enabled = False
            mw.removeEventFilter(loseFocusEventFilter)
            Reviewer._initWeb = og_reviewer #reassigns initial constructor
            mw.setWindowState(og_window_state)
            mw.reviewer.web.resizeEvent = og_resizeEvent
            mw.mainLayout.removeWidget(fs_window)
            mw.mainLayout.addWidget(mw.toolbar.web)
            mw.mainLayout.addWidget(mw.reviewer.web)
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)
            mw.removeDockWidget(mw.test)       
            mw.toolbar.web.show()
            mw.menuBar().setMaximumHeight(9999)

            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice

            if window_flags_set: #helps prevent annoying flickering when toggling
                mw.setWindowFlags(og_window_flags) #reassigns initial flags
                mw.show()
            mw.reset()

def stateChange(new_state, old_state, *args):
    #print(str(old_state) + " -> " + str(new_state))
    global ndfs_inReview
    if 'review' in new_state.lower() and ndfs_enabled:
        ndfs_inReview = True
    elif ndfs_enabled:
        ndfs_inReview = False
        mw.reviewer.bottom.web.eval(f"show_mouse('{str(new_state)}');") #resets timers
        mw.reviewer.web.eval(f"show_mouse('{str(new_state)}');")   
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor() #need to call twice

def toggle_full_screen():
    config = mw.addonManager.getConfig(__name__)
    config['last_toggle'] = 'full_screen'
    shortcut = config['hotkey']
    mw.addonManager.writeConfig(__name__, config)
    fullscreen.setShortcut(shortcut)
    windowed.setShortcut('')
    toggle()

def toggle_window():
    config = mw.addonManager.getConfig(__name__)
    config['last_toggle'] = 'windowed'
    shortcut = config['hotkey']
    mw.addonManager.writeConfig(__name__, config)
    windowed.setShortcut(shortcut)
    fullscreen.setShortcut('')
    toggle()

#add menus
try:
    mw.addon_view_menu
except AttributeError:
    mw.addon_view_menu = QMenu(('View'), mw)
    mw.form.menubar.insertMenu(
        mw.form.menuTools.menuAction(),
        mw.addon_view_menu
    )

#Format changes when not in review
addHook("afterStateChange", stateChange)
addHook("showQuestion", resizeBottom)
addHook("showAnswer", resizeBottom)
addHook("revertedCard", resizeBottom)

menu = QMenu(('Full Screen'), mw)
mw.addon_view_menu.addMenu(menu)

display = QActionGroup(mw)

fullscreen = QAction('Toggle Full Screen Mode', display)
fullscreen.triggered.connect(toggle_full_screen)
menu.addAction(fullscreen)

windowed = QAction('Toggle Windowed Mode', display)
windowed.triggered.connect(toggle_window)
menu.addAction(windowed)

keep_on_top = QAction('   Windowed Mode Always On Top', mw)
keep_on_top.setCheckable(True)
menu.addAction(keep_on_top)
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
        if "cursor_hide" in msg and ndfs_inReview:
            QGuiApplication.setOverrideCursor(Qt.BlankCursor)
            return True, None
        elif "cursor_show" in msg:
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
            return True, None
        else:
            return handled
    gui_hooks.webview_did_receive_js_message.append(hide_cursor_hook)
except:
    def linkHandler_wrapper(self, url):
        if "cursor_hide" in url and ndfs_inReview:
            QGuiApplication.setOverrideCursor(Qt.BlankCursor)
        elif "cursor_show" in url:
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
        else:
            origLinkHandler(self, url)
    origLinkHandler = Reviewer._linkHandler
    Reviewer._linkHandler = linkHandler_wrapper #custom wrapper

class loseFocus(QObject):
    def eventFilter(self, obj, event):
        if ndfs_inReview:
            if event.type() in [QEvent.WindowDeactivate, QEvent.HoverLeave]: #Card edit does not trigger these - cursor shown by state change hook
                mw.reviewer.bottom.web.eval(f"show_mouse('{event.type()}');")
                mw.reviewer.web.eval(f"show_mouse('{event.type()}');")     
            elif event.type() == QEvent.WindowActivate:
                mw.reviewer.bottom.web.eval(f"countDown('{event.type()}');")
            #if event.type() not in [77, 129, 173]:
            #    print(event.type())
        return QObject.eventFilter(self, obj, event)

loseFocusEventFilter = loseFocus()

menu.addSeparator()
menu.addAction(enable_cursor_hide)

recheckBoxes()