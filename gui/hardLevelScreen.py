from datetime import date
import arcade
import random
from arcade.gui import UIManager, UIAnchorLayout, UIFlatButton, UIMessageBox, UIBoxLayout, UILabel
from models.category import Category
from models.word import Word
from models.session import SessionLocal
from utils.save_game_data import save_game_data



class HardLevelScreen(arcade.View):
    """
    Ekran trudnego poziomu gry wisielec.

    Obsługuje logikę gry: losowanie słowa, rysowanie wisielca,
    obsługę zgadywania liter, pauzy oraz zakończenia gry.
    """

    def __init__(self, user_id):
        """
        Inicjalizuje ekran, ładuje słowa z kategorii 'HARD' z bazy danych,
        tworzy UI i ustawia podstawowe parametry gry.
        """
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_RED)
        self.user_id = user_id
        self.manager = UIManager()
        self.manager.enable()

        # Timer
        self.timer = 0
        self.is_paused = False

        session = SessionLocal()
        hard_category = session.query(Category).filter(Category.name.ilike("HARD")).first()

        if hard_category:
            words_query = session.query(Word).filter(Word.category_id == hard_category.id).all()
            self.easy_words = [word.polish_word.upper() for word in words_query]
        else:
            self.easy_words = []

        session.close()

        if self.easy_words:
            self.current_word = random.choice(self.easy_words)
        else:
            self.current_word = "DOM"  # fallback
            print("⚠️ Brak słów w bazie danych dla kategorii 'trudny'")

        self.guessed_letters = set()
        self.wrong_letters = set()
        self.max_wrong = 5  # Mniej prób niż w łatwym
        self.game_over = False
        self.game_won = False

        self.anchor = UIAnchorLayout()
        self.manager.add(self.anchor)

        self.back_button = UIFlatButton(text="Powrót do menu", width=150)
        self.anchor.add(child=self.back_button, anchor_x="left", anchor_y="bottom")

        @self.back_button.event("on_click")
        def on_click_back(event):
            """
            Obsługa kliknięcia przycisku powrotu do menu.
            Pokazuje okno potwierdzenia przed wyjściem z gry.
            """
            print("Kliknięto przycisk powrotu do menu")
            self.show_confirmation()

        # Przycisk pauzy
        self.pause_button = UIFlatButton(text="PAUZA", width=100)
        self.anchor.add(child=self.pause_button, anchor_x="center", anchor_y="bottom")

        @self.pause_button.event("on_click")
        def on_click_pause(event):
            """
            Obsługa kliknięcia przycisku pauzy.
            Przełącza stan pauzy gry.
            """
            self.toggle_pause()

        # Klawiatura
        self.keyboard_layout = None
        self.keyboard_visible = True
        self.create_keyboard()

        # Teksty poziomu
        self.level_label = arcade.Text(
            "Poziom Trudny", 20, self.window.height - 20,
            arcade.color.WHITE, font_size=18, anchor_x="left", anchor_y="top"
        )

    def create_keyboard(self):
        """
        Tworzy UI klawiatury ekranowej z literami do zgadywania.
        Przypisuje event kliknięcia dla każdej litery.
        """
        keyboard_layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

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

    def guess_letter(self, letter):
        """
        Przetwarza zgadnięcie litery przez gracza.

        Dodaje literę do odpowiednich zbiorów zgadniętych lub błędnych,
        sprawdza warunki wygranej lub przegranej i odpowiednio aktualizuje stan gry.
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
            save_game_data(user_id=self.user_id, time=self.timer, game_date=date.today(), category_id=2)
        elif len(self.wrong_letters) >= self.max_wrong:
            self.game_over = True
            self.hide_keyboard()
            print("Przegrałeś!")

    def hide_keyboard(self):
        """
        Ukrywa i dezaktywuje klawiaturę ekranową po zakończeniu gry.
        """
        if self.keyboard_visible:
            self.keyboard_visible = False
            for button in self.keyboard_buttons.values():
                button.disabled = True
                button.visible = False
            print("Klawiatura ukryta")

    def check_win(self):
        """
        Sprawdza, czy gracz odgadł całe słowo.

        Zwraca True, jeśli wszystkie litery w słowie zostały odgadnięte.
        """
        for letter in self.current_word:
            if letter not in self.guessed_letters:
                return False
        return True

    def toggle_pause(self):
        """
        Przełącza stan pauzy gry.

        W czasie pauzy dezaktywuje aktywne przyciski liter.
        """
        self.is_paused = not self.is_paused
        pause_text = "WZNÓW" if self.is_paused else "PAUZA"
        self.pause_button.text = pause_text

        if self.keyboard_visible:
            for letter, button in self.keyboard_buttons.items():
                if letter not in self.guessed_letters and letter not in self.wrong_letters:
                    button.disabled = self.is_paused

    def draw_word(self):
        """
        Rysuje na ekranie aktualny stan odgadywanego słowa.

        Pokazuje odgadnięte litery i podkreślenia dla pozostałych.
        """
        word_display = ""
        for letter in self.current_word:
            if letter in self.guessed_letters:
                word_display += letter + " "
            else:
                word_display += "_ "

        x = self.window.width // 2
        y = self.window.height - 100

        arcade.Text(
            word_display.strip(), x, y,
            arcade.color.WHITE, font_size=36,
            anchor_x="center", anchor_y="center"
        ).draw()

    def draw_game_over_messages(self):
        """
        Wyświetla komunikaty o wygranej lub przegranej po zakończeniu gry.

        Pokazuje również czas rozgrywki lub hasło, jeśli gracz przegrał.
        """
        if self.game_over:
            center_x = self.window.width // 2
            center_y = self.window.height // 2

            if self.game_won:
                arcade.Text(
                    "GRATULACJE!", center_x, center_y + 40,
                    arcade.color.GREEN, font_size=48,
                    anchor_x="center", anchor_y="center"
                ).draw()

                minutes = int(self.timer // 60)
                seconds = int(self.timer % 60)
                time_text = f"Twój czas: {minutes:02d}:{seconds:02d}"
                arcade.Text(
                    time_text, center_x, center_y,
                    arcade.color.YELLOW, font_size=24,
                    anchor_x="center", anchor_y="center"
                ).draw()
            else:
                arcade.Text(
                    "PRZEGRANA!", center_x, center_y + 40,
                    arcade.color.RED, font_size=48,
                    anchor_x="center", anchor_y="center"
                ).draw()

                password_text = f"Hasło to było: {self.current_word}"
                arcade.Text(
                    password_text, center_x, center_y,
                    arcade.color.WHITE, font_size=24,
                    anchor_x="center", anchor_y="center"
                ).draw()

    def draw_hangman(self):
        """
        Rysuje stan wisielca w zależności od liczby błędnych liter.
        """
        wrong_count = len(self.wrong_letters)

        base_x = 100
        base_y = 400

        if wrong_count >= 1:
            arcade.draw_line(base_x - 50, base_y - 100, base_x + 50, base_y - 100, arcade.color.BROWN, 6)
            arcade.draw_line(base_x, base_y - 100, base_x, base_y + 60, arcade.color.BROWN, 6)
            arcade.draw_line(base_x, base_y + 60, base_x + 60, base_y + 60, arcade.color.BROWN, 6)
            arcade.draw_line(base_x + 60, base_y + 60, base_x + 60, base_y + 35, arcade.color.BROWN, 4)
            arcade.draw_line(base_x, base_y + 40, base_x + 20, base_y + 60, arcade.color.BROWN, 4)

        if wrong_count >= 2:
            arcade.draw_circle_outline(base_x + 60, base_y + 20, 15, arcade.color.WHITE, 4)
            arcade.draw_line(base_x + 55, base_y + 25, base_x + 60, base_y + 20, arcade.color.RED, 2)
            arcade.draw_line(base_x + 60, base_y + 25, base_x + 55, base_y + 20, arcade.color.RED, 2)
            arcade.draw_line(base_x + 65, base_y + 25, base_x + 70, base_y + 20, arcade.color.RED, 2)
            arcade.draw_line(base_x + 70, base_y + 25, base_x + 65, base_y + 20, arcade.color.RED, 2)

        if wrong_count >= 3:
            arcade.draw_line(base_x + 60, base_y + 5, base_x + 60, base_y - 40, arcade.color.WHITE, 4)

        if wrong_count >= 4:
            arcade.draw_line(base_x + 60, base_y - 10, base_x + 40, base_y - 30, arcade.color.WHITE, 4)
            arcade.draw_line(base_x + 60, base_y - 10, base_x + 80, base_y - 30, arcade.color.WHITE, 4)

        if wrong_count >= 5:
            arcade.draw_line(base_x + 60, base_y - 40, base_x + 45, base_y - 65, arcade.color.WHITE, 4)
            arcade.draw_line(base_x + 60, base_y - 40, base_x + 75, base_y - 65, arcade.color.WHITE, 4)

    def draw_timer(self):
        """
        Rysuje na ekranie aktualny czas gry oraz status pauzy.
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
        Wyświetla błędnie odgadnięte litery oraz liczbę pozostałych prób.
        """
        if self.wrong_letters:
            wrong_text = "Błędne: " + ", ".join(sorted(self.wrong_letters))
            arcade.Text(
                wrong_text, self.window.width // 2, 120,
                arcade.color.RED, font_size=16,
                anchor_x="center", anchor_y="center"
            ).draw()

        remaining = self.max_wrong - len(self.wrong_letters)
        remaining_text = f"Pozostałe próby: {remaining}"
        color = arcade.color.RED if remaining <= 2 else arcade.color.YELLOW
        arcade.Text(
            remaining_text, self.window.width // 2, 140,
            color, font_size=16,
            anchor_x="center", anchor_y="center"
        ).draw()

    def show_confirmation(self):
        """
        Pokazuje okno dialogowe z potwierdzeniem powrotu do menu.

        Po wybraniu "Tak" przełącza widok na menu główne.
        """
        message_box = UIMessageBox(
            width=400,
            height=200,
            message_text="Obecna gra zostanie utracona.\nNa pewno chcesz wrócić do menu?",
            buttons=["Tak", "Nie"]
        )

        @message_box.event("on_action")
        def on_message_box_action(event):
            print(f"Akcja MessageBox: {event.action}")

            if event.action == "Tak":
                print("Wybrano TAK - powrót do menu")
                try:
                    from gui.mainMenu import MainMenu
                    import globals.user_id
                    self.manager.clear()
                    main_menu = MainMenu(globals.user_id.current_user)
                    self.window.show_view(main_menu)
                except Exception as e:
                    print(f"Błąd podczas powrotu do menu: {e}")

            try:
                self.manager.remove(message_box)
            except:
                pass

        self.manager.add(message_box)

    def on_update(self, delta_time):
        """
        Aktualizuje timer gry, jeśli gra nie jest w pauzie i nie została zakończona.
        """
        if not self.is_paused and not self.game_over:
            self.timer += delta_time

    def on_draw(self):
        """
        Renderuje wszystkie elementy ekranu: teksty, wisielca,
        słowo, klawiaturę, timer oraz komunikaty końcowe.
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
        Aktywuje menedżera UI po wyświetleniu widoku.
        """
        self.manager.enable()

    def on_hide_view(self):
        """
        Dezaktywuje menedżera UI po ukryciu widoku.
        """
        self.manager.disable()