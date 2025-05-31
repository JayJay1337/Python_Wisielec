import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
from utils.displayScreen import displayScreen
from utils.password_cover import Password_Text



class LoginScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        anchor = UIAnchorLayout()
        self.vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        #POLE TEKSTOWE USERNAME
        self.username_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(UILabel(text="Username", font_size=14, text_color=arcade.color.WHITE))
        self.vbox.add(self.username_input)
        #POLE TEKSTOWE PASSWORD
        self.vbox.add(UILabel(text="Password", font_size=14, text_color=arcade.color.WHITE))
        self.password_input = Password_Text(width=300, height=30)
        self.vbox.add(self.password_input)

        self.error_label = UILabel(text="", font_size=14, text_color=arcade.color.RED)
        self.vbox.add(self.error_label)

        #PRZYCISK SUBMIT
        submit_button = UIFlatButton(text="Submit", width=200)
        self.vbox.add(submit_button)

        @submit_button.event("on_click")
        def on_submit(event):
            username = self.username_input.text.strip()
            password = self.password_input.get_password().strip()
            from services.login_logic import login
            if username == "" or password == "":
                self.error_label.text = "Wszystkie pola muszą być wypełnione."
                return
            elif login(username, password) == False:
                self.error_label.text="Niepoprawna nazwa użytkownika lub hasło"
                return
            from gui.mainMenu import MainMenu
            displayScreen(self.window, self.manager, MainMenu())


        back_button = UIFlatButton(text="Back to Menu", width=200)
        self.vbox.add(back_button)

        #PRZYCISK BACK
        @back_button.event("on_click")
        def on_back(event):
            from gui.startingScreen import StartingScreen
            displayScreen(self.window, self.manager, StartingScreen())

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


