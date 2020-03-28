# No Distractions Full Screen
### To install, please visit the <a href="https://ankiweb.net/shared/info/1049863218">addon page</a>

Eliminates <i>everything</i> unnecessary during reviews giving you maximum usable screen space and a clean, adjustable interface that supports touch.

<b><code>TL;DR:</code></b>  
<b>Press F11 for fullscreen</b> or use menu option <i>(View -&gt; Full Screen)</i>.

<b><code>Features:</code></b>
- <b>Hides all menu bars</b> including bottom bar ("More, Edit") and both top bars ("File, Edit..." and "Decks, Add...").
- <b>Superimposes answer buttons</b> over cards, with <b>adjustable opacity</b>. Becomes opaque on mouse-over.
- <b>Draggable answer buttons</b> that support touch. Enable with right click menu option or hotkey.
- <b>No Distractions Answer Bar</b>: Minimalistic reimagining of answer bar with animated answer confirmations
- <b>Hides mouse cursor</b> if idle.
- <b>No Distractions Windowed Mode</b>: Same clean interface in a resizable window. Accessible through menu. Can set to <b>always be on top</b>.
- <b>Auto-toggle</b> No Distractions mode when starting/leaving reviews
- <b>Highly customizable</b>: Common settings can be changed in menu options (<i>View -&gt; Full Screen</i>). Further settings can be changed in config, accessible through the <i>Advanced Settings</i> menu option. Detailed descriptions within.
- <b>Highly compatible</b>: Supports wide range of addons (tested list in notes section below), Win/Mac/Linux, hardware/software rendering modes and legacy clients (at least 2.1.15 and probably lower).
- <b>Review with minimal mouse movement</b>: allows card scrolling even when hovering over answer buttons (ideal for mouse users).

<b><code>In Action:</code></b>  
No Distractions Windowed Mode shown with <a href="https://ankiweb.net/shared/info/374005964" rel="nofollow">King of Buttons</a> addon:
<img src="https://i.ibb.co/44JKxCj/01kg-H1au5l.gif">

No Distractions Answer Bar with animated answer confirmation enabled:
<img src="https://i.ibb.co/p0YLTVS/HKASp-GFBt-W.gif">

<b><code>Notes:</code></b>  
- No Distractions Answer Bar uses a custom layout and may not play well with other addons. Feel free to report issues, and I will try my best, but widespread compatibility may not be possible.
- Automatically switches colors for normal/night mode with support for Night Mode Addon
- The F11 shortcut will automatically toggle the last enabled mode (either fullscreen or windowed).
- In Fullscreen mode, moving the mouse to the bottom of the screen will unhide answer buttons (if hidden).
- Supports all card layouts; cards are dynamically padded so that superimposed answer buttons do not obscure the bottom of cards when scrolled down
- Tested compatibility with v2.1.15, v2.1.20, v2.1.21, <a href="https://ankiweb.net/shared/info/1829090218" rel="nofollow">Large and Colorful Buttons</a>, <a href="https://ankiweb.net/shared/info/1496166067" rel="nofollow">Night Mode</a>, <a href="https://ankiweb.net/shared/info/538879081" rel="nofollow">Anki Zoom</a>, <a href="https://ankiweb.net/shared/info/1042429613" rel="nofollow">Large Fancy Buttons</a>, <a href="https://ankiweb.net/shared/info/1046608507" rel="nofollow">Speed Focus Mode</a>, <a href="https://ankiweb.net/shared/info/1758045507" rel="nofollow">Anki Habitica</a>, <a href="https://ankiweb.net/shared/info/1933645497" rel="nofollow">Fill the blanks</a>, <a href="https://ankiweb.net/shared/info/385888438" rel="nofollow">Edit field during review</a>, <a href="https://ankiweb.net/shared/info/1024346707" rel="nofollow">Directly Review</a>, <a href="https://ankiweb.net/shared/info/374005964" rel="nofollow">King of Buttons</a>, <a href="https://ankiweb.net/shared/info/378638814" rel="nofollow">Dancing Baloney</a>, <a href="https://ankiweb.net/shared/info/2091361802" rel="nofollow">Progress Bar</a>

- <b>Please report issues here: <a href="https://github.com/Quip13/No-Distractions-Full-Screen/issues" rel="nofollow">Github</a></b>.

<b><code>Changelog:</code></b>  
- 3/28/2020 v4.0:
  - Added No Distractions Answer Bar with animated confirmation
  - Added Normal/Night automatic color switching with support for Night Mode Addon
  - Reviewer rewritten to be one unified webpage with iFrames. Offers better performance and much better compatibility. Now supports software rendering, and plays better with other addons. Answer iFrames have zoom compensation so remains fixed in size and space on zoom.
  - Cursor hide logic rewritten to be python based  
- 3/16/2020 v3.2.8: Fixed bug on Windows where taskbar would not hide under certain resolutions/UI scale factors (big thanks to posnum for report)
- 3/15/2020 v3.2.7: Added config option to force fullscreen on top for Windows machines (helps resolve persistent taskbar issues). Auto-toggle state tracking improved for compatibility with addons that manipulate states
- 3/11/2020 v3.2.6: Added auto-toggle option - will trigger when entering reviews and when finishing reviews, going to the deck screen or syncing
- 3/9/2020 v3.2.5: Added option to use old fullscreen renderer for Windows users having issues with the new one. Added "Advanced Settings" menu option that directly links to the config. Config text made easier to read  
- 3/8/2020 v3.2.4: Fixed bug where fullscreen would always show on top  
- 3/8/2020 v3.2.3: Fixed flickering with Speed Focus Mode addon and other graphical issues (including context menu not showing) in fullscreen mode on Windows machines (big thanks to Cupbox for testing). All values in config now are effective immediately  
- 3/5/2020 v3.2.2: Fixed bug where toggling full screen mode in certain review conditions would change current card. Will also retain answer bar position when Anki automatically refreshes screen every 100 consecutive reviews  
- 3/1/2020 v3.2.1: Fixed error on linux machines  
- 2/29/2020 v3.2: Scrolling over answer buttons now scrolls cards, can be changed in config. Refactored code with minor performance improvements. Added manifest file. Bug fixes: more consistent answer button opacity transitions while changing cards and dragging  
- 2/28/2020 v3.1.2: Bug fixes: improved compatibility with other addons, answer buttons no longer briefly shift to origin after a new card, adjusted render sequence/delay to cause less flickering  
- 2/27/2020 v3.0:
  - Added draggable answer buttons (uses interact.js)
  - Rewrote bottom widget (again) to allow better interaction with cards (previously inputs would not register in bottom of screen)
  - Added subtle fade animation to non-opaque answer buttons
  - Added user-configurable delay when redrawing widgets to reduce flicker/artifacts (see config for more info)
  - Added new config and renamed fullscreen hotkey in config
  - Fixed bug with where always-on-top toggle would not reset
  - Added warning popup for software rendering
- 2/20/2020 v2.3.5: Rewrote cursor hide method to be more robust (now supports {type} cards)  
- 2/10/2020 v2.3.4: Added remappable hotkey to config. Bug fixes (adding cards now reveals cursor - thanks for bug submission)  
- 2/10/2020 v2.3.3: Removed limitation of full screen only in review. Added border color config option  
- 2/10/2020 v2.3.2: Performance improvements  
- 2/9/2020: v2.3: Added windowed mode. Added dynamic padding to bottom of cards. Rewrote display widget  
- 2/9/2020: v2.2.2: Added idle mouse hide feature. Added user-adjustable config. Bug fixes (now behaves properly when burying/suspending cards in full screen)  
- 2/4/2020: v2.1.1: Fixed bug where you could not exit full screen after finishing review - now automatically exits  
- 2/2/2020: v2.1: Added customizable answer button opacity  
- 2/1/2020: v2.0: Now hides bottom bar with floating answer buttons  

Big thanks to lovac42 for toolbar package, glutanimate's Toggle Full Screen Extended, <a href="https://ankiweb.net/shared/info/1612375712" rel="nofollow">Full Screen Toggle</a>, <a href="https://ankiweb.net/shared/info/1214415810" rel="nofollow">HTML Window Source</a> and <a href="https://ankiweb.net/shared/info/31746032" rel="nofollow">AnkiWebView Inspector</a>