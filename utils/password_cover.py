from arcade.gui import UIInputText, UIEvent

# GWIAZDKOWANIE HASŁA
class Password_Text(UIInputText):
    """
    Klasa UIInputText służąca do wprowadzania hasła z automatycznym maskowaniem (gwiazdkowaniem).

    Tekst wpisywany przez użytkownika jest wyświetlany jako ciąg gwiazdek '*',
    natomiast rzeczywista wartość hasła przechowywana jest wewnętrznie w `real_password`.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje komponent pola tekstowego do wprowadzania hasła.

        Args:
            **kwargs: Parametry przekazywane do konstruktora klasy nadrzędnej UIInputText.
        """
        super().__init__(**kwargs)
        self.real_password = ""

    def on_event(self, event):
        """
        Obsługuje zdarzenia związane z edycją tekstu.

        Zamiast faktycznie wpisywanego tekstu, w polu pojawiają się gwiazdki,
        a wpisywana treść przechowywana jest w `real_password`.

        Args:
            event (UIEvent): Zdarzenie interfejsu użytkownika.

        Returns:
            bool: True, jeśli zdarzenie zostało obsłużone; False w przeciwnym razie.
        """
        handled = super().on_event(event)
        if len(self.text) > len(self.real_password):
            char = self.text[0]
            self.real_password += char
        elif len(self.text) < len(self.real_password):
            self.real_password = self.real_password[:len(self.text)]
        self.text = "*" * len(self.text)

        return handled

    def get_password(self):
        """
        Zwraca rzeczywistą treść wpisanego hasła (niemaskowaną).

        Returns:
            str: Prawdziwe hasło wprowadzone przez użytkownika.
        """
        return self.real_password
