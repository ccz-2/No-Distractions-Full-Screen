### NDFS v3.2.4 Config:
The most useful config is outlined below. (Modifying other values may have unintended consequences - please click "Restore Defaults" if having issues.)  
All changes are effective immediately. Note: Changing settings through menu buttons will override respective values.  

-   `answer_button_border_color`: Color of border around answer buttons  
  Accepts HTML color codes. For help, see: [Color Picker](https://www.hexcolortool.com/#6e6e6e,0.8)  
  Suggested values for dark mode: `rgba(110, 110, 110, 0.8)` | light mode: `rgba(180, 180, 180, 0.8)` 

-   `answer_button_opacity`: Pre-mouse-hover opacity  
  `0` = hidden, `1` = solid. Must add leading 0 (e.g. `0.5`)

-   `cursor_idle_timer`: Milliseconds to wait before hiding mouse

-   `fullscreen_hotkey`: Keybinding that toggles fullscreen/windowed mode  
  Examples:  `F11`,  `Ctrl+F`,  `Shift+D`,  `P`  
  For more details, see: [QKeySequence](https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html?highlight=qkeysequence#PySide2.QtGui.QKeySequence)  

-   `ignore_scroll_on_answer_buttons`: If `true`, scrolling on answer buttons scrolls the card instead. Allows scrolling and answering cards with minimal mouse movement.

-   `lock_answer_bar_hotkey`: Keybinding that toggles whether the answer bar should be draggable  

-   `rendering_delay`: Milliseconds to wait before window is updated with layout changes. Helps reduce flickering and artifacts when toggling fullscreen/windowed.  
  Can be adjusted depending on your machine and preferences. Higher values = cleaner transitions, but less responsive toggling