# No Distractions Full Screen
# v3.2.2 3/3/2020
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
from aqt.reviewer import Reviewer
from aqt.qt import *
from aqt import *
from aqt.webview import AnkiWebView
from aqt.deckbrowser import DeckBrowser
from anki.hooks import *
from anki.utils import isMac, isWin

########## Wrappers ##########
#monkey patched function to disable height adjustment
def adjustHeightToFit_override(*args):
    return

#CSS/JS injection
def reviewer_wrapper(func):
    NDFullScreen = open(os.path.join(os.path.dirname(__file__), 'NDFullScreen.js')).read()
    draggable = open(os.path.join(os.path.dirname(__file__), 'draggable.js')).read()
    hide_cursor = open(os.path.join(os.path.dirname(__file__), 'hide_cursor.js')).read()
    card_padding = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
    interact = open(os.path.join(os.path.dirname(__file__), 'interact.min.js')).read()
    def _initReviewerWeb(*args):
        config = mw.addonManager.getConfig(__name__)
        op = config['answer_button_opacity']
        cursorIdleTimer = config['cursor_idle_timer']
        color = config['answer_button_border_color']
        func()
        mw.reviewer.bottom.web.eval(interact)
        mw.reviewer.bottom.web.eval(draggable)
        mw.reviewer.bottom.web.eval(f"var op = {op}; var color = '{color}'; {NDFullScreen}")
        mw.reviewer.bottom.web.eval(f"var cursorIdleTimer = {cursorIdleTimer}; {hide_cursor}")
        mw.reviewer.web.eval(card_padding)
    return _initReviewerWeb

def linkHandler_wrapper(self, url):
    global posX
    global posY
    if "NDFS-cursor_hide" == url and ndfs_inReview:
        QGuiApplication.setOverrideCursor(Qt.BlankCursor)
    elif "NDFS-cursor_show" == url:
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.restoreOverrideCursor() #need to call twice
    elif "NDFS-hover_out" == url and ndfs_inReview:
        mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        reviewer_eventFilter_obj.bottomActive = False
    elif "NDFS-hover_in" == url:
        mw.reviewer.bottom.web.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        reviewer_eventFilter_obj.bottomActive = True
    elif "NDFS-touchstart" == url:
        reviewer_eventFilter_obj.bottomActive = True
        touchCancelEvent = QTouchEvent(QEvent.TouchCancel)
        touchCancelEvent.NDFS = True #flags event so that it is only sent to reviewer in eventListener
        QApplication.sendEvent(reviewer_QWidget, touchCancelEvent) #cancels initial touchstart event in reviewer, since further touch events are passed to bottom only
    elif "NDFS-draggable_pos" in url:
        pos = url.split(": ")[1]
        pos = pos.split(", ")
        posX = pos[0]
        posY = pos[1]
        config = mw.addonManager.getConfig(__name__)
        config['answer_bar_posX'] = posX
        config['answer_bar_posY']  = posY
        mw.addonManager.writeConfig(__name__, config)
    else:
        origLinkHandler(self, url)
origLinkHandler = Reviewer._linkHandler
Reviewer._linkHandler = linkHandler_wrapper





########## PyQt manipulation ##########
def setupWeb(): #can be accomplished by just calling mw.reset(), but this also cycles to next card, since Reviewer.shwow() calls nextCard()
    if mw.state == 'review':
        try:
            reviewState = mw.reviewer.state
            mw.reviewer._initWeb()
            mw.reviewer._showQuestion()
            if reviewState == 'answer':
                try:
                    mw.reviewer._showAnswer() #breaks on fill in the blank cards
                except:
                    pass
            stateChange('NDFS_review', None) #call statechange hook as if was reset
        except:
            mw.reset() #failsafe
    else:
        mw.reset()

ndfs_enabled = False
ndfs_inReview = False

def toggle():
        global ndfs_enabled
        global ndfs_inReview
        global og_adjustHeightToFit
        global og_reviewer
        global og_window_flags
        global og_window_state
        global window_flags_set
        global fs_window
        config = mw.addonManager.getConfig(__name__)

        if not ndfs_enabled:
            ndfs_enabled = True
            window_flags_set = False
            checkSoftwareRendering()
            og_adjustHeightToFit = mw.reviewer.bottom.web.adjustHeightToFit
            og_window_state = mw.windowState()
            og_window_flags = mw.windowFlags() #stores initial flags
            og_reviewer = mw.reviewer._initWeb #stores initial reviewer before wrap
            
            if config['last_toggle'] == 'full_screen':
                if isMac: #kicks out of OSX maximize
                    mw.showNormal()
                mw.showFullScreen()
            if config['stay_on_top'] and not mw.isFullScreen():
                mw.setWindowFlags(og_window_flags | Qt.WindowStaysOnTopHint)
                window_flags_set = True
                mw.show()
            mw.setUpdatesEnabled(False) #pauses updates to screen
            mw.reviewer._initWeb = reviewer_wrapper(og_reviewer) #tried to use triggers instead but is called prematurely upon suspend/bury
            mw.reviewer.bottom.web.adjustHeightToFit = adjustHeightToFit_override #disables adjustheighttofit
            mw.reviewer.bottom.web.setFixedSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX) #resets fixed minimums

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
            setupWeb()
            setupEventFilters()
            if config['cursor_idle_timer'] >= 0:
                mw.installEventFilter(loseFocusEventFilter)
            if config['ignore_scroll_on_answer_buttons']:
                bottom_QWidget.installEventFilter(bottom_eventFilter_obj)
            reviewer_QWidget.installEventFilter(reviewer_eventFilter_obj)

        else:
            ndfs_enabled = False
            ndfs_inReview = False
            if window_flags_set: #helps prevent annoying flickering when toggling
                mw.setWindowFlags(og_window_flags) #reassigns initial flags
                window_flags_set = False
                mw.show()
            mw.setUpdatesEnabled(False) #pauses updates to screen

            mw.reviewer._initWeb = og_reviewer #reassigns initial constructor
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

            mw.removeEventFilter(loseFocusEventFilter)
            reviewer_QWidget.removeEventFilter(reviewer_eventFilter_obj)
            bottom_QWidget.removeEventFilter(bottom_eventFilter_obj)

            setupWeb()

        delay = config['rendering_delay']
        def unpause():
            mw.setUpdatesEnabled(True)
        QTimer.singleShot(delay, unpause)

def updateBottom(*args):
    if ndfs_inReview:
        config = mw.addonManager.getConfig(__name__)
        posX = config['answer_bar_posX']
        posY = config['answer_bar_posY']
        mw.reviewer.bottom.web.eval(f"updatePos({posX}, {posY});")
        mw.reviewer.bottom.web.eval("activateHover();")
        padCards()
        setLock()
        if mw.isFullScreen():
           mw.reviewer.bottom.web.eval("enable_bottomHover();") #enables showing of bottom bar when mouse on bottom

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

def padCards():
    def padCardsCallback(height):
        mw.reviewer.web.eval(f"calcPadding({height});")
    mw.reviewer.bottom.web.evalWithCallback('getHeight();', padCardsCallback)

def checkSoftwareRendering():
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





########## EventFilters ##########
def setupEventFilters(): #if called too soon will throw error on linux machines
    global reviewer_QWidget
    global bottom_eventFilter_obj
    global bottom_QWidget
    global reviewer_eventFilter_obj
    reviewer_QWidget = mw.reviewer.web.focusProxy()
    bottom_eventFilter_obj = bottom_eventFilter(reviewer_QWidget)
    bottom_QWidget = mw.reviewer.bottom.web.focusProxy()
    reviewer_eventFilter_obj = reviewer_eventFilter(bottom_QWidget)

#Intercepts events on reviewer for routing (touch handling + mouse hover events)
class reviewer_eventFilter(QObject):
    def __init__(self, bottomQWidget):
        QObject.__init__(self)
        self.bottomActive = False
        self.bottom_QWidget = bottomQWidget
    def eventFilter(self, obj, event):
        if event.type() == QEvent.TouchCancel and hasattr(event, 'NDFS'): #checks tag to see if event is sent by linkhandler
            return False #event only sent to reviewer
        if event.type() in [QEvent.MouseMove, QEvent.TouchBegin, QEvent.TouchEnd, QEvent.TouchUpdate, QEvent.TouchCancel]: #mousemove event will trigger js hover event
            QApplication.sendEvent(self.bottom_QWidget, event) #bottom gets event
            if self.bottomActive:
                return True #event only sent to bottom
        return False #event is sent to reviewer


#Intercepts events on bottom for routing (passes scrolling to bottom)
class bottom_eventFilter(QObject):
    def __init__(self, reviewerQWidget):
        QObject.__init__(self)
        self.reviewer_QWidget = reviewerQWidget
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            QApplication.sendEvent(self.reviewer_QWidget, event) #reviewer gets event
            return True #event is only sent to reviewer
        return False #event is only sent to bottom

#Intercepts events to detect when focus is lost to show mouse cursor
class loseFocus(QObject):
    def eventFilter(self, obj, event):
        if ndfs_inReview:
            if event.type() in [QEvent.WindowDeactivate, QEvent.HoverLeave]: #Card edit does not trigger these - cursor shown by state change hook
                mw.reviewer.bottom.web.eval(f"show_mouse('{event.type()}');")
            elif event.type() == QEvent.WindowActivate:
                mw.reviewer.bottom.web.eval(f"countDown('{event.type()}');")
        return False
loseFocusEventFilter = loseFocus()

########## Menu actions ##########
def resetPos():
    config = mw.addonManager.getConfig(__name__)
    config['answer_bar_posX'] = 0
    config['answer_bar_posY'] = 0
    mw.addonManager.writeConfig(__name__, config)
    updateBottom()

def on_context_menu_event(web, menu):
    if ndfs_inReview:
        menu.addAction(lockDrag)
    else:
        menu.removeAction(lockDrag)

#Qt inverts selection before triggering
def toggleBar():
    setLock()
    config = mw.addonManager.getConfig(__name__)
    config['answer_bar_locked'] = lockDrag.isChecked()
    mw.addonManager.writeConfig(__name__, config)

def setLock():
    if ndfs_inReview:
        if lockDrag.isChecked():
            mw.reviewer.bottom.web.eval("disable_drag();")
        else:
            mw.reviewer.bottom.web.eval("enable_drag();")

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





########## Hooks ##########
addHook("afterStateChange", stateChange)
addHook("showQuestion", updateBottom) #only needed so that bottom bar updates when Reviewer runs _init/_showQuestion every 100 answers
addHook("AnkiWebView.contextMenuEvent", on_context_menu_event)




########## Menu setup ##########
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

recheckBoxes()