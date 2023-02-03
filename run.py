"""
1. Get the date and weather
2. return the birthday
3. Continue receiving input of time. Also optional of the person's name


python run.py
"""
import json
import sys

from enum import Enum

VILLAGERS = [
    'Alex',
    'Elliot',
    'Harvey',
    'Sam',
    'Sebastian',
    'Shane',
    'Abigail',
    'Emily',
    'Haley',
    'Leah',
    'Maru',
    'Penny',
    'Caroline',
    'Clint',
    'Demetrius',
    'Dwarf',
    'Evelyn',
    'George',
    'Gus',
    'Jas',
    'Jodi',
    'Kent',
    'Krobus',
    'Leo',
    'Lewis',
    'Linus',
    'Marnie',
    'Pam',
    'Pierre',
    'Robin',
    'Sandy',
    'Vincent',
    'Willy',
    'Wizard',
]

DATA = {}

class Season(Enum):
    SPRING = 1
    SUMMER = 2
    FALL = 3
    WINTER = 4


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Validator:
    @classmethod
    def validate_season_input(cls, season_input):
        if season_input not in {"1", "2", "3", "4"}:
            raise ValueError(f"{season_input} is not a valid season.")
        else:
            return Season(int(season_input))

    @classmethod
    def validate_date_input(cls, date_input):
        if int(date_input) not in range(1, 29):
            raise ValueError(f"Date should be between 1 and 28")
        else:
            return int(date_input)


class Villager:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.parse_birthday()

    def parse_birthday(self):
        birthday = self.data["basic"]["Birthday"]
        self.birthday_season = Season[birthday.split(' ')[0].upper()]
        self.birthday_date = int(birthday.split(' ')[-1])

    @property
    def best_gifts(self):
        return self.data["basic"]["Best Gifts"]


def get_birthday_people(season, date):
    birthday_people = []
    for villager_name, villager in DATA.items():
        if villager.birthday_season == season and villager.birthday_date == date:
            birthday_people.append(villager)

    print("╔═════════════════✿═════════════════╗")
    print(f" {season.name} {date}")
    print(" ---------------------------------- ")
    if birthday_people:
        for birthday_person in birthday_people:
            print(f" It is {bcolors.HEADER}{birthday_person.name}'s{bcolors.ENDC} birthday.")
            print(f" Their favorite gifts are")
            for gift in birthday_person.best_gifts:
                print(f"  - {gift}.")
    else:
        print(" There is no birthday today.")
    print("╚═════════════════✿═════════════════╝")


def load_data():
    global DATA
    folder_path = 'villagers/parsed'
    for villager in VILLAGERS:
        with open(f'{folder_path}/{villager}.json', 'r') as f:
            DATA[villager] = Villager(villager, json.load(f))


if __name__ == "__main__":
    print("Welcome Mark and Irene's Stardew Valley")
    print("---------------------------------------")

    print("Loading data...")
    data = load_data()
    print("Data loaded successfully.\n")

    season_input = input("Please enter the current season (1-Spring, 2-Summer, 3-Fall, 4-Winter): ")
    season = Validator.validate_season_input(season_input)

    date_input = input("Please enter the date (1-28): ")
    date = Validator.validate_date_input(date_input)

    get_birthday_people(season, date)
    
    while True:
        print("What do you want to do next?")
        print("You can enter:")
        print("1 - To go to the next day")
        print("2 - Get location of a villager")
        print("3 - Get location of all the villagers")
        print("4 - Exit program")
        command = input("Enter: ")


