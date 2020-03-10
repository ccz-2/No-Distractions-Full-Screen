# No Distractions Full Screen
# Made by Quip13 (random.emailforcrap@gmail.com) <- its real :)
# v2.0 2/1/2020

from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import addHook

def reformat_screen_css():
    if mw.isFullScreen():
        mw.reviewer.bottom.web.eval(f"$('button[onclick*=\"edit\"], button[onclick*=\"more\"]').css({{'visibility': 'hidden'}});") #removes edit, more buttons
        #mw.reviewer.bottom.web.eval(f"$('.nobold, .stattxt').css({{'text-shadow':'2px 2px 5px #000000, 2px -2px 5px #000000, -2px -2px 5px #000000, -2px 2px 5px #000000'}});") #adds shadow to text
        mw.reviewer.bottom.web.eval(f"$('body, #outer').css({{'background':'transparent', 'border-top-color':'transparent'}});") #removes gradient coloring
        mw.reviewer.bottom.web.eval(f"$('table:not([id=\"innertable\"]').css({{'padding':'0px','border-radius':'5px','background-color':'rgba(100,100,100,0.8)'}});") #adds box around buttons

def toggle_full_screen():
    if not mw.isFullScreen():
        mw.setWindowState(mw.windowState() | Qt.WindowFullScreen)
        mw.reviewer.bottom.web.page().setBackgroundColor(QColor(0, 0, 0, 0)) #qtwidget background removal
        mw.menuBar().setMaximumHeight(0) #Removes File Edit etc.
        mw.toolbar.web.setFixedHeight(0) #Removes Decks Add etc.
        mw.mainLayout.removeWidget(mw.reviewer.bottom.web) #Removes bottom bar from layout (makes it float)
        reformat_screen_css()
    else:
        mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)
        mw.reset()
        mw.menuBar().setMaximumHeight(9999)
        mw.toolbar.web.adjustHeightToFit()
        mw.mainLayout.addWidget(mw.reviewer.bottom.web)

#reformat css when bottom refreshes
addHook("showQuestion", reformat_screen_css)
addHook("showAnswer", reformat_screen_css)

action = QAction("Toggle Full Screen", mw)
action.setShortcut("F11")
action.triggered.connect(toggle_full_screen)
mw.form.menuTools.addAction(action)