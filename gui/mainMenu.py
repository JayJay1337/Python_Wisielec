import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton, UIBoxLayout, UILabel

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton, UIBoxLayout, UILabel


class MainMenu(arcade.View):
    """
    Główne menu gry z przyciskami umożliwiającymi wybór poziomu trudności.

    Zawiera przyciski do przejścia na ekran poziomu łatwego i trudnego.
    """

    def __init__(self, user_id):
        """
        Inicjalizuje widok głównego menu.

        Ustawia tło, konfiguruje menedżera UI oraz dodaje przyciski do wyboru poziomu trudności.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.user_id = user_id
        self.manager = UIManager()
        self.manager.enable()
        anchor = UIAnchorLayout()

        self.vbox = UIBoxLayout(vertical=True, space_between=20)

        self.vbox.add(UILabel(text="USTAWIENIA", font_size=40, text_color=arcade.color.CYAN))

        # Przycisk poziomu łatwego
        easy_button = UIFlatButton(text="Poziom Łatwy", width=200)
        self.vbox.add(easy_button)

        @easy_button.event("on_click")
        def on_easy_click(event):
            """
            Obsługuje kliknięcie przycisku 'Poziom Łatwy'.

            Importuje widok EasyLevelScreen i zmienia widok aplikacji.
            """
            print("Kliknięto przycisk: Poziom Łatwy")  # Debug
            from gui.easyLevelScreen import EasyLevelScreen  # Upewnij się, że import jest poprawny
            self.window.show_view(EasyLevelScreen(self.user_id))  # Zmieniamy widok na EasyLevelScreen

        # Przycisk poziomu trudnego
        hard_button = UIFlatButton(text="Poziom Trudny", width=200)
        self.vbox.add(hard_button)

        @hard_button.event("on_click")
        def on_hard_click(event):
            """
            Obsługuje kliknięcie przycisku 'Poziom Trudny'.

            Importuje widok HardLevelScreen i zmienia widok aplikacji.
            """
            print("Kliknięto przycisk: Poziom Trudny")  # Debug
            from gui.hardLevelScreen import HardLevelScreen  # Upewnij się, że import jest poprawny
            self.window.show_view(HardLevelScreen(self.user_id))  # Zmieniamy widok na HardLevelScreen

        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")

        scoreboard_button = UIFlatButton(text="Tablica Wyników", width=200)
        self.vbox.add(scoreboard_button)
        @scoreboard_button.event("on_click")
        def on_scoreboard_click(event):
            from gui.scoreboard import ScoreBoard
            scoreboard = ScoreBoard()
            self.window.show_view(scoreboard)

        self.manager.add(anchor)

    def on_draw(self):
        """
        Rysuje ekran menu głównego.

        Czyści ekran i rysuje wszystkie elementy UI zarządzane przez UIManager.
        """
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        """
        Wywoływana przy ukryciu widoku.

        Dezaktywuje menedżera UI, aby nie reagował na zdarzenia.
        """
        self.manager.disable()

    def on_show_view(self):
        """
        Wywoływana przy ponownym pokazaniu widoku.

        Aktywuje menedżera UI, aby umożliwić interakcję z interfejsem.
        """
        self.manager.enable()

