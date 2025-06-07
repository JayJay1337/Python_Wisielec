import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
from utils.password_cover import Password_Text



class LoginScreen(arcade.View):
    """
    Ekran logowania użytkownika.

    Zawiera pola do wpisania nazwy użytkownika i hasła,
    przyciski do zatwierdzenia i powrotu do menu oraz komunikaty błędów.
    """

    def __init__(self):
        """
        Inicjalizuje ekran logowania, tworzy UI (pola tekstowe, etykiety, przyciski)
        oraz ustawia obsługę zdarzeń dla przycisków Submit i Back.
        """
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        anchor = UIAnchorLayout()
        self.vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        # Pole tekstowe username
        self.username_input = arcade.gui.UIInputText(width=300, height=30)
        self.vbox.add(UILabel(text="Username", font_size=14, text_color=arcade.color.WHITE))
        self.vbox.add(self.username_input)

        # Pole tekstowe password
        self.vbox.add(UILabel(text="Password", font_size=14, text_color=arcade.color.WHITE))
        self.password_input = Password_Text(width=300, height=30)
        self.vbox.add(self.password_input)

        # Etykieta błędu
        self.error_label = UILabel(text="", font_size=14, text_color=arcade.color.RED)
        self.vbox.add(self.error_label)

        # Przycisk submit
        submit_button = UIFlatButton(text="Submit", width=200)
        self.vbox.add(submit_button)

        @submit_button.event("on_click")
        def on_submit(event):
            """
            Obsługuje kliknięcie przycisku Submit.

            Sprawdza poprawność wprowadzonych danych (username i password).
            W przypadku błędu wyświetla odpowiedni komunikat.
            Przy poprawnym logowaniu przechodzi do menu głównego.
            """
            username = self.username_input.text.strip()
            password = self.password_input.get_password().strip()
            from services.login_logic import login
            if username == "" or password == "":
                self.error_label.text = "Wszystkie pola muszą być wypełnione."
                return
            user = login(username, password)
            if not user:
                self.error_label.text = "Niepoprawna nazwa użytkownika lub hasło"
                return
            from gui.mainMenu import MainMenu
            import globals.user_id
            self.manager.clear()
            main_menu = MainMenu(globals.user_id.current_user)
            self.window.show_view(main_menu)

        # Przycisk back
        back_button = UIFlatButton(text="Back to Menu", width=200)
        self.vbox.add(back_button)

        @back_button.event("on_click")
        def on_back(event):
            """
            Obsługuje kliknięcie przycisku Back.

            Przechodzi do ekranu startowego aplikacji.
            """
            from gui.startingScreen import StartingScreen
            self.manager.clear()
            starting_screen = StartingScreen()
            self.window.show_view(starting_screen)

        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def on_show_view(self):
        """
        Wywoływane przy pokazaniu widoku.

        Czyści ekran i rysuje UI.
        """
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        """
        Wywoływane przy ukryciu widoku.

        Wyłącza menedżera UI, aby zwolnić zasoby.
        """
        self.manager.disable()
        self.manager.clear()

    def on_draw(self):
        """
        Rysuje widok na ekranie.

        Czyści ekran i rysuje menedżera UI.
        """
        self.clear()
        self.manager.draw()



