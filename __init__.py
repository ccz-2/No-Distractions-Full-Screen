# No Distractions Full Screen
# v4.1.8 8/13/2020
# Copyright (c) 2020 Quip13 (random.emailforcrap@gmail.com)
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limiattion the rights
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
from anki import version as anki_version
from .toolbar import *
from .ND_answerbar import *
import os

########## Wrappers ##########
#CSS/JS injection
def reviewer_wrapper(func):
	draggable = open(os.path.join(os.path.dirname(__file__), 'draggable.js')).read()
	card_padding = open(os.path.join(os.path.dirname(__file__), 'card_padding.js')).read()
	interact = open(os.path.join(os.path.dirname(__file__), 'interact.min.js')).read()
	iframe = open(os.path.join(os.path.dirname(__file__), 'iFrame.js')).read()
	bbActual_html_manip = open(os.path.join(os.path.dirname(__file__), 'bbActual_html_manip.js')).read()
	bbBkgnd_html_manip = open(os.path.join(os.path.dirname(__file__), 'bbBkgnd_html_manip.js')).read()
	bottom_bar_sizing = open(os.path.join(os.path.dirname(__file__), 'bottom_bar_sizing.js')).read()
	config = mw.addonManager.getConfig(__name__)

	def _initReviewerWeb(*args):

		config = mw.addonManager.getConfig(__name__)
		op = config['answer_button_opacity']
		iFrame_domDone = False #set to true after HTML is injected
		iFrameDummy_domDone = False
		NDAB = int(config['ND_AnswerBar_enabled'])

		func()
		mw.reviewer.web.eval(f'window.defaultScale = {getScale()}') #sets scale factor for javascript functions
		mw.reviewer.web.eval(f'window.NDAB = {NDAB}') #sets scale factor for javascript functions	
		mw.reviewer.web.eval(interact)
		mw.reviewer.web.eval(draggable)
		if not config['ND_AnswerBar_enabled']:
			mw.reviewer.bottom.web.eval(bbActual_html_manip)
			mw.reviewer.bottom.web.eval(bbBkgnd_html_manip)
		else:
			mw.reviewer.bottom.web.eval('//<<<FOR BKGND>>>//\n $("#container").hide();')
			mw.reviewer.bottom.web.eval('//<<<FOR ACTUAL>>>//\n $("td.stat").hide();')

		mw.reviewer.web.eval(card_padding)
		mw.reviewer.web.eval(f'var op = {op}; {iframe}') #prettify iframe
		mw.reviewer.bottom.web.eval(f"var scale = {getScale()}; {bottom_bar_sizing}")

		mw.reviewer.bottom.web.eval(f"finishedLoad();")
		mw.reviewer.bottom.web.hide() #automatically shown in _initWeb
	return _initReviewerWeb

def getScale():
	try: 
		scale = mw.screen().devicePixelRatio()
	except:
		scale = mw.windowHandle().devicePixelRatio() #support for legacy clients (e.g.)
	return scale

isNightMode = False
def checkNightMode(on = None):
	global isNightMode
	old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)
	if old_anki:
		if on is not None:
			isNightMode = on
	else:
		from aqt.theme import theme_manager
		if theme_manager.night_mode:
			isNightMode = True

def linkHandler_wrapper(self, url):
	global posX
	global posY
	global iFrame_domDone
	global iFrameDummy_domDone
	if "NDFS-draggable_pos" in url:
		pos = url.split(": ")[1]
		pos = pos.split(", ")
		posX = pos[0]
		posY = pos[1]
		config = mw.addonManager.getConfig(__name__)
		config['answer_bar_posX'] = posX
		config['answer_bar_posY']  = posY
		mw.addonManager.writeConfig(__name__, config)
	elif url == "NDFS-iFrame-DOMReady":
		iFrame_domDone = True
		runiFrameJS()
	elif url == 'NDFS-iFrameDummy-DOMReady':
		iFrameDummy_domDone = True
		runiFrameJS()
	else:
		origLinkHandler(self, url)
origLinkHandler = Reviewer._linkHandler
Reviewer._linkHandler = linkHandler_wrapper





########## PyQt manipulation ##########

iFrame_domDone = False #Is set to true via pycmd after HTML loaded
iFrameDummy_domDone = False
js_queue = []
def runiFrameJS(): # Mimics Anki reviewer evalWithCallback queue, just for iFrame
	global js_queue
	while len(js_queue) != 0 and iFrame_domDone and iFrameDummy_domDone and mw.state == 'review':
		i = js_queue.pop(0)
		js = i[0]
		cb = i[1]
		js = urllib.parse.quote(js, safe='')
		mw.reviewer.web.evalWithCallback(f"scriptExec(`{js}`);", cb)			

def setupWeb():
	global js_queue
	global iFrame_domDone
	global iFrameDummy_domDone
	global ndfs_inReview

	config = mw.addonManager.getConfig(__name__)
	if config['ND_AnswerBar_enabled']:
		color = 'transparent'
	elif isNightMode:
		color = config['answer_button_border_color_night']
	else:
		color = config['answer_button_border_color_normal']
	
	drag_hotkey = urllib.parse.quote(config['lock_answer_bar_hotkey'], safe='')
	def setHtml_wrapper(self, html, _old):
		if self == mw.reviewer.bottom.web:
			iframe_setHTML = open(os.path.join(os.path.dirname(__file__), 'iframe_setHTML.js')).read()
			html = urllib.parse.quote(html, safe='')
			mw.reviewer.web.eval(f"var url = `{html}`; var color = '{color}'; var drag_hotkey = `{drag_hotkey}`; {iframe_setHTML}")
		else:
			_old(self, html)

	def evalWithCallback_wrapper(self, js, cb, _old):
		global js_queue
		if self == mw.reviewer.bottom.web:
			js_queue.append([js, cb])
			runiFrameJS()
		else:
			_old(self, js, cb)

	def reviewerSetFocus_wrapper(func):
		def reviewerFocus(*args):
			func(*args)
			mw.reviewer.bottom.web.eval('parent.focus()')
		return reviewerFocus

	if ndfs_inReview:
		iFrame_domDone = False
		iFrameDummy_domDone = False

		AnkiWebView._setHtml = wrap(AnkiWebView._setHtml,setHtml_wrapper, "around")
		AnkiWebView._evalWithCallback = wrap(AnkiWebView._evalWithCallback,evalWithCallback_wrapper, "around")
		mw.reviewer.web.setFocus = reviewerSetFocus_wrapper(mw.reviewer.web.setFocus)
	elif not ndfs_enabled: #disabling NDFS
		AnkiWebView._setHtml = og_setHtml
		AnkiWebView._evalWithCallback = og_evalWithCallback
		mw.reviewer.web.setFocus = og_setFocus

	if mw.state == 'review':
		try:
			reviewState = mw.reviewer.state
			mw.reviewer._initWeb() #reviewer_wrapper is run
			mw.reviewer.bottom.web.hide() #automatically shown in _initWeb
			mw.reviewer._showQuestion()
			if reviewState == 'answer':
				try:
					mw.reviewer._showAnswer() #breaks on fill in the blank cards
				except:
					pass
		except:
			mw.reset() #failsafe
	else:
		mw.reset()

	if ndfs_inReview:
		updateBottom()
		mw.reviewer.bottom.web.reload() #breaks currently running scripts in bottom

def updateBottom(*args):
	if ndfs_inReview:
		config = mw.addonManager.getConfig(__name__)
		posX = config['answer_bar_posX']
		posY = config['answer_bar_posY']
		mw.reviewer.web.eval(f"updatePos({posX}, {posY});")
		padCards()
		setLock()
		if isFullscreen:
		   mw.reviewer.web.eval("enable_bottomHover();") #enables showing of bottom bar when mouse on bottom

last_state = mw.state
def stateChange(new_state, old_state, *args):
	global ndfs_inReview
	global ndfs_enabled
	global last_state
	config = mw.addonManager.getConfig(__name__)

	#print(last_state + "->" + mw.state +" :: " + str(old_state) + " -> " + str(new_state))
	if mw.state == 'review':
		if config['auto_toggle_when_reviewing'] and not ndfs_enabled and last_state != mw.state:
			toggle() #sets ndfs_enabled to true
		if ndfs_enabled:
			ndfs_inReview = True
			setupWeb()
			curIdleTimer.enable()
			if config['ND_AnswerBar_enabled']:
				resetPos()
	elif ndfs_enabled:
		ndfs_inReview = False
		curIdleTimer.disable()
		mw.reviewer.web.eval("$('#outer').remove()") #remove iframe
		if config['auto_toggle_when_reviewing']: #manually changed screens/finished reviews
			if last_state == 'review' and mw.state in ['overview', 'deckBrowser']:
				toggle()

	if ndfs_enabled and mw.reviewer.bottom.web.isVisible():
		mw.reviewer.bottom.web.hide() #screen reset shows bottom bar

	if mw.state != 'resetRequired':
		last_state = mw.state

def padCards():
	def padCardsCallback(height):
		mw.reviewer.web.eval(f"calcPadding({height});")
	mw.reviewer.web.evalWithCallback('$("#bottomiFrame").contents().height()', padCardsCallback) #not exact height but does not need to be precise

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
		global isFullscreen
		global fs_compat_mode
		global DPIScaler
		global og_setHtml,og_evalWithCallback, og_setFocus
		global curIdleTimer
		config = mw.addonManager.getConfig(__name__)
		checkNightMode()

		if not ndfs_enabled:
			ndfs_enabled = True
			window_flags_set = False
			og_window_state = mw.windowState()
			og_window_flags = mw.windowFlags() #stores initial flags
			og_reviewer = mw.reviewer._initWeb #stores initial reviewer before wrap

			og_setHtml = AnkiWebView._setHtml
			og_evalWithCallback = AnkiWebView._evalWithCallback
			og_setFocus = mw.reviewer.web.setFocus
			curIdleTimer = cursorHide()
			curIdleTimer.install(mw)

			mw.setUpdatesEnabled(False) #pauses drawing to screen to prevent flickering

			reset_bar.setVisible(True) #menu items visible for context menu
			lockDrag.setVisible(True)

			if config['last_toggle'] == 'full_screen': #Fullscreen mode
				if isMac:
					mw.showFullScreen()
				if isWin and config['MS_Windows_fullscreen_compatibility_mode']: #Graphical issues on windows when using inbuilt method
					og_geometry = mw.normalGeometry()
					mw.showNormal() #user reported bug where taskbar would show if maximized (prob not necessary, since changing window geometry automatically changes state to normal)
					mw.setWindowFlags(mw.windowFlags() | Qt.FramelessWindowHint)
					fs_compat_mode = True
					window_flags_set = True
					mw.show()
					try:
						screenSize = mw.screen().geometry()
					except: #uses deprecated functions for legacy client support e.g. v2.1.15
						windowSize = mw.frameGeometry()
						screenNum = mw.app.desktop().screenNumber(mw)
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

			mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
			mw.toolbar.web.hide()
			mw.mainLayout.removeWidget(mw.reviewer.bottom.web) #removing from layout resolves quick reformatting changes when automatically shown
			mw.reviewer.bottom.web.hide() #iFrame handles bottom bar
			if config['ND_AnswerBar_enabled']:
				enable_ND_bottomBar(isNightMode)
			mw.reviewer._initWeb = reviewer_wrapper(mw.reviewer._initWeb) #tried to use triggers instead but is called prematurely upon suspend/bury
			stateChange(None, None) #will setup web and cursor

			try:
				def scaleChange():
					if ndfs_inReview:
						mw.reviewer.web.eval(f'changeScale({getScale()})')
				DPIScaler = mw.windowHandle().screenChanged.connect(scaleChange)
			except:
				print('NDFS: Screen Change Listener connection error')

		else:
			ndfs_enabled = False
			ndfs_inReview = False
			mw.setUpdatesEnabled(False) #pauses updates to screen
			mw.reviewer._initWeb = og_reviewer #reassigns initial constructor
			if mw.state == 'review':
				mw.reviewer.web.eval('disableResize();')
			if config['ND_AnswerBar_enabled']:
				disable_ND_bottomBar()
			setupWeb()

			if isFullscreen and fs_compat_mode:
				mw.hide() #prevents ghost window from showing when resizing
				mw.setGeometry(og_geometry)
				fs_compat_mode = False
				window_flags_set = True #should always be true regardless - just reminder
			if window_flags_set: #helps prevent annoying flickering when toggling
				mw.setWindowFlags(og_window_flags) #reassigns initial flags
				window_flags_set = False
			if isFullscreen: #only change window state if was fullscreen
				mw.setWindowState(og_window_state)
				isFullscreen = False

			mw.toolbar.web.show()
			mw.mainLayout.addWidget(mw.reviewer.bottom.web)
			mw.reviewer.bottom.web.show()
			mw.menuBar().setMaximumHeight(QWIDGETSIZE_MAX)
			curIdleTimer.uninstall(mw)

			reset_bar.setVisible(False)
			lockDrag.setVisible(False)

			try: #resolves disconnection error bug
				mw.windowHandle().screenChanged.disconnect(DPIScaler)
			except:
				print('NDFS: Screen Change Listener disconnection error')

			mw.show()

		delay = config['rendering_delay']		
		QTimer.singleShot(delay, lambda:mw.setUpdatesEnabled(True))

########## Mac Auto Toggle ##########
class macAutoToggle(QObject):
	def __init__(self):
		QObject.__init__(self)

	def install(self, widget):
		widget.installEventFilter(self)

	def uninstall(self, widget):
		widget.removeEventFilter(self)

	def eventFilter(self, obj, event):
		if event.type() in [QEvent.WindowStateChange]:
			if mw.isFullScreen() and not ndfs_enabled:
				toggle()
			elif not mw.isFullScreen() and ndfs_enabled:
				toggle()
		return False

macToggle = macAutoToggle()

########## Idle Cursor Functions ##########
#Intercepts events to detect when focus is lost to show mouse cursor
class cursorHide(QObject):
	def __init__(self):
		QObject.__init__(self)
		self.config = mw.addonManager.getConfig(__name__)
		self.timer = QTimer()
		self.timer.timeout.connect(self.hideCursor)
		self.cursorIdleTimer = self.config['cursor_idle_timer']
		self.enabled = False

	def install(self, widget):
		if self.cursorIdleTimer >= 0:
			widget.installEventFilter(self)
			self.enable()

	def uninstall(self, widget):
		widget.removeEventFilter(self)
		self.disable()

	def enable(self):
		self.enabled = True
		self.countdown()

	def disable(self):
		self.enabled = False
		self.showCursor()

	def eventFilter(self, obj, event):
		if ndfs_inReview:
			if event.type() in [QEvent.WindowDeactivate]: #Card edit does not trigger these - cursor shown by state change hook
				self.disable()
			elif event.type() in [QEvent.HoverMove, QEvent.HoverEnter]:
				if self.config['cursor_idle_timer'] > 0:
					self.showCursor()
				if self.enabled:
					self.countdown()
			elif event.type() in [QEvent.WindowActivate]:
				self.enable()
		return False

	def countdown(self):
		if self.config['cursor_idle_timer'] >= 0:
			self.timer.start(self.cursorIdleTimer)

	def showCursor(self):
		self.timer.stop()
		if QGuiApplication.overrideCursor() is None:
			return
		if QGuiApplication.overrideCursor().shape() == Qt.BlankCursor: #hidden cursor
			QGuiApplication.restoreOverrideCursor()
			QGuiApplication.restoreOverrideCursor() #need to clear stack, call twice

	def hideCursor(self):
		self.timer.stop()
		if QGuiApplication.overrideCursor() is None:
			QGuiApplication.setOverrideCursor(Qt.BlankCursor)

########## Menu actions ##########
def resetPos():
	config = mw.addonManager.getConfig(__name__)
	config['answer_bar_posX'] = 0
	config['answer_bar_posY'] = 0
	mw.addonManager.writeConfig(__name__, config)
	updateBottom()

def on_context_menu_event(web, menu):
	config = mw.addonManager.getConfig(__name__)
	menu.addSection('NDFS')
	menu.addAction(toggleNDFS)

	if ndfs_inReview and not config['ND_AnswerBar_enabled']:
		menu.addAction(lockDrag)
		menu.addAction(reset_bar)
	else:
		menu.removeAction(lockDrag)
		menu.removeAction(reset_bar)
	menu.addSeparator()

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

def activate_fs():
	config = mw.addonManager.getConfig(__name__)
	config['last_toggle'] = 'full_screen'
	mw.addonManager.writeConfig(__name__, config)

def activate_windowed():
	config = mw.addonManager.getConfig(__name__)
	config['last_toggle'] = 'windowed'
	mw.addonManager.writeConfig(__name__, config)

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
	rendering_delay = config['rendering_delay']
	NDAB = config['ND_AnswerBar_enabled']
	ans_conf_time = config['answer_conf_time']
	mac_tog = config['auto_toggle_when_mac_max_min']

	if rendering_delay < 0:
		config['rendering_delay'] = 0

	if op == 1:
		mouseover_default.setChecked(True)
	elif op == 0:
		mouseover_hidden.setChecked(True)
	else:
		mouseover_translucent.setChecked(True)

	if cursorIdleTimer >= 0:
		enable_cursor_hide.setChecked(True)
	else:
		enable_cursor_hide.setChecked(False)

	toggleNDFS.setShortcut(fs_shortcut)
	if last_toggle == 'windowed':
		windowed.setChecked(True)
	else:
		fullscreen.setChecked(True)

	if w_onTop:
		keep_on_top.setChecked(True)
	else:
		keep_on_top.setChecked(False)

	lockDrag.setShortcut(lock_shortcut)
	if dragLocked:
		lockDrag.setChecked(True)
	else:
		lockDrag.setChecked(False)

	if auto_tog:
		auto_toggle.setChecked(True)
	else:
		auto_toggle.setChecked(False)

	if NDAB:
		nd_answerBar.setChecked(True)
	else:
		nd_answerBar.setChecked(False)

	if ans_conf_time > 0:
		ans_conf.setChecked(False)
	else:
		config['answer_conf_time'] = 0
		ans_conf.setChecked(True)

	if mac_tog:
		macAutoToggle.setChecked(True)
	else:
		macAutoToggle.setChecked(False)

	ndab_settings_check()
	mw.addonManager.writeConfig(__name__, config)

#conditional settings
def ndab_settings_check():
	if nd_answerBar.isChecked():
		lockDrag.setEnabled(False)
		lockDrag.setChecked(True)
		config = mw.addonManager.getConfig(__name__)
		config['answer_bar_locked'] = True
		mw.addonManager.writeConfig(__name__, config)
		reset_bar.setEnabled(False)
		ans_conf.setEnabled(True)
	else:
		lockDrag.setEnabled(True)
		reset_bar.setEnabled(True)
		ans_conf.setEnabled(False)

	if macAutoToggle.isChecked() and isMac:
		macToggle.install(mw)
	else:
		macToggle.uninstall(mw)

########## Hooks ##########
addHook("afterStateChange", stateChange)
addHook("showQuestion", updateBottom) #only needed so that bottom bar updates when Reviewer runs _init/_showQuestion every 100 answers
addHook("showAnswer", updateBottom)
addHook("AnkiWebView.contextMenuEvent", on_context_menu_event)
mw.addonManager.setConfigUpdatedAction(__name__, recheckBoxes)
addHook("night_mode_state_changed", checkNightMode) #Night Mode addon (1496166067) support for legacy Anki versions


def menu_select(state, confVal):
	config = mw.addonManager.getConfig(__name__)
	config[confVal] = state
	mw.addonManager.writeConfig(__name__, config)
	ndab_settings_check()

########## Menu setup ##########
addon_view_menu = getMenu(mw, "&View")
menu = QMenu(('ND Full Screen'), mw)
addon_view_menu.addMenu(menu)

display = QActionGroup(mw)

toggleNDFS = QAction('Toggle No Distractions', mw)
toggleNDFS.triggered.connect(toggle)
menu.addAction(toggleNDFS)

if isMac:
	dummy = QAction('(New in NDFS: Use green window maximize button for fullscreen)', mw)
	dummy.setEnabled(False)
	menu.addAction(dummy)

fullscreen = QAction('     Full Screen Mode', display)
fullscreen.triggered.connect(activate_fs)
fullscreen.setCheckable(True)
fullscreen.setChecked(True)
menu.addAction(fullscreen)

windowed = QAction('     Windowed Mode', display)
windowed.triggered.connect(activate_windowed)
windowed.setCheckable(True)
windowed.setChecked(False)
menu.addAction(windowed)

menu.addSeparator()

nd_answerBar = QAction('Enable No Distractions Answer Bar', mw)
nd_answerBar.setCheckable(True)
nd_answerBar.setChecked(False)
menu.addAction(nd_answerBar)
nd_answerBar.triggered.connect(lambda state, confVal = 'ND_AnswerBar_enabled': menu_select(state,confVal))

ans_conf = QAction('    Disable Answer Confirmation', mw)
ans_conf.setCheckable(True)
ans_conf.setChecked(False)
menu.addAction(ans_conf)
ans_conf.triggered.connect(lambda state, confVal = 'answer_conf_time': menu_select(0,confVal) if state else menu_select(0.5,confVal))

menu.addSection('Quick Settings')

auto_toggle = QAction('Auto-Toggle when Reviewing', mw)
auto_toggle.setCheckable(True)
auto_toggle.setChecked(False)
menu.addAction(auto_toggle)
auto_toggle.triggered.connect(lambda state, confVal = 'auto_toggle_when_reviewing': menu_select(state,confVal))

macAutoToggle = QAction('Auto-Toggle when Max/Min', mw)
macAutoToggle.setCheckable(True)
macAutoToggle.setChecked(False)
menu.addAction(macAutoToggle)
macAutoToggle.triggered.connect(lambda state, confVal = 'auto_toggle_when_mac_max_min': menu_select(state,confVal))
macAutoToggle.setVisible(False)

if isMac: #uses windowed mode and removes toggle options (FS mode is built in)
	windowed.setVisible(False)
	fullscreen.setVisible(False)
	macAutoToggle.setVisible(True)
	activate_windowed()	

keep_on_top = QAction('Always On Top (Windowed mode)', mw)
keep_on_top.setCheckable(True)
menu.addAction(keep_on_top)
keep_on_top.triggered.connect(lambda state, confVal = 'stay_on_top_windowed': menu_select(state,confVal))

enable_cursor_hide = QAction('Enable Idle Cursor Hide', mw)
enable_cursor_hide.setCheckable(True)
enable_cursor_hide.setChecked(True)
menu.addAction(enable_cursor_hide)
enable_cursor_hide.triggered.connect(lambda state, confVal = 'cursor_idle_timer': menu_select(10000,confVal) if state else menu_select(-1,confVal))

ABVisMenu = QMenu(('Answer Button Visibility'), mw)
menu.addMenu(ABVisMenu)

mouseover = QActionGroup(mw)
mouseover_default = QAction('Do Not Hide', mouseover)
mouseover_default.setCheckable(True)
ABVisMenu.addAction(mouseover_default)
mouseover_default.setChecked(True)
mouseover_default.triggered.connect(lambda state, confVal = 'answer_button_opacity': menu_select(1,confVal) if state else None)

mouseover_translucent = QAction('Translucent (Reveals on Mouseover)', mouseover)
mouseover_translucent.setCheckable(True)
ABVisMenu.addAction(mouseover_translucent)
mouseover_translucent.triggered.connect(lambda state, confVal = 'answer_button_opacity': menu_select(0.5,confVal) if state else None)

mouseover_hidden = QAction('Hidden (Reveals on Mouseover)', mouseover)
mouseover_hidden.setCheckable(True)
ABVisMenu.addAction(mouseover_hidden)
mouseover_hidden.triggered.connect(lambda state, confVal = 'answer_button_opacity': menu_select(0,confVal) if state else None)

menu.addSection('Advanced Settings')

advanced_settings = QAction('General Settings (Config)', mw)
menu.addAction(advanced_settings)
advanced_settings.triggered.connect(on_advanced_settings)

ndab_settings = QAction('ND Answer Bar Appearance Settings', mw)
menu.addAction(ndab_settings)
ndab_settings.triggered.connect(on_ndab_settings)

#Hidden actions - accessible through right click
lockDrag = QAction('Lock Answer Bar Position', mw)
lockDrag.setCheckable(True)
menu.addAction(lockDrag) #need to add for shortcut
lockDrag.setVisible(False)
lockDrag.triggered.connect(toggleBar)

reset_bar = QAction('Reset Answer Bar Position', mw)
reset_bar.triggered.connect(resetPos)

recheckBoxes()