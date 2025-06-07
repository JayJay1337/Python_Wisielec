import arcade
import random
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton, UIMessageBox, UIBoxLayout
from datetime import date
from models.category import Category
from models.word import Word
from models.session import SessionLocal
from utils.save_game_data import save_game_data
from globals.user_id import current_user


class EasyLevelScreen(arcade.View):
    """
    Ekran gry dla poziomu łatwego w grze wisielec.

    Odpowiada za logikę rozgrywki, wyświetlanie interfejsu użytkownika oraz obsługę zdarzeń.
    """

    def __init__(self, user_id: int):
        """
        Inicjalizuje ekran gry, ładując dane z bazy, konfigurując grę i interfejs.

        Args:
            user_id (int): ID aktualnie zalogowanego użytkownika.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.user_id = user_id
        self.manager = UIManager()
        self.manager.enable()

        self.timer = 0
        self.is_paused = False

        session = SessionLocal()
        easy_category = session.query(Category).filter(Category.name.ilike("EASY")).first()

        if easy_category:
            words_query = session.query(Word).filter(Word.category_id == easy_category.id).all()
            self.easy_words = [word.polish_word.upper() for word in words_query]
        else:
            self.easy_words = []

        session.close()

        if self.easy_words:
            self.current_word = random.choice(self.easy_words)
        else:
            self.current_word = "DOM"
            print("⚠️ Brak słów w bazie danych dla kategorii 'łatwy'")

        self.guessed_letters = set()
        self.wrong_letters = set()
        self.max_wrong = 6
        self.game_over = False
        self.game_won = False

        self.anchor = UIAnchorLayout()
        self.manager.add(self.anchor)

        self.back_button = UIFlatButton(text="Powrót do menu", width=150)
        self.anchor.add(child=self.back_button, anchor_x="left", anchor_y="bottom")

        @self.back_button.event("on_click")
        def on_click_back(event):
            """Obsługuje kliknięcie przycisku powrotu do menu."""
            print("Kliknięto przycisk powrotu do menu")
            self.show_confirmation()

        self.pause_button = UIFlatButton(text="PAUZA", width=100)
        self.anchor.add(child=self.pause_button, anchor_x="center", anchor_y="bottom")

        @self.pause_button.event("on_click")
        def on_click_pause(event):
            """Obsługuje kliknięcie przycisku pauzy gry."""
            self.toggle_pause()

        self.keyboard_layout = None
        self.keyboard_visible = True
        self.create_keyboard()

        self.level_label = arcade.Text(
            "Poziom Łatwy", 20, self.window.height - 20,
            arcade.color.WHITE, font_size=18, anchor_x="left", anchor_y="top"
        )

    def create_keyboard(self):
        """
        Tworzy interaktywną klawiaturę QWERTY jako zestaw przycisków UI.
        Każdy przycisk reprezentuje literę do odgadnięcia.
        """
        keyboard_layout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.keyboard_buttons = {}
        self.keyboard_layout = UIBoxLayout(vertical=True, space_between=5)

        for row in keyboard_layout:
            row_layout = UIBoxLayout(vertical=False, space_between=5)
            for letter in row:
                button = UIFlatButton(text=letter, width=40, height=40)

                @button.event("on_click")
                def on_letter_click(event, letter=letter):
                    if not self.is_paused and not self.game_over:
                        self.guess_letter(letter)
                        event.source.disabled = True

                self.keyboard_buttons[letter] = button
                row_layout.add(button)

            self.keyboard_layout.add(row_layout)

        self.anchor.add(child=self.keyboard_layout, anchor_x="center", anchor_y="center")

    def guess_letter(self, letter: str):
        """
        Przetwarza odgadnięcie litery przez gracza.

        Args:
            letter (str): Litera podana przez gracza.
        """
        if letter in self.current_word:
            self.guessed_letters.add(letter)
            print(f"Dobrze! Litera {letter} jest w słowie")
        else:
            self.wrong_letters.add(letter)
            print(f"Źle! Litery {letter} nie ma w słowie")

        if self.check_win():
            self.game_won = True
            self.game_over = True
            self.hide_keyboard()
            print("Wygrałeś!")
            save_game_data(user_id=self.user_id, time=self.timer, game_date=date.today(), category_id=1)
        elif len(self.wrong_letters) >= self.max_wrong:
            self.game_over = True
            self.hide_keyboard()
            print("Przegrałeś!")

    def hide_keyboard(self):
        """
        Dezaktywuje i ukrywa wszystkie przyciski klawiatury po zakończeniu gry.
        """
        if self.keyboard_visible:
            self.keyboard_visible = False
            for button in self.keyboard_buttons.values():
                button.disabled = True
                button.visible = False
            print("Klawiatura ukryta")

    def check_win(self) -> bool:
        """
        Sprawdza, czy wszystkie litery w słowie zostały poprawnie odgadnięte.

        Returns:
            bool: True jeśli gracz wygrał, False w przeciwnym razie.
        """
        return all(letter in self.guessed_letters for letter in self.current_word)

    def toggle_pause(self):
        """
        Przełącza stan pauzy gry oraz blokuje/odblokowuje interakcję z klawiaturą.
        """
        self.is_paused = not self.is_paused
        self.pause_button.text = "WZNÓW" if self.is_paused else "PAUZA"

        if self.keyboard_visible:
            for letter, button in self.keyboard_buttons.items():
                if letter not in self.guessed_letters and letter not in self.wrong_letters:
                    button.disabled = self.is_paused

    def draw_word(self):
        """
        Rysuje bieżące hasło na ekranie, pokazując zgadnięte litery oraz podkreślenia.
        """
        word_display = " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.current_word
        )
        x = self.window.width // 2
        y = self.window.height - 100

        arcade.Text(
            word_display.strip(), x, y,
            arcade.color.WHITE, font_size=36,
            anchor_x="center", anchor_y="center"
        ).draw()

    def draw_game_over_messages(self):
        """
        Wyświetla komunikaty o wygranej lub przegranej oraz dodatkowe informacje.
        """
        if self.game_over:
            cx, cy = self.window.width // 2, self.window.height // 2

            if self.game_won:
                arcade.Text("GRATULACJE!", cx, cy + 40, arcade.color.GREEN, 48, anchor_x="center").draw()
                time_text = f"Twój czas: {int(self.timer // 60):02d}:{int(self.timer % 60):02d}"
                arcade.Text(time_text, cx, cy, arcade.color.YELLOW, 24, anchor_x="center").draw()
            else:
                arcade.Text("PRZEGRANA!", cx, cy + 40, arcade.color.RED, 48, anchor_x="center").draw()
                arcade.Text(f"Hasło to było: {self.current_word}", cx, cy, arcade.color.WHITE, 24, anchor_x="center").draw()

    def draw_hangman(self):
        """
        Rysuje elementy szubienicy i postaci wisielca w zależności od liczby błędów.
        """
        wrong = len(self.wrong_letters)
        x, y = 100, 400

        if wrong >= 1:
            arcade.draw_line(x - 40, y - 100, x + 40, y - 100, arcade.color.BROWN, 5)
            arcade.draw_line(x, y - 100, x, y + 50, arcade.color.BROWN, 5)
            arcade.draw_line(x, y + 50, x + 50, y + 50, arcade.color.BROWN, 5)
            arcade.draw_line(x + 50, y + 50, x + 50, y + 30, arcade.color.BROWN, 3)
        if wrong >= 2:
            arcade.draw_circle_outline(x + 50, y + 15, 15, arcade.color.WHITE, 3)
        if wrong >= 3:
            arcade.draw_line(x + 50, y, x + 50, y - 40, arcade.color.WHITE, 3)
        if wrong >= 4:
            arcade.draw_line(x + 50, y - 10, x + 30, y - 25, arcade.color.WHITE, 3)
        if wrong >= 5:
            arcade.draw_line(x + 50, y - 10, x + 70, y - 25, arcade.color.WHITE, 3)
        if wrong >= 6:
            arcade.draw_line(x + 50, y - 40, x + 35, y - 60, arcade.color.WHITE, 3)
            arcade.draw_line(x + 50, y - 40, x + 65, y - 60, arcade.color.WHITE, 3)

    def draw_timer(self):
        """
        Wyświetla aktualny czas rozgrywki w prawym górnym rogu ekranu.
        """
        minutes = int(self.timer // 60)
        seconds = int(self.timer % 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"
        if self.is_paused:
            timer_text += " (PAUZA)"

        arcade.Text(
            timer_text, self.window.width - 20, self.window.height - 20,
            arcade.color.WHITE, font_size=18,
            anchor_x="right", anchor_y="top"
        ).draw()

    def draw_wrong_letters(self):
        """
        Wyświetla błędnie odgadnięte litery w dolnej części ekranu.
        """
        if self.wrong_letters:
            wrong_text = "Błędne: " + ", ".join(sorted(self.wrong_letters))
            arcade.Text(
                wrong_text, self.window.width // 2, 100,
                arcade.color.RED, font_size=16,
                anchor_x="center", anchor_y="center"
            ).draw()

    def show_confirmation(self):
        """
        Pokazuje okno potwierdzenia powrotu do menu głównego.
        """
        message_box = UIMessageBox(
            width=400,
            height=200,
            message_text="Obecna gra zostanie utracona.\nNa pewno chcesz wrócić do menu?",
            buttons=["Tak", "Nie"]
        )

        @message_box.event("on_action")
        def on_message_box_action(event):
            """
            Obsługuje kliknięcia w oknie potwierdzenia.

            Args:
                event: Zdarzenie zawierające wybraną akcję.
            """
            print(f"Akcja MessageBox: {event.action}")
            if event.action == "Tak":
                print("Wybrano TAK - powrót do menu")
                try:
                    from gui.mainMenu import MainMenu
                    self.manager.clear()
                    self.window.show_view(MainMenu(current_user))
                except Exception as e:
                    print(f"Błąd podczas powrotu do menu: {e}")
            try:
                self.manager.remove(message_box)
            except:
                pass

        self.manager.add(message_box)

    def on_update(self, delta_time: float):
        """
        Aktualizuje stan gry – głównie czas – jeśli gra nie jest w pauzie.

        Args:
            delta_time (float): Czas (w sekundach) od ostatniej aktualizacji.
        """
        if not self.is_paused and not self.game_over:
            self.timer += delta_time

    def on_draw(self):
        """
        Rysuje wszystkie elementy widoku gry.
        """
        self.clear()
        self.level_label.draw()
        self.draw_timer()
        self.draw_word()
        self.draw_hangman()
        if not self.game_over:
            self.draw_wrong_letters()
        self.draw_game_over_messages()
        self.manager.draw()

    def on_show_view(self):
        """
        Aktywuje menedżer UI po przełączeniu widoku na ten ekran.
        """
        self.manager.enable()

    def on_hide_view(self):
        """
        Dezaktywuje menedżer UI przy opuszczaniu widoku.
        """
        self.manager.disable()
