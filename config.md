## NDFS v3.2.7 Config:
### The most useful config is outlined below. (Modifying other values may have unintended consequences - please click "Restore Defaults" if having issues.)  

All changes are effective immediately. Note: Changing settings through menu buttons will override respective values. Some values may be obselete. Please click "Restore Defaults" to reset config and remove obselete values.

Please report bugs/feature requests to [Github](https://github.com/Quip13/No-Distractions-Full-Screen/issues) or email at random.emailforcrap@gmail.com (yes it's real &#9786;)  


-  <span style="color:dodgerblue">**`MS_Windows_fullscreen_compatibility_mode`**</span>:
  Only applies to Microsoft Windows. When enabled, resolves many graphical issues when in Fullscreen mode (e.g. flickering with addon alerts, hidden right click-menus).  
  <span style="color:indianred">If experiencing other fullscreen graphical issues (e.g. persistent taskbar), try setting to `false`. If still having issues, try setting `MS_Windows_force_FS_on_top` to `false`.</span>

  -  <span style="color:dodgerblue">**`MS_Windows_fullscreen_force_on_top`**</span>: Only applies to Microsoft Windows. If `true`, will also enable `MS_Windows_fullscreen_compatibility_mode` and force fullscreen window on top. Note that new windows (e.g. Card Editor or Browser) will not display over fullscreen mode.  
  <span style="color:indianred">Intended as a workaround for persistent taskbars on Windows despite `MS_Windows_fullscreen_compatibility_mode` being disabled.</span>

-  <span style="color:dodgerblue">**`answer_button_border_color`**</span>: Color of border around answer buttons. Accepts HTML color codes. For help, see: [Color Picker](https://www.hexcolortool.com/#6e6e6e,0.8)  
  <span style="color:indianred">Suggested values for dark mode: `rgba(110, 110, 110, 0.8)` | light mode: `rgba(180, 180, 180, 0.8)`</span>

-  <span style="color:dodgerblue">**`answer_button_opacity`**</span>: Pre-mouse-hover opacity of the answer buttons  
  <span style="color:indianred">`0` = hidden, `1` = solid. Must add leading 0 (e.g. `0.5`)</span>

-  <span style="color:dodgerblue">**`cursor_idle_timer`**</span>: Milliseconds to wait before hiding mouse

-  <span style="color:dodgerblue">**`fullscreen_hotkey`**</span>: Keybinding that toggles fullscreen/windowed mode  
  <span style="color:indianred">Examples:  `F11`,  `Ctrl+F`,  `Shift+D`,  `P`. For more details, see: [QKeySequence](https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html?highlight=qkeysequence#PySide2.QtGui.QKeySequence)</span>

-  <span style="color:dodgerblue">**`ignore_scroll_on_answer_buttons`**</span>: If `true`, scrolling over answer buttons is ignored and scrolls the card instead. Allows scrolling and answering cards with minimal mouse movement.

-  <span style="color:dodgerblue">**`lock_answer_bar_hotkey`**</span>: Keybinding that toggles whether the answer bar should be draggable  

-  <span style="color:dodgerblue">**`rendering_delay`**</span>: Milliseconds to wait before window is updated with layout changes. Helps reduce flickering and artifacts when toggling fullscreen/windowed.  
  <span style="color:indianred">Can be adjusted depending on your machine and preferences. Higher values = cleaner transitions, but less responsive toggling</span>