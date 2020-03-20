## NDFS v4.0 Config:

#### <span style="color:mediumaquamarine">If you are updating from an old version,</span> many values may be obsolete. Please note your current config and click "Restore Defaults" clean up config.  

#### The most useful config is outlined below. (Modifying other values may have unintended consequences - please click "Restore Defaults" if having issues.)  

#### All changes are effective immediately. Note: Changing settings through menu buttons will override respective values.  

#### Please report bugs/feature requests to [Github](https://github.com/Quip13/No-Distractions-Full-Screen/issues) or email at random.emailforcrap@gmail.com (yes it's real &#9786;)  


-  <span style="color:dodgerblue">**`MS_Windows_fullscreen_compatibility_mode`**</span>:
  Only applies to Microsoft Windows. Enabled by default; resolves numerous graphical issues when in Fullscreen mode (e.g. persistent task bar, flickering with overlays, hidden right click-menus).  
  <span style="color:indianred">If still experiencing fullscreen graphical issues in Windows, try setting to `false`.

-  <span style="color:dodgerblue">**`answer_button_border_color_normal`**</span>,  
  <span style="color:dodgerblue">**`answer_button_border_color_night`**</span>:  
  Color of border around answer buttons for normal/night mode. Supports both Night Mode Addon (1496166067) and native Anki Night Mode. Accepts HTML color codes. For help, see: [Color Picker](https://www.hexcolortool.com/#6e6e6e,0.8)  

-  <span style="color:dodgerblue">**`answer_button_opacity`**</span>: Pre-mouse-hover opacity of the answer buttons  
  <span style="color:indianred">`0` = hidden, `1` = solid. Must add leading 0 (e.g. `0.5`)</span>

-  <span style="color:dodgerblue">**`cursor_idle_timer`**</span>: Milliseconds to wait before hiding mouse

-  <span style="color:dodgerblue">**`fullscreen_hotkey`**</span>: Keybinding that toggles fullscreen/windowed mode  
  <span style="color:indianred">Examples:  `F11`,  `Ctrl+F`,  `Shift+D`,  `P`. For more details, see: [QKeySequence](https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html?highlight=qkeysequence#PySide2.QtGui.QKeySequence)</span>

-  <span style="color:dodgerblue">**`lock_answer_bar_hotkey`**</span>: Keybinding that toggles whether the answer bar should be draggable  

-  <span style="color:dodgerblue">**`rendering_delay`**</span>: Milliseconds to wait before window is updated with layout changes. Helps reduce flickering and artifacts when toggling fullscreen/windowed.  
  <span style="color:indianred">Can be adjusted depending on your machine and preferences. Higher values = cleaner transitions, but less responsive toggling</span>
