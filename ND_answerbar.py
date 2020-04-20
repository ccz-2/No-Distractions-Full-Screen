# No Distractions Full Screen v4.1.3

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

def linkHandler_wrapper(self, url):
    if url == "NDFS_showAns" and NDAB_enabled:
        NDAB_showAnswerButs()
    elif url == "NDFS_showQues" and NDAB_enabled:
        mw.reviewer.bottom.web.eval(f'ansConf({last_ease}, `{mw.reviewer._remaining()}`)')
    else:
        origLinkHandler(self, url)
origLinkHandler = Reviewer._linkHandler
Reviewer._linkHandler = linkHandler_wrapper

def NDAB_bottomHTML():
    config = mw.addonManager.getConfig(__name__)
    animTime = config['answer_conf_time']
    if isNightMode:
        color = config['answer_button_border_color_night']
    else:
        color = config['answer_button_border_color_normal']

    NDAB_css = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.css')).read()
    NDAB_css_settings = get_css_settings()
    NDAB_html = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.html')).read()
    NDAB_css = f"""
        {NDAB_css_settings}
        :root {{
            --bkgndColor: {color};
             --animTime: {animTime}s;
            }}
        {NDAB_css}"""
    return f"""
        <style> {NDAB_css} </style>
        {NDAB_html}
        <script>
            time = {mw.reviewer.card.timeTaken()};
        </script>
        """

def NDAB_initWeb(func):
    NDAB_js = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.js')).read()
    def wrap(*args):
        func(*args)
        html = NDAB_bottomHTML()
        html = urllib.parse.quote(html, safe='')
        mw.reviewer.bottom.web.eval(f'var url = decodeURIComponent(`{html}`); $("#outer")[0].innerHTML = url')
        mw.reviewer.bottom.web.eval(NDAB_js)
    return wrap

def NDAB_showAnswerButs():
    default = mw.reviewer._defaultEase()
    def but(ease, label):
        if ease == default:
            extra = "id=defease"
        else:
            extra = ""
        due = mw.reviewer._buttonTime(ease)
        mw.reviewer.bottom.web.eval(f'insertAnsBut(`{due}`, `{extra}`, {ease}, `{label}`)')

    mw.reviewer.bottom.web.eval('clearButs();')
    for ease, label in NDAB_answerButtonList():
        but(ease, label)
    mw.reviewer.bottom.web.eval('$(function () { $("#defease").focus(); });')

# Reimplemented Anki method without multilingual support, to set language-agnostic class names
def NDAB_answerButtonList():
    l = ((1, ("Again")),)
    cnt = mw.col.sched.answerButtons(mw.reviewer.card)
    if cnt == 2:
        return l + ((2, ("Good")),)
    elif cnt == 3:
        return l + ((2, ("Good")), (3, ("Easy")))
    else:
        return l + ((2, ("Hard")), (3, ("Good")), (4, ("Easy")))

last_ease = 1
#Grabs the last ease - used in linkhandler for answer confirmation
def NDAB_answerCard(func):
    global last_ease
    def confAns(ease):
        global last_ease
        func(ease)
        last_ease = ease
    return confAns

NDAB_enabled = False
def enable_ND_bottomBar(nightMode = False):
    global og_initWeb, og_answerCard
    global isNightMode
    global NDAB_enabled
    NDAB_enabled = True
    isNightMode = nightMode
    og_initWeb = mw.reviewer._initWeb
    og_answerCard = mw.reviewer._answerCard
    mw.reviewer._answerCard  = NDAB_answerCard(mw.reviewer._answerCard)
    mw.reviewer._initWeb = NDAB_initWeb(mw.reviewer._initWeb)

def disable_ND_bottomBar():
    global NDAB_enabled
    NDAB_enabled = False

def get_css_settings():
    config = mw.addonManager.getConfig(__name__)
    css = config['NDAB_css_v1']
    if not css: #if empty (running for first time)
        css = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar_default_settings.css')).read()
        config['NDAB_css_v1'] = css
        mw.addonManager.writeConfig(__name__, config)
    return css

window = None
def on_ndab_settings():
    global window
    if window and window.isVisible():
        window.raise_()
        return
    css = get_css_settings() 

    window = QDialog(mw)
    window.setWindowTitle("No-Distractions-Answer-Bar Appearance Settings")
    buttons = QDialogButtonBox()
    buttons.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Close | QDialogButtonBox.RestoreDefaults)

    text_editor = QPlainTextEdit()
    text_editor.setPlainText(css)
    text_editor.setWordWrapMode(QTextOption.NoWrap)
    text_editor.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

    msg = QLabel('''
        The following CSS variables can be adjusted to change the appearance of No Distractions Answer Bar
        <br><span style='color:mediumaquamarine'><b>Toggling No Distractions Mode will apply settings.
        <br>This window can be kept open to make on-the-fly changes eaiser.</b></span>
        <br>
        <br>Note: To change the background color of the "Show Answer" button equivalent, change the 
            <code><span style="color:dodgerblue">answer_button_border_color_night</span></code> and 
            <code><span style="color:dodgerblue">answer_button_border_color_normal</span></code> values in the <b>addon-config</b> (not here).''')
    msg.setTextFormat(Qt.RichText)
    msg.setWordWrap(True)

    def save():
        css = text_editor.document().toPlainText()
        config = mw.addonManager.getConfig(__name__)
        config['NDAB_css_v1'] = css
        mw.addonManager.writeConfig(__name__, config)

    def restore_defaults():
        NDAB_css_settings = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar_default_settings.css')).read()
        text_editor.setPlainText(NDAB_css_settings)
        save()

    def sizeHintOverload():
        return QSize(600, 400) 

    buttons.accepted.connect(save)
    buttons.rejected.connect(window.close)
    buttons.button(QDialogButtonBox.RestoreDefaults).clicked.connect(restore_defaults)

    layout = QVBoxLayout()
    layout.addWidget(msg)
    layout.addWidget(text_editor)
    layout.addWidget(buttons)
    window.setLayout(layout)
    window.sizeHint = sizeHintOverload
    window.show()
