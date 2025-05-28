import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
from utils.displayScreen import displayScreen


class LoginScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        anchor = UIAnchorLayout()
        self.vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=10)


        self.username_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(UILabel(text="Username", font_size=14, text_color=arcade.color.WHITE))
        self.vbox.add(self.username_input)

        self.vbox.add(UILabel(text="Password", font_size=14, text_color=arcade.color.WHITE))
        self.password_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(self.password_input)

        # SUBMIT
        submit_button = UIFlatButton(text="Submit", width=200)
        self.vbox.add(submit_button)

        @submit_button.event("on_click")
        def on_submit(event):
            #print(f"Username: {self.username_input.text}")
            #print(f"Password: {self.password_input.text}")
            from mainMenu import MainMenu
            displayScreen(self.window, self.manager, MainMenu())


        back_button = UIFlatButton(text="Back to Menu", width=200)
        self.vbox.add(back_button)
        #BACK
        @back_button.event("on_click")
        def on_back(event):
            from startingScreen import StaringScreen
            displayScreen(self.window, self.manager, StaringScreen())

        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")


        self.manager.add(anchor)

    def on_show(self):
        self.clear()
        self.manager.draw()

    def on_hide(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


