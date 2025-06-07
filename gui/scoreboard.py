import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton, UIBoxLayout, UILabel
from globals.user_id import current_user

class ScoreBoard(arcade.View):
    """
    Widok tablicy wyników gry.

    Wyświetla listę wyników graczy dla poziomu łatwego i trudnego.
    """

    def __init__(self):
        """
        Inicjalizuje UI tablicy wyników, tworzy strukturę layoutów
        i dodaje przycisk powrotu do menu głównego.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.manager = UIManager()
        self.manager.enable()

        self.main_vbox = UIBoxLayout(vertical=False, space_between=200)

        self.left_top_vbox = UIBoxLayout(vertical=False, space_between=10)
        self.left_top_vbox.add(UILabel(text="Nazwa", bold=True))
        self.left_top_vbox.add(UILabel(text="Czas", bold=True))

        self.left_vbox = UIBoxLayout(vertical=True, space_between=10)
        self.left_vbox.add(UILabel(text="Poziom trudny", bold =True))
        self.left_vbox.add(self.left_top_vbox)

        self.right_top_vbox = UIBoxLayout(vertical=False, space_between=10)
        self.right_top_vbox.add(UILabel(text="Nazwa", bold=True))
        self.right_top_vbox.add(UILabel(text="Czas", bold=True))

        self.right_vbox = UIBoxLayout(vertical=True, space_between=10)
        self.right_vbox.add(UILabel(text="Poziom łatwy", bold =True))
        self.right_vbox.add(self.right_top_vbox)

        self.main_vbox.add(self.left_vbox)
        self.main_vbox.add(self.right_vbox)
        anchor_center = UIAnchorLayout()
        self.title_label = UILabel(text="Tablica wyników", font_size=40, bold=True, text_color=arcade.color.CYAN)

        self.root_vbox = UIBoxLayout(vertical=True, space_between=20)
        self.root_vbox.add(self.title_label)
        self.root_vbox.add(self.main_vbox)

        anchor_center.add(child=self.root_vbox, anchor_x="center", anchor_y="top")
        self.manager.add(anchor_center)
        self.back_button = UIFlatButton(text="Powrót do menu", width=150)

        @self.back_button.event("on_click")
        def on_click_back(event):
            """
            Obsługa kliknięcia przycisku powrotu do menu głównego.
            Przełącza widok na MainMenu.
            """
            from gui.mainMenu import MainMenu
            import globals.user_id
            self.manager.clear()
            main_menu = MainMenu(globals.user_id.current_user)
            self.window.show_view(main_menu)

        anchor_bottom = UIAnchorLayout()
        anchor_bottom.add(child=self.back_button, anchor_x="center", anchor_y="bottom")
        self.manager.add(anchor_bottom)

    def load_scores(self):
        """
        Ładuje i wyświetla wyniki graczy z różnych poziomów trudności
        (łatwy – ID 1, trudny – ID 2) na tablicy wyników.
        """
        from utils.get_users_score import get_users_score
        all_users = get_users_score()
        for user in all_users:
            print(f"User: {user.username}")
            row = UIBoxLayout(vertical=False, space_between=10)
            row.add(UILabel(text=user.username))
            row.add(UILabel(text=str(user.time)))

            if user.category_id == 2:
                self.left_vbox.add(row)
            elif user.category_id == 1:
                self.right_vbox.add(row)

    def on_show_view(self):
        """
        Wywoływana po pokazaniu widoku.
        Czyści ekran i ładuje wyniki graczy.
        """
        self.clear()
        self.load_scores()

    def on_hide_view(self):
        """
        Wywoływana po ukryciu widoku.
        Dezaktywuje i czyści menedżera UI.
        """
        self.manager.disable()
        self.manager.clear()

    def on_draw(self):
        """
        Renderuje UI tablicy wyników na ekranie.
        """
        self.clear()
        self.manager.draw()
