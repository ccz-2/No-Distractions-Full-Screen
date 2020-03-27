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

def NDAB_bottomHTML():
    config = mw.addonManager.getConfig(__name__)
    animTime = config['answer_conf_time']
    if isNightMode:
        color = config['answer_button_border_color_night']
    else:
        color = config['answer_button_border_color_normal']

    NDAB_css = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.css')).read()
    NDAB_js = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.js')).read()
    NDAB_html = open(os.path.join(os.path.dirname(__file__), 'ND_answerbar.html')).read()
    NDAB_css = f"""
        :root {{
            --bkgndColor: {color};
             --animTime: {animTime}s;
            }} \n {NDAB_css}"""
    return f"""
        <script> {NDAB_js} </script>
        <style> {NDAB_css} </style>
        {NDAB_html}
        <script>
            time = {mw.reviewer.card.timeTaken()};
        </script>
        """

def NDAB_answerButtons():
    default = mw.reviewer._defaultEase()

    def but(ease, label):
        if ease == default:
            extra = "id=defease"
        else:
            extra = ""
        due = mw.reviewer._buttonTime(ease)
        mw.reviewer.bottom.web.eval(f'insertAnsBut("{due}", "{extra}", {ease}, "{label}")')

    mw.reviewer.bottom.web.eval('clearButs();')
    for ease, label in mw.reviewer._answerButtonList():
        but(ease, label)
    mw.reviewer.bottom.web.eval('$(function () { $("#defease").focus(); });')

def NDAB_showEaseButtons():
    NDAB_answerButtons()

def NDAB_showAnswerButton():
    mw.reviewer.bottom.web.eval(f'insertQuesBut("{mw.reviewer._remaining()}")')
    if mw.reviewer.card.shouldShowTimer():
        maxTime = mw.reviewer.card.timeLimit() / 1000
    else:
        maxTime = 0
    mw.reviewer.bottom.web.eval(f"showQuestion('',{maxTime});")
    mw.reviewer.bottom.web.adjustHeightToFit()

def NDAB_answerCard(func):
    def confAns(ease):
        func(ease)
        mw.reviewer.bottom.web.eval(f'ansConf({ease}, "{mw.reviewer._remaining()}")')
    return confAns


def enable_ND_bottomBar(nightMode = False):
    global og_bottomHTML, og_answerButtons, og_bottomTime, og_showEaseButtons, og_showAnswerButton, og_answerCard
    global isNightMode
    isNightMode = nightMode

    og_bottomHTML = mw.reviewer._bottomHTML
    og_answerButtons = mw.reviewer._answerButtons
    og_bottomTime = mw.reviewer._buttonTime
    og_showEaseButtons = mw.reviewer._showEaseButtons
    og_showAnswerButton = mw.reviewer._showAnswerButton
    og_answerCard = mw.reviewer._answerCard

    mw.reviewer._bottomHTML = NDAB_bottomHTML
    mw.reviewer._answerButtons = NDAB_answerButtons
    mw.reviewer._showEaseButtons = NDAB_showEaseButtons
    mw.reviewer._showAnswerButton = NDAB_showAnswerButton
    mw.reviewer._answerCard  = NDAB_answerCard(mw.reviewer._answerCard)

def disable_ND_bottomBar():
    mw.reviewer._bottomHTML = og_bottomHTML
    mw.reviewer._answerButtons = og_answerButtons
    mw.reviewer._showEaseButtons = og_showEaseButtons
    mw.reviewer._showAnswerButton = og_showAnswerButton
    mw.reviewer._answerCard  = og_answerCard