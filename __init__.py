# No Distractions Full Screen
# v3.3 3/18/2020
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
from aqt.addons import *
import urllib

########## Wrappers ##########
#monkey patched function to disable height adjustment
def adjustHeightToFit_override(*args):
	return

#CSS/JS injection
def reviewer_wrapper(func):
	bottom_bar = open(os.path.join(os.path.dirname(__file__), 'bottom_bar.js')).read()
	draggable = open(os.path.join(os.path.dirname(__file__), 'draggable.js')).read()
	card_padding = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
	interact = open(os.path.join(os.path.dirname(__file__), 'interact.min.js')).read()
	iframe = open(os.path.join(os.path.dirname(__file__), 'iFrame.js')).read()

	def _initReviewerWeb(*args):
		config = mw.addonManager.getConfig(__name__)
		op = config['answer_button_opacity']
		cursorIdleTimer = config['cursor_idle_timer']
		color = config['answer_button_border_color']
		func()
		mw.reviewer.web.eval(interact)
		mw.reviewer.web.eval(draggable)
		mw.reviewer.bottom.web.eval(f"var op = {op}; var color = '{color}'; {bottom_bar}")
		mw.reviewer.web.eval(card_padding)
		mw.reviewer.web.eval(iframe) #construct iframe for bottom
	return _initReviewerWeb

def updateiFrame(html):
	global ndfs_inReview
	if ndfs_enabled:
		update = open(os.path.join(os.path.dirname(__file__), 'iframe_update.js')).read()
		html = urllib.parse.quote(html, safe='') #percent encoding hack so can be passed to js
		mw.reviewer.web.eval(f"var url = `{html}`; {update}")

def linkHandler_wrapper(self, url):
	global posX
	global posY
	if "NDFS-draggable_pos" in url:
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
def setupWeb(): #can be accomplished by just calling mw.reset(), but issue since also cycles to next card, since Reviewer.show() calls nextCard()
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
isFullscreen = False
fs_compat_mode = False
def toggle():
		global ndfs_enabled
		global ndfs_inReview
		global og_adjustHeightToFit
		global og_reviewer
		global og_window_flags
		global og_window_state
		global og_geometry
		global window_flags_set
		global fs_window
		global isFullscreen
		global fs_compat_mode
		config = mw.addonManager.getConfig(__name__)

		if not ndfs_enabled:
			ndfs_enabled = True
			window_flags_set = False
			checkSoftwareRendering()
			og_adjustHeightToFit = mw.reviewer.bottom.web.adjustHeightToFit
			og_window_state = mw.windowState()
			og_window_flags = mw.windowFlags() #stores initial flags
			og_reviewer = mw.reviewer._initWeb #stores initial reviewer before wrap

			mw.setUpdatesEnabled(False) #pauses drawing to screen to prevent flickering

			if config['last_toggle'] == 'full_screen': #Fullscreen mode
				if isMac: #kicks out of OSX maximize if on
					mw.showNormal()
					mw.showFullScreen()
				if isWin and config['MS_Windows_fullscreen_compatibility_mode']: #Graphical issues on windows when using inbuilt method
					og_geometry = mw.normalGeometry()
					mw.showNormal() #user reported bug where taskbar would show if maximized (prob not necessary, since changing window geometry automatically changes state to normal)
					if config['MS_Windows_fullscreen_force_on_top']: #user reported bug where taskbar would not disappear unless on top
						mw.setWindowFlags(mw.windowFlags() | Qt.WindowStaysOnTopHint)
					mw.setWindowFlags(mw.windowFlags() | Qt.FramelessWindowHint)
					fs_compat_mode = True
					window_flags_set = True
					mw.show()
					try:
						screenSize = mw.screen().geometry()
					except: #uses deprecated functions for legacy client support e.g. v2.1.15
						windowSize = mw.frameGeometry()
						offset = QPoint(10,10) #if maximized, pos returns coords that are off
						screenNum = mw.app.desktop().screenNumber(mw.pos() + offset)
						screenSize = mw.app.desktop().screenGeometry(screenNum)
					#Qt bug where if exactly screen size, will prevent overlays (context menus, alerts).
					#Screen size is affected by Windows scaling and Anki interace scaling, and so to make sure larger requires at least 1px border around screen.
					#If does not take up full screen height, will not hide taskbar
					mw.setGeometry(screenSize.x()-1,screenSize.y()-1,screenSize.width()+2, screenSize.height()+2)
				else:
					mw.showFullScreen()
				isFullscreen = True

			if (config['stay_on_top_windowed'] and not isFullscreen) : #ontopWindow option
				mw.setWindowFlags(mw.windowFlags() | Qt.WindowStaysOnTopHint)
				window_flags_set = True
				mw.show()

			mw.reviewer._initWeb = reviewer_wrapper(og_reviewer) #tried to use triggers instead but is called prematurely upon suspend/bury
			setupWeb()

			#Builds new widget for window
			fs_window = QWidget()
			fs_layout = QGridLayout(fs_window)
			fs_layout.setContentsMargins(QMargins(0,0,0,0))
			fs_layout.setSpacing(0)
			fs_layout.addWidget(mw.toolbar.web,0,0)#,Qt.AlignTop) #need to add or breaks (garbagecollected)
			fs_layout.addWidget(mw.reviewer.web,0,0)
			fs_layout.addWidget(mw.reviewer.bottom.web,0,0)

			mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
			mw.toolbar.web.hide()
			mw.reviewer.bottom.web.hide() #iFrame handles bottom bar

			mw.mainLayout.addWidget(fs_window)

			if config['cursor_idle_timer'] >= 0:
				mw.installEventFilter(curIdleTimer)
				curIdleTimer.countdown()
			if config['ignore_scroll_on_answer_buttons']:
				print('FIXME')

		else:
			ndfs_enabled = False
			ndfs_inReview = False
			mw.setUpdatesEnabled(False) #pauses updates to screen
			
			if isFullscreen and fs_compat_mode:
				mw.hide() #prevents ghost window from showing when resizing
				mw.setGeometry(og_geometry)
				fs_compat_mode = False
				window_flags_set = True #should always be true regardless - just reminder
			if window_flags_set: #helps prevent annoying flickering when toggling
				mw.setWindowFlags(og_window_flags) #reassigns initial flags
				window_flags_set = False
				
			isFullscreen = False

			mw.reviewer._initWeb = og_reviewer #reassigns initial constructor
			mw.setWindowState(og_window_state)
			mw.reviewer.bottom.web.adjustHeightToFit = og_adjustHeightToFit
			mw.mainLayout.removeWidget(fs_window)
			mw.mainLayout.addWidget(mw.toolbar.web)
			mw.mainLayout.addWidget(mw.reviewer.web)
			mw.mainLayout.addWidget(mw.reviewer.bottom.web)
			mw.toolbar.web.show()
			mw.reviewer.bottom.web.show()
			mw.menuBar().setMaximumHeight(QWIDGETSIZE_MAX)
			mw.removeEventFilter(curIdleTimer)
			curIdleTimer.showCursor()
			setupWeb()
			mw.show()
		delay = config['rendering_delay']
		def unpause():
			mw.setUpdatesEnabled(True)
		QTimer.singleShot(delay, unpause)

def updateBottom(*args):
	if ndfs_inReview:
		config = mw.addonManager.getConfig(__name__)
		#posX = config['answer_bar_posX']
		#posY = config['answer_bar_posY']
		#mw.reviewer.bottom.web.eval(f"updatePos({posX}, {posY});")
		#mw.reviewer.bottom.web.eval("activateHover();")
		padCards()
		#setLock()
		mw.reviewer.bottom.web.hide() #screen reset shows bottom bar
		if isFullscreen:
		   print('FIXME')
		   #mw.reviewer.bottom.web.eval("enable_bottomHover();") #enables showing of bottom bar when mouse on bottom
		mw.reviewer.bottom.web.evalWithCallback("""
			(function(){
				return document.documentElement.outerHTML
			}())
			""", updateiFrame)

last_state = mw.state
def stateChange(new_state, old_state, *args):
	global ndfs_inReview
	global ndfs_enabled
	global last_state
	config = mw.addonManager.getConfig(__name__)

	print(last_state + "->" + mw.state +" :: " + str(old_state) + " -> " + str(new_state))

	if mw.state == 'review': #triggers on NDFS_review and review states
		if config['auto_toggle_when_reviewing'] and not ndfs_enabled and mw.state == 'review' and last_state != mw.state: #filters out self generated NDFS_review state changes
			toggle() #sets ndfs_enabled to true
		if ndfs_enabled:
			ndfs_inReview = True
			updateBottom()
	elif ndfs_enabled:
		ndfs_inReview = False
		mw.reviewer.bottom.web.hide()
		curIdleTimer.showCursor()

		if config['auto_toggle_when_reviewing']: #manually changed screens/finished reviews
			if last_state == 'review' and mw.state in ['overview', 'deckBrowser']:
				toggle()

	if mw.state != 'resetRequired':
		last_state = mw.state

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
		msgBox = QMessageBox(QMessageBox.Warning, 'No Distractions Full Screen', 'Software Rendering detected!\nThis may cause artifacts with the No Distractions Full Screen addon and is not recommended.\nPlease switch to hardware acceleration via Anki Preferences if possible.');
		msgBox.setInformativeText("(If screen is frozen, try resizing the window as a workaround)");
		msgBox.setStandardButtons(QMessageBox.Ok);
		msgBox.setDefaultButton(QMessageBox.Ok);
		doNotShowAgain = QCheckBox('Do not show again')
		msgBox.setCheckBox(doNotShowAgain)
		msgBox.exec();
		if doNotShowAgain.isChecked():
			config['do_not_show_warnings'] = True
			mw.addonManager.writeConfig(__name__, config)





########## Idle Cursor Functions ##########
#Intercepts events to detect when focus is lost to show mouse cursor
class cursor_eventFilter(QObject):
	def __init__(self):
		QObject.__init__(self)
		self.timer = QTimer()
		self.timer.timeout.connect(self.hideCursor)
		self.updateIdleTimer()

	def eventFilter(self, obj, event):
		if ndfs_inReview:
			if event.type() in [QEvent.WindowDeactivate, QEvent.HoverLeave]: #Card edit does not trigger these - cursor shown by state change hook
				self.showCursor()
				self.timer.stop()
			elif event.type() == QEvent.HoverMove:
				self.showCursor()
				self.countdown()
			elif event.type() == QEvent.WindowActivate:
				self.countdown()			
		return False

	def countdown(self):
		self.timer.start(self.cursorIdleTimer)

	def updateIdleTimer(self):
		config = mw.addonManager.getConfig(__name__)
		self.cursorIdleTimer = config['cursor_idle_timer']

	def showCursor(self):
		self.timer.stop()
		if QGuiApplication.overrideCursor() is None:
			return
		if QGuiApplication.overrideCursor().shape() == Qt.BlankCursor: #hidden cursor
			QGuiApplication.restoreOverrideCursor()
			QGuiApplication.restoreOverrideCursor() #need to call twice	

	def hideCursor(self):
		self.timer.stop()
		QGuiApplication.setOverrideCursor(Qt.BlankCursor)
		print('hide')

curIdleTimer = cursor_eventFilter()

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
			mw.reviewer.web.eval("disable_drag();")
		else:
			mw.reviewer.web.eval("enable_drag();")

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

#opens config screen
def on_advanced_settings():
	addonDlg = AddonsDialog(mw.addonManager)
	addonDlg.accept() #closes addon dialog
	ConfigEditor(addonDlg,__name__,mw.addonManager.getConfig(__name__))

#sets up menu to display previous settings
def recheckBoxes(*args):
	config = mw.addonManager.getConfig(__name__)
	op = config['answer_button_opacity']
	cursorIdleTimer = config['cursor_idle_timer']
	last_toggle = config['last_toggle']
	w_onTop = config['stay_on_top_windowed']
	fs_shortcut = config['fullscreen_hotkey']
	lock_shortcut = config['lock_answer_bar_hotkey']
	dragLocked = config['answer_bar_locked']
	auto_tog = config['auto_toggle_when_reviewing']
	ms_fs_on_top = config['MS_Windows_fullscreen_force_on_top']

	curIdleTimer.updateIdleTimer()

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

	if w_onTop:
		keep_on_top.setChecked(True)

	if dragLocked:
		lockDrag.setChecked(True)

	if auto_tog:
		auto_toggle.setChecked(True)

	if ms_fs_on_top:
		config['MS_Windows_fullscreen_compatibility_mode'] = True

	mw.addonManager.writeConfig(__name__, config)
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
		w_onTop = True
	else:
		w_onTop = False
	config['stay_on_top_windowed'] = w_onTop

	if auto_toggle.isChecked():
		auto_tog = True
	else:
		auto_tog = False
	config['auto_toggle_when_reviewing'] = auto_tog

	mw.addonManager.writeConfig(__name__, config)




########## Hooks ##########
addHook("afterStateChange", stateChange)
addHook("showQuestion", updateBottom) #only needed so that bottom bar updates when Reviewer runs _init/_showQuestion every 100 answers
addHook("showAnswer", updateBottom)
addHook("AnkiWebView.contextMenuEvent", on_context_menu_event)
mw.addonManager.setConfigUpdatedAction(__name__, recheckBoxes)



########## Menu setup ##########
try:
	mw.addon_view_menu
except AttributeError:
	mw.addon_view_menu = QMenu(('View'), mw)
	mw.form.menubar.insertMenu(
		mw.form.menuTools.menuAction(),
		mw.addon_view_menu
	)

menu = QMenu(('ND Full Screen'), mw)
mw.addon_view_menu.addMenu(menu)

display = QActionGroup(mw)

fullscreen = QAction('Toggle Full Screen Mode', display)
fullscreen.triggered.connect(toggle_full_screen)
menu.addAction(fullscreen)

windowed = QAction('Toggle Windowed Mode', display)
windowed.triggered.connect(toggle_window)
menu.addAction(windowed)

keep_on_top = QAction('    ► Windowed Mode Always On Top', mw)
keep_on_top.setCheckable(True)
menu.addAction(keep_on_top)
keep_on_top.triggered.connect(user_settings)

auto_toggle = QAction('Auto-Toggle', mw)
auto_toggle.setCheckable(True)
auto_toggle.setChecked(False)
menu.addAction(auto_toggle)
auto_toggle.triggered.connect(user_settings)

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

menu.addSeparator()

advanced_settings = QAction('Advanced Settings (Config)', mw)
menu.addAction(advanced_settings)
advanced_settings.triggered.connect(on_advanced_settings)

recheckBoxes()
