from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
def displayScreen(window, manager, new_view):
    manager.disable()
    window.show_view(new_view)