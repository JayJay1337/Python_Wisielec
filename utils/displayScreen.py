from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
#ZMIANA SCEN
def displayScreen(window, manager, new_view):
    manager.disable()
    window.show_view(new_view)