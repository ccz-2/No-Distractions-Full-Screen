# No Distractions Full Screen
# v2.4 2/10/2020
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
from aqt.reviewer import Reviewer
from anki.hooks import *
from anki.utils import isMac, isWin
import urllib

#read files
reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
pad_cards = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
update = open(os.path.join(os.path.dirname(__file__), 'iframe_update.js')).read()

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

#CSS/JS injection
def reviewer_wrapper(func):
    def _initReviewerWeb(*args):
        func()

        reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
        iframe = open(os.path.join(os.path.dirname(__file__), 'iFrame.js')).read()
        height = mw.reviewer.bottom.web.height() #passed to js to calc card padding
        config = mw.addonManager.getConfig(__name__)
        op = config['answer_button_opacity']
        cursorIdleTimer = config['cursor_idle_timer']
        color = config['answer_button_border_color']
        mw.reviewer.bottom.web.eval(f"{reformat}")
        mw.reviewer.web.eval(f"var height = {height}; {pad_cards}")
    
        mw.reviewer.web.eval(f"var op = {op}; var color = '{color}'; {iframe}") #construct iframe for bottom
        #mw.reviewer.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")

    return _initReviewerWeb

def updateiFrame(html):
    global ndfs_inReview
    if ndfs_enabled:
        update = open(os.path.join(os.path.dirname(__file__), 'iframe_update.js')).read()
        html = urllib.parse.quote(html, safe='') #percent encoding hack so can be passed to js
        mw.reviewer.web.eval(f"var url = `{html}`; {update}")

def udpateBottom(*args):
    mw.reviewer.bottom.web.evalWithCallback("""
        (function(){
             return document.documentElement.outerHTML
         }())
    """, updateiFrame)


#PyQt manipulation
ndfs_enabled = False
def toggle():
        global ndfs_enabled
        global og_reviewer
        global config
        global fs_window
        global og_window_flags
        global og_window_state
        global window_flags_set
        config = mw.addonManager.getConfig(__name__)
        window_flags_set = False

        if not ndfs_enabled:
            ndfs_enabled = True
            og_window_state = mw.windowState()
            og_reviewer = mw.reviewer._initWeb #stores initial reviewer before wrap
            og_window_flags = mw.windowFlags() #stores initial flags

            mw.reviewer._initWeb = reviewer_wrapper(og_reviewer) #tried to use triggers instead but is called prematurely upon suspend/bury
            
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
            fs_layout.addWidget(mw.toolbar.web,1,1) #need to add or breaks (garbagecollected)

            fs_layout.addWidget(mw.reviewer.web,2,1)
            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            fs_layout.addWidget(mw.reviewer.bottom.web,2,1,Qt.AlignBottom)

            mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
            mw.toolbar.web.hide()
            mw.reviewer.bottom.web.hide() #Unhidden in hook

            mw.mainLayout.addWidget(fs_window)
            mw.reset()
            mw.reviewer.web.setFocus()

        else:
            ndfs_enabled = False
            mw.reviewer._initWeb = og_reviewer #reassigns initial constructor
            mw.setWindowState(og_window_state)
            mw.mainLayout.removeWidget(fs_window)
            mw.mainLayout.addWidget(mw.toolbar.web)
            mw.mainLayout.addWidget(mw.reviewer.web)
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)            
            mw.toolbar.web.show()
            mw.menuBar().setMaximumHeight(9999)

            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice

            if window_flags_set: #helps prevent annoying flickering when toggling
                mw.setWindowFlags(og_window_flags) #reassigns initial flags
                mw.show()
            mw.reset()

def stateChange(new_state, old_state, *args):
    #aqt.utils.showText(str(old_state) + " -> " + str(new_state))
    global ndfs_inReview
    if 'review' in new_state.lower() and ndfs_enabled:
        ndfs_inReview = True
        mw.reviewer.bottom.web.hide() #show!
    elif ndfs_enabled:
        ndfs_inReview = False
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor() #need to call twice
        mw.reviewer.bottom.web.hide()

#Format changes when not in review
addHook("afterStateChange", stateChange)
addHook("showQuestion", udpateBottom)
addHook("showAnswer", udpateBottom)

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

def linkHandler_wrapper( self, url): #prob can do something with _old here to avoid throwing so many errors in console, idk
    if "NDFS" in url:
        if 'hide:' in url and ndfs_inReview:
            QGuiApplication.setOverrideCursor(Qt.BlankCursor)
        elif 'show:' in url:
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice
        return

Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler_wrapper, pos = 'before')

menu.addSeparator()
#menu.addAction(enable_cursor_hide)

recheckBoxes()
