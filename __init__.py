# No Distractions Full Screen
# v3.0 2/27/2020
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
from aqt.webview import AnkiWebView
from aqt.reviewer import Reviewer
from aqt.deckbrowser import DeckBrowser
from anki.hooks import *
from anki.utils import isMac, isWin
import random
#sets up menu to display previous settings
def recheckBoxes():
    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    last_toggle = config['last_toggle']
    onTop = config['stay_on_top']
    fs_shortcut = config['fullscreen_hotkey']
    lock_shortcut = config['lock_answer_bar_hotkey']
    dragLocked = config['answer_bar_locked']

    if op == 1:
        mouseover_default.setChecked(True)
    elif op == 0:
        mouseover_hidden.setChecked(True)
    else:
        mouseover_translucent.setChecked(True)

    if cursorIdleTimer >= 0:
        enable_cursor_hide.setChecked(True)

    if last_toggle == 'windowed':
        windowed.setShortcut(fs_shortcut)
        fullscreen.setShortcut('')
    else:
        fullscreen.setShortcut(fs_shortcut)
        windowed.setShortcut('')

    if onTop:
        keep_on_top.setChecked(True)

    if dragLocked:
        lockDrag.setChecked(True)
    lockDrag.setShortcut(lock_shortcut)

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

def padCardsCallback(height):
    mw.reviewer.web.eval(f"calcPadding({height});")

def padCards():
    mw.reviewer.bottom.web.evalWithCallback('getHeight();', padCardsCallback)

#CSS/JS injection
def reviewer_wrapper(*args):
    reformat = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
    draggable = open(os.path.join(os.path.dirname(__file__), 'draggable.js')).read()
    hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
    pad_cards = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
    interact = open(os.path.join(os.path.dirname(__file__), 'interact.min.js')).read()

    config = mw.addonManager.getConfig(__name__)
    op = config['answer_button_opacity']
    cursorIdleTimer = config['cursor_idle_timer']
    color = config['answer_button_border_color']

    mw.reviewer.bottom.web.eval(interact)
    mw.reviewer.bottom.web.eval(draggable)
    mw.reviewer.bottom.web.eval(f"var op = {op}; var color = '{color}'; {reformat}")
    mw.reviewer.bottom.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")

    mw.reviewer.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
    mw.reviewer.web.eval(pad_cards)

#Passes touchevents (except touchcancel) and mousemovements to bottom; will trigger bottom to grab events
class eventPassThroughFilter(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.bottomActive = False
    def eventFilter(self, obj, event):
        if event.type() in [QEvent.MouseMove, QEvent.TouchBegin, QEvent.TouchEnd, QEvent.TouchUpdate]: #TouchCancel omitted - to be passed to reviewer
            for i in mw.reviewer.bottom.web.findChildren(QWidget): #Need to access underlying QQuickWidget for mouse events
                QApplication.sendEvent(i, event)
            if self.bottomActive:
                return True     
        return False

eventPassThrough = eventPassThroughFilter()


def softwareRendering():
    try:
        software1 = (os.environ["QT_XCB_FORCE_SOFTWARE_OPENGL"] == '1')
    except:
        software1 = False
    try:
        software2 = (os.environ["QT_OPENGL"] =='software')
    except:
        software2 = False
    try:
        software3 = os.environ.get("ANKI_SOFTWAREOPENGL")
    except:
        software3 = False

    if software1 or software2 or software3:
        config = mw.addonManager.getConfig(__name__)
        if config['do_not_show_warnings']:
            return
        msgBox = QMessageBox(QMessageBox.Warning, 'No Distractions Full Screen', 'Software Rendering was detected!\nThis may cause artifacts with the No Distractions Full Screen addon and is not recommended.\nPlease switch to hardware acceleration via Anki Preferences if possible.');
        msgBox.setInformativeText("(If screen is frozen, try resizing the window as a workaround)");
        msgBox.setStandardButtons(QMessageBox.Ok);
        msgBox.setDefaultButton(QMessageBox.Ok);
        doNotShowAgain = QCheckBox('Do not show again')
        msgBox.setCheckBox(doNotShowAgain)
        msgBox.exec();
        if doNotShowAgain.isChecked():
            config['do_not_show_warnings'] = True
            mw.addonManager.writeConfig(__name__, config)

#monkey patched function to disable height adjustment
def adjustHeightToFit_override(*args):
    return

#PyQt manipulation
ndfs_enabled = False
window_flags_set = False
def toggle():
        global ndfs_enabled
        global ndfs_inReview
        global og_adjustHeightToFit
        global og_reviewer
        global config
        global fs_window
        global og_window_flags
        global og_window_state
        global window_flags_set
        config = mw.addonManager.getConfig(__name__)

        mw.setUpdatesEnabled(False)
        if not ndfs_enabled:
            ndfs_enabled = True
            softwareRendering()
            og_adjustHeightToFit = mw.reviewer.bottom.web.adjustHeightToFit
            og_window_state = mw.windowState()
            og_reviewer = Reviewer._initWeb #stores initial reviewer before wrap
            og_window_flags = mw.windowFlags() #stores initial flags

            Reviewer._initWeb = wrap(og_reviewer, reviewer_wrapper) #tried to use triggers instead but is called prematurely upon suspend/bury

            mw.reviewer.bottom.web.adjustHeightToFit = adjustHeightToFit_override #disables adjustheighttofit
            mw.reviewer.bottom.web.setFixedSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX) #resets fixed minimums

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
            fs_layout.addWidget(mw.toolbar.web,0,0)#,Qt.AlignTop) #need to add or breaks (garbagecollected)
            fs_layout.addWidget(mw.reviewer.web,0,0)
            fs_layout.addWidget(mw.reviewer.bottom.web,0,0)
            mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
            mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
            mw.toolbar.web.hide()
            mw.mainLayout.addWidget(fs_window)
            mw.reset()
            if config['cursor_idle_timer'] >= 0:
                mw.installEventFilter(loseFocusEventFilter)

            for i in mw.reviewer.web.findChildren(QWidget): #Stupid Qt workaround to grab events
                i.installEventFilter(eventPassThrough)

        else:
            ndfs_enabled = False
            ndfs_inReview = False
            mw.removeEventFilter(loseFocusEventFilter)
            Reviewer._initWeb = og_reviewer #reassigns initial constructor
            mw.setWindowState(og_window_state)
            mw.reviewer.bottom.web.adjustHeightToFit = og_adjustHeightToFit
            mw.mainLayout.removeWidget(fs_window)
            mw.mainLayout.addWidget(mw.toolbar.web)
            mw.mainLayout.addWidget(mw.reviewer.web)
            mw.mainLayout.addWidget(mw.reviewer.bottom.web)            
            mw.toolbar.web.show()
            mw.menuBar().setMaximumHeight(9999)
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.restoreOverrideCursor() #need to call twice

            mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            for i in mw.reviewer.web.findChildren(QWidget):
                i.removeEventFilter(eventPassThrough)

            if window_flags_set: #helps prevent annoying flickering when toggling
                mw.setWindowFlags(og_window_flags) #reassigns initial flags
                window_flags_set = False
                mw.show()
            mw.reset()

        #def test():
        #    mw.setUpdatesEnabled(True)
        #QTimer.singleShot(0, test);
        pause = config['rendering_pause']
        mw.reviewer.bottom.web.eval(f"setTimeout(function(){{pycmd('NDFSready');}}, {pause});") #waits arbitrary amount before drawing mw to reduce rendering artifacts

ndfs_inReview = False
def updateBottom(*args):
    global ndfs_inReview
    if ndfs_inReview:
        config = mw.addonManager.getConfig(__name__)
        posX = config['answer_bar_posX']
        posY = config['answer_bar_posY']
        mw.reviewer.bottom.web.eval(f"updatePos({posX}, {posY});")
        mw.reviewer.bottom.web.eval("activateHover();")
        padCards()

        if lockDrag.isChecked():
            mw.reviewer.bottom.web.eval("disable_drag();")
        else:
           mw.reviewer.bottom.web.eval("enable_drag();")

        if mw.isFullScreen():
           mw.reviewer.bottom.web.eval("enable_bottomHover();") #enables showing of bottom bar when mouse on bottom

def resetPos():
    config['answer_bar_posX'] = 0
    config['answer_bar_posY']  = 0
    mw.addonManager.writeConfig(__name__, config)

def stateChange(new_state, old_state, *args):
    #print(str(old_state) + " -> " + str(new_state))
    global ndfs_inReview
    global ndfs_enabled
    if 'review' in new_state.lower() and ndfs_enabled:
        ndfs_inReview = True
        mw.reviewer.bottom.web.show()
        updateBottom()
    elif ndfs_enabled:
        ndfs_inReview = False
        mw.reviewer.bottom.web.hide()
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor() #twice still bugs out - needs 4 (?)

def on_context_menu_event(web, menu):
    global ndfs_inReview
    if ndfs_inReview:
        menu.addAction(lockDrag)
    else:
        menu.removeAction(lockDrag)

def toggleBar():
    config = mw.addonManager.getConfig(__name__)
    updateBottom()
    config['answer_bar_locked'] = lockDrag.isChecked()
    mw.addonManager.writeConfig(__name__, config)

#Format changes when not in review
addHook("afterStateChange", stateChange)
addHook("AnkiWebView.contextMenuEvent", on_context_menu_event)
addHook("showQuestion", updateBottom)
addHook("showAnswer", updateBottom)
addHook("revertedCard", updateBottom)

def toggle_full_screen():
    config = mw.addonManager.getConfig(__name__)
    config['last_toggle'] = 'full_screen'
    shortcut = config['fullscreen_hotkey']
    mw.addonManager.writeConfig(__name__, config)
    fullscreen.setShortcut(shortcut)
    windowed.setShortcut('')
    toggle()
    

def toggle_window():
    config = mw.addonManager.getConfig(__name__)
    config['last_toggle'] = 'windowed'
    shortcut = config['fullscreen_hotkey']
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

menu.addSeparator()

lockDrag = QAction('Lock Answer Bar Position', mw)
lockDrag.setCheckable(True)
menu.addAction(lockDrag)
lockDrag.triggered.connect(toggleBar)

reset_bar = QAction('Reset Answer Bar Position', mw)
menu.addAction(reset_bar)
reset_bar.triggered.connect(resetPos)

menu.addSeparator()

enable_cursor_hide = QAction('Enable Idle Cursor Hide', mw)
enable_cursor_hide.setCheckable(True)
enable_cursor_hide.setChecked(True)
menu.addAction(enable_cursor_hide)
enable_cursor_hide.triggered.connect(user_settings)

def linkHandler_wrapper(self, url):
    global posX
    global posY
    if "cursor_hide" in url and ndfs_inReview:
        QGuiApplication.setOverrideCursor(Qt.BlankCursor)
    elif "cursor_show" in url:
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor() #need to call twice
    elif "hover_out" in url and ndfs_inReview:
        mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        eventPassThrough.bottomActive = False
    elif "hover_in" in url:
        mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        eventPassThrough.bottomActive = True
    elif "touchstart" in url:
        eventPassThrough.bottomActive = True
        for i in mw.reviewer.web.findChildren(QWidget):
            QApplication.sendEvent(i, QTouchEvent(QEvent.TouchCancel)) #cancels touchstart event in reviewer
    elif "NDFSready" in url:
        mw.setUpdatesEnabled(True)
    elif "draggable_pos" in url:
        pos = url.split(": ")[1]
        pos = pos.split(", ")
        posX = pos[0]
        posY = pos[1]
        config['answer_bar_posX'] = posX
        config['answer_bar_posY']  = posY
        mw.addonManager.writeConfig(__name__, config)
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
        return False

loseFocusEventFilter = loseFocus()

recheckBoxes()