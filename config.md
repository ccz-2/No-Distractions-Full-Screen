## No Distractions Full Screen v4.1.8 Config:

#### Thanks for using NDFS! The most useful config is outlined below. (Modifying other values may have unintended consequences - please click "Restore Defaults" if having issues.)  

  Please report bugs/feature requests to [Github](https://github.com/Quip13/No-Distractions-Full-Screen/issues) or email at random.emailforcrap@gmail.com (yes it's real 😊). Note that the No Distractions <u>Answer Bar</u> uses a custom layout and may not play well with other addons. Feel free to report issues, and I will try my best, but widespread compatibility may not be possible.  

 <b><span style="color:mediumaquamarine">If you are updating from an old version,</span></b> many values may be obsolete. Please note your current config and click "Restore Defaults" to remove non-functional values.  

 <b><span style="color:mediumaquamarine">Changing the appearance of the No Distractions Answer Bar</span></b> can be done through the NDFS toolbar menu option (not here). However clicking "Restore Defaults" on this screen <u>will</u> reset your No Distractions Answer Bar appearance settings.

 <b><span style="color:mediumaquamarine">All changes are effective immediately.</span></b> Note that changing settings through menu buttons will override respective values.  

-  <span style="color:dodgerblue">**`MS_Windows_fullscreen_compatibility_mode`**</span>:
  Only applies to Microsoft Windows. Enabled by default; resolves numerous graphical issues when in Fullscreen mode (e.g. persistent task bar, flickering with overlays, hidden right click-menus).  
  <span style="color:indianred">If on Windows and experiencing grpahical issues, try setting to `false`.</span>

-  <span style="color:dodgerblue">**`answer_button_border_color_normal`**</span>,  
  <span style="color:dodgerblue">**`answer_button_border_color_night`**</span>:  
  Color of border around answer buttons for normal/night mode. Supports both the <u>Night Mode</u> Addon for legacy Anki versions and native Anki Night Mode. Accepts HTML color codes. For help, see: [Color Picker](https://www.hexcolortool.com/#6e6e6e,0.8)  
  <span style="color:indianred">This value is used in both the default answer bar and No Distractions Answer Bar</span> 

-  <span style="color:dodgerblue">**`answer_button_opacity`**</span>: Opacity of the answer buttons. Note that mouse-hovers will make the answer buttons opaque.  
  <span style="color:indianred">`0` = hidden, `1` = solid. Must add leading `0` (e.g. `0.5`)</span>  

-  <span style="color:dodgerblue">**`answer_conf_time`**</span>: Number of seconds the answer confirmation animation lasts. Only applies if No Distractions Answer Bar is enabled.  
  <span style="color:indianred">Setting to `0` will disable animation</span>  

-  <span style="color:dodgerblue">**`cursor_idle_timer`**</span>: Milliseconds to wait before hiding cursor.  
  <span style="color:indianred">Setting to `0` will keep cursor hidden even when moving. Negative values will disable cursor hide.</span>  

-  <span style="color:dodgerblue">**`fullscreen_hotkey`**</span>: Keybinding that toggles fullscreen/windowed mode  
  <span style="color:indianred">Examples:  `F11`,  `Ctrl+F`,  `Shift+D`,  `P`. For more details, see: [QKeySequence](https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html?highlight=qkeysequence#PySide2.QtGui.QKeySequence)</span>

-  <span style="color:dodgerblue">**`lock_answer_bar_hotkey`**</span>: Keybinding that toggles whether the answer bar should be draggable.  
  <span style="color:indianred">Examples:  `Ctrl+C`,  `Shift+R`. For more details, see: [QKeySequence](https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html?highlight=qkeysequence#PySide2.QtGui.QKeySequence)</span>

-  <span style="color:dodgerblue">**`rendering_delay`**</span>: Milliseconds to wait before window is updated with layout changes. Helps reduce flickering and artifacts when toggling fullscreen/windowed.  
  <span style="color:indianred">Can be adjusted depending on your computer speed and preferences. Higher values = cleaner transitions, but less responsive toggling.</span>
