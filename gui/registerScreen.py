import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
from utils.password_cover import Password_Text

class RegisterScreen(arcade.View):
    """
    Ekran rejestracji użytkownika.

    Umożliwia wpisanie nazwy użytkownika, emaila, hasła oraz powtórzenia hasła.
    Obsługuje walidację pól oraz przekierowuje do głównego menu po poprawnej rejestracji.
    """

    def __init__(self):
        """
        Inicjalizuje widok rejestracji.

        Tworzy pola tekstowe do wpisania nazwy użytkownika, emaila, hasła
        i powtórzenia hasła oraz przyciski zatwierdzenia i powrotu.
        """
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()

        anchor = UIAnchorLayout()
        self.vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        self.username_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(UILabel(text="Username", font_size=14, text_color=arcade.color.WHITE))
        self.vbox.add(self.username_input)

        self.email_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(UILabel(text="Email", font_size=14, text_color=arcade.color.WHITE))
        self.vbox.add(self.email_input)

        self.vbox.add(UILabel(text="Password", font_size=14, text_color=arcade.color.WHITE))
        self.password_input = Password_Text(width=300, height=30)
        self.vbox.add(self.password_input)

        self.vbox.add(UILabel(text="Repeat password", font_size=14, text_color=arcade.color.WHITE))
        self.repeat_password_input = Password_Text(width=300, height=30)
        self.vbox.add(self.repeat_password_input)

        self.error_label = UILabel(text="", font_size=14, text_color=arcade.color.RED)
        self.vbox.add(self.error_label)

        submit_button = UIFlatButton(text="Submit", width=200)
        self.vbox.add(submit_button)

        @submit_button.event("on_click")
        def on_submit(event):
            username = self.username_input.text.strip()
            password = self.password_input.get_password().strip()
            repeat_password = self.repeat_password_input.get_password().strip()
            email = self.email_input.text.strip()

            if not username or not password or not repeat_password or not email:
                self.error_label.text = "Wszystkie pola muszą być wypełnione."
                return

            if password != repeat_password:
                self.error_label.text = "Hasła się nie zgadzają."
                return

            self.error_label.text = ""
            from services.register_logic import register
            register(username, password, email)
            from gui.mainMenu import MainMenu
            import globals.user_id
            self.manager.clear()
            main_menu = MainMenu(globals.user_id.current_user)
            self.window.show_view(main_menu)
            print(globals.user_id.current_user)
        back_button = UIFlatButton(text="Back to Menu", width=200)
        self.vbox.add(back_button)

        @back_button.event("on_click")
        def on_back(event):
            from gui.startingScreen import StartingScreen
            self.manager.clear()
            starting_screen = StartingScreen()
            self.window.show_view(starting_screen)

        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)
    def on_show_view(self):
        """
        Wywoływane po pokazaniu widoku.

        Czyści ekran i rysuje UI.
        """
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        """
        Wywoływane po ukryciu widoku.

        Wyłącza menedżera UI, aby zwolnić zasoby.
        """
        self.manager.disable()
        self.manager.clear()


    def on_draw(self):
        """
        Rysuje widok rejestracji.

        Czyści ekran i rysuje UI.
        """
        self.clear()
        self.manager.draw()




