# Gra Wisielec

Klasyczna gra wisielec napisana w Pythonie z wykorzystaniem Arcade. Projekt powstał jako praca zaliczeniowa i zawiera system użytkowników oraz ranking wyników.

## Funkcje

- Logowanie i rejestracja użytkowników z hashowaniem haseł (bcrypt)
- Dwa poziomy trudności (łatwy i trudny)
- Timer mierzący czas gry z możliwością pauzy
- Ranking najlepszych wyników posortowany po czasie
- Graficzny interfejs z interaktywną klawiaturą QWERTY
- Progresywne rysowanie wisielca w zależności od błędów

## Wymagania

- Python 3.8+
- arcade
- sqlalchemy 
- bcrypt

## Instalacja

git clone [url-repo]
cd projekt_wisielec
pip install arcade sqlalchemy bcrypt
python main.py

## Struktura projektu

projekt_wisielec/
├── globals/
│   └── user_id.py          # globalna zmienna aktualnego użytkownika
├── gui/                    # wszystkie ekrany gry
│   ├── startingScreen.py   # ekran powitalny
│   ├── loginScreen.py      # logowanie
│   ├── registerScreen.py   # rejestracja
│   ├── mainMenu.py         # menu główne
│   ├── easyLevelScreen.py  # poziom łatwy
│   ├── hardLevelScreen.py  # poziom trudny
│   └── scoreboard.py       # ranking
├── models/                 # modele SQLAlchemy
│   ├── user.py            # model użytkownika
│   ├── game_data.py       # dane gier
│   ├── category.py        # kategorie słów
│   └── word.py            # słowa
├── services/              # logika biznesowa
│   ├── login_logic.py     # weryfikacja logowania
│   ├── register_logic.py  # rejestracja użytkowników
│   ├── save_game_data.py  # zapis wyników
│   └── get_users_score.py # pobieranie rankingu
├── utils/
│   ├── init_db.py         # inicjalizacja bazy danych
│   └── password_cover.py  # maskowanie hasła gwiazdkami
└── main.py

## Implementacja

### System użytkowników
Hasła są hashowane przy pomocy bcrypt przed zapisem do bazy:
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

Przy logowaniu sprawdzane jest czy podane hasło pasuje do hasha:
if user and bcrypt.checkpw(password.encode(), user.password.encode()):
    return user

### Logika gry
Główna pętla gry znajduje się w klasach EasyLevelScreen i HardLevelScreen. Każda litera na klawiaturze to osobny przycisk z callbackiem:

- guess_letter() - sprawdza czy litera występuje w słowie
- check_win() - weryfikuje czy wszystkie litery zostały odgadnięte
- draw_hangman() - rysuje kolejne części wisielca przy błędach
- toggle_pause() - zatrzymuje/wznawia timer

### Baza danych
SQLAlchemy z SQLite przechowuje:
- *Users*: id, username, password (hash), email
- *Categories*: id, name (EASY/HARD)
- *Words*: id, polish_word, category_id
- *GameData*: id, user_id, time, game_date, category_id

Relacje między tabelami przez foreign keys.

### Timer
Timer działa na delta_time z Arcade i formatuje czas do MM:SS. Podczas pauzy delta_time nie jest dodawane do całkowitego czasu.

## Jak grać

1. Zarejestruj się lub zaloguj (hasło będzie maskowane gwiazdkami)
2. Wybierz poziom trudności z menu
3. Klikaj litery na klawiaturze ekranowej
4. Masz 6 prób na łatwym (5 na trudnym)
5. Użyj przycisku PAUZA żeby zatrzymać timer

Gra automatycznie zapisuje wyniki po wygranej i pokazuje je w rankingu.

## Poziomy trudności

*Łatwy*: 6 prób, słowa z kategorii "EASY", podstawowa grafika wisielca
*Trudny*: 5 prób, słowa z kategorii "HARD", bardziej szczegółowa grafika wisielca

Słowa są losowo wybierane z odpowiedniej kategorii przy starcie gry.


## Autorzy

Jakub Juściński i Magdalena Sroka
