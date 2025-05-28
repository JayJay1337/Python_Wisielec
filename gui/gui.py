import tkinter as tk
from tkinter import ttk, messagebox




def appScreen():
    root = tk.Tk()
    root.title("Wisielec!")
    root.geometry("800x600")
    root.resizable(False, False)


    #POLE Z NAPISEM
    welcome_label = ttk.Label(
        root,
        text="Witamy w grze Wisielec!",
        font=("Press Start 2P", 24),

    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")
    """
    settingsButton = ttk.Button(root , text="Ustawienia")
    settingsButton.place(relx=0.5, rely=0.2, anchor="center")
    """
    exitButton = ttk.Button(root , text="Wyjdź", command = root.destroy)
    exitButton.place(relx=0.5, rely=0.4, anchor="center")

    loginButton = ttk.Button(root, text="Zaloguj")
    loginButton.place(relx=0.5, rely=0.3, anchor="center")

    registerButton = ttk.Button(root, text="Zarejestruj się")
    registerButton.place(relx=0.5, rely=0.35, anchor="center")

    """
    #POLE DO WPISANIA NAZWY UZYTKOWNIKA
    username_label = ttk.Label(root, text="Wprowadź nazwę użytkownika:")
    username_label.place(relx=0.5, rely=0.25, anchor="center")
    username = ttk.Entry(root, width=30)
    username.place(relx=0.5, rely=0.3,anchor="center")
    """
    root.mainloop()
appScreen()