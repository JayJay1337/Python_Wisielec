from arcade.gui import UIInputText, UIEvent


#GWIAZDKOWANIE HASŁA
class Password_Text(UIInputText):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.real_password = ""

    def on_event(self, event):
        handled = super().on_event(event)
        if len(self.text) > len(self.real_password):
            char = self.text[0]
            self.real_password += char
        elif len(self.text) < len(self.real_password):
            self.real_password = self.real_password[:len(self.text)]
        self.text = "*" * len(self.text)

        return handled

    def get_password(self):
        return self.real_password
