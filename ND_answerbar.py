from aqt.reviewer import Reviewer, ReviewerBottomBar
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
    NDAB_html = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.html')).read()
    NDAB_css = f"""
        :root {{
            --bkgndColor: {color};
             --animTime: {animTime}s;
            }} \n {NDAB_css}"""
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
    for ease, label in mw.reviewer._answerButtonList():
        but(ease, label)
    mw.reviewer.bottom.web.eval('$(function () { $("#defease").focus(); });')

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