import gc
import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout

class StartingScreen(arcade.View):
    """
    StartingScreen to ekran początkowy gry Hangman.

    Zawiera przyciski umożliwiające zalogowanie się, rejestrację lub wyjście z gry.
    Obsługuje również wyświetlanie tytułu gry i zarządzanie interfejsem użytkownika.
    """

    def __init__(self):
        """
        Inicjalizuje StartingScreen: ustawia tło, tytuł, interfejs GUI i obsługę przycisków.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()

        self.title_text = arcade.Text(
            "HANGMAN",
            self.window.width // 2,
            self.window.height - 100,
            color=arcade.color.AQUA,
            font_size=60,
            anchor_x="center",
            anchor_y="top",
            font_name="Kenney Future"
        )

        anchor = UIAnchorLayout()
        self.vbox = UIBoxLayout(vertical=True, space_between=20)

        login_button = UIFlatButton(text="Login", width=200)
        self.vbox.add(login_button)

        @login_button.event("on_click")
        def on_click_login(event):
            """
            Obsługuje kliknięcie przycisku 'Login'.
            Przełącza widok na ekran logowania.
            """
            print("Logged in")
            from gui.loginScreen import LoginScreen
            self.manager.clear()
            login_screen = LoginScreen()
            self.window.show_view(login_screen)

        register_button = UIFlatButton(text="Register", width=200)

        @register_button.event("on_click")
        def on_click_register(event):
            """
            Obsługuje kliknięcie przycisku 'Register'.
            Przełącza widok na ekran rejestracji.
            """
            print("Registered")
            from gui.registerScreen import RegisterScreen
            self.manager.clear()
            register_screen = RegisterScreen()
            self.window.show_view(register_screen)
        self.vbox.add(register_button)

        exit_button = UIFlatButton(text="Exit", width=200)

        @exit_button.event("on_click")
        def on_click_exit(event):
            """
            Obsługuje kliknięcie przycisku 'Exit'.
            Zamyka grę.
            """
            print("Exiting...")
            arcade.close_window()

        self.vbox.add(exit_button)

        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def on_draw(self):
        """
        Renderuje ekran: czyści tło, rysuje tytuł oraz GUI.
        """
        self.clear()
        self.title_text.draw()
        self.manager.draw()

    def on_hide_view(self):
        """
        Wywoływane po ukryciu widoku.

        Wyłącza menedżera UI, aby zwolnić zasoby.
        """
        self.manager.disable()
        self.manager.clear()

    def on_show_view(self):
        """
        Aktywuje menedżer GUI przy ponownym pokazaniu widoku.
        """
        self.manager.enable()


