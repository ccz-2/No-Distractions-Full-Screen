# No-Distractions-Full-Screen

This is an Anki addon that eliminates <i>everything</i> unnecessary during reviews giving you maximum usable screen space and a clean, adjustable interface that supports touch.

### To install please go to the  <a href="https://ankiweb.net/shared/info/1049863218" rel="nofollow">addon page</a>.

<b><code>TL;DR:</code></b>
Press F11 for fullscreen

<b><code>Features:</code></b>
- Press <b>F11</b> to enable or use menu option (View -&gt; Full Screen) <i>(hotkey can be changed in config)</i>
- <b>Hides all menu bars</b> including bottom bar ("More, Edit") and both top bars ("File, Edit..." and "Decks, Add...")
- <b>Superimposes answer buttons</b> over cards, with <b>adjustable opacity</b>. Becomes opaque on mouse-over <i>(color/opacity can be adjusted in config)</i>
- <b>Draggable answer buttons</b> that support touch. Position can be locked with right click option, hotkey or menu button <i>(hotkey can be changed in config)</i>
- <b>No Distractions Windowed Mode</b>: Same clean interface in a re-sizable window. Accessible through menu. Can set to <b>always be on top</b>
- Option to <b>hide mouse cursor if idle</b> <i>(idle time can be adjusted in config)</i>
- Allows card scrolling even with cursor over answer buttons (ideal for mouse users) <i>(can be disabled in config)</i>
- All cards types are compatible; cards are dynamically padded so that superimposed answer buttons do not obscure the bottom of cards when scrolled down (compatible with zoom addons)

<b><code>In Action:</code></b>
No Distractions Windowed Mode with translucent answer buttons enabled. Shown with <a href="https://ankiweb.net/shared/info/1829090218" rel="nofollow">Large and Colorful Buttons</a> addon:
<img src="https://i.ibb.co/dcvKWC8/ezgif-com-resize-2.gif">

<b><code>Notes:</code></b>
- <b>Software rendering is not supported.</b> The minority of users with hardware acceleration disabled may experience glitches. They should receive a popup warning when enabling fullscreen mode. <b>A compatibility mode is in the works</b>
- Please use the config to fine tune settings. Can be accessed through: <i>Tools-&gt;Options-&gt;Add-ons-&gt;No Distractions Full Screen-&gt;Config</i>. Detailed descriptions are within config.
- The F11 shortcut will automatically toggle the last enabled mode (either fullscreen or windowed)
- In Fullscreen mode, moving the mouse to the bottom of the screen will unhide answer buttons (if hidden)
- The answer buttons will snap back to their original location if dragged nearby. The position can also be reset through the menu options
- Tested compatibility with v2.1.15, v2.1.20, <a href="https://ankiweb.net/shared/info/1829090218" rel="nofollow">Large and Colorful Buttons</a>, <a href="https://ankiweb.net/shared/info/1496166067" rel="nofollow">Night Mode</a>, <a href="https://ankiweb.net/shared/info/538879081" rel="nofollow">Anki Zoom</a>, <a href="https://ankiweb.net/shared/info/1042429613" rel="nofollow">Large Fancy Buttons</a>, <a href="https://ankiweb.net/shared/info/1046608507" rel="nofollow">Speed Focus Mode</a>, <a href="https://ankiweb.net/shared/info/1758045507" rel="nofollow">Anki Habitica</a>, <a href="https://ankiweb.net/shared/info/1933645497" rel="nofollow">Fill the blanks</a>, <a href="https://ankiweb.net/shared/info/385888438" rel="nofollow">Edit field during review</a>

<b><code>Changelog:</code></b>
3/1/2020 v3.2.1: Fixed error on linux machines
2/29/2020 v3.2: Scrolling over answer buttons now scrolls cards, can be changed in config. Refactored code with minor performance improvements. Added manifest file. Bug fixes: more consistent answer button opacity transitions while changing cards and dragging
2/28/2020 v3.1.2: Bug fixes: improved compatibility with other addons, answer buttons no longer briefly shift to origin after a new card, adjusted render sequence/delay to cause less flickering
2/27/2020 v3.0:
- Added draggable answer buttons (uses interact.js)
- Rewrote bottom widget (again) to allow better interaction with cards (previously inputs would not register in bottom of screen)
- Added subtle fade animation to non-opaque answer buttons
- Added user-configurable delay when redrawing widgets to reduce flicker/artifacts (see config for more info)
- Added new config and renamed fullscreen hotkey in config - <b>users that used custom hotkeys prior should re-map</b>
- Fixed bug with where always-on-top toggle would not reset
- Added warning popup for software rendering
2/20/2020 v2.3.5: Rewrote cursor hide method to be more robust (now supports {type} cards)
2/10/2020 v2.3.4: Added remappable hotkey to config. Bug fixes (adding cards now reveals cursor - thanks for bug submission)
2/10/2020 v2.3.3: Removed limitation of full screen only in review. Added border color config option
2/10/2020 v2.3.2: Performance improvements
2/9/2020: v2.3: Added windowed mode. Added dynamic padding to bottom of cards. Rewrote display widget
2/9/2020: v2.2.2: Added idle mouse hide feature. Added user-adjustable config. Bug fixes (now behaves properly when burying/suspending cards in full screen)
2/4/2020: v2.1.1: Fixed bug where you could not exit full screen after finishing review - now automatically exits
2/2/2020: v2.1: Added customizable answer button opacity
2/1/2020: v2.0: Now hides bottom bar with floating answer buttons

Big thanks to glutanimate's Toggle Full Screen Extended, <a href="https://ankiweb.net/shared/info/1612375712" rel="nofollow">Full Screen Toggle</a>, <a href="https://ankiweb.net/shared/info/1214415810" rel="nofollow">HTML Window Source</a> and <a href="https://ankiweb.net/shared/info/31746032" rel="nofollow">AnkiWebView Inspector</a>
