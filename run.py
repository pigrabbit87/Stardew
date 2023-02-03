"""
1. Get the date and weather
2. return the birthday
3. Continue receiving input of time. Also optional of the person's name


python run.py
"""
import json
import sys

from enum import Enum

from models.command import Command

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

# Global variabls
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

    @classmethod
    def validate_command(cls, command_input):
        try:
            return Command(int(command_input))
        except ValueError:
            print(f"{command_input} is not a valid command.")


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


class Stardew:
    def __init__(self, season, date):
        self.season = season
        self.date = date

    def get_birthday_people(self):
        birthday_people = []
        for villager_name, villager in DATA.items():
            if villager.birthday_season == self.season and villager.birthday_date == self.date:
                birthday_people.append(villager)

        print("╔═════════════════✿═════════════════╗")
        print(f" {self.season.name} {self.date}")
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

    def to_next_day(self):
        if self.date in range(1, 28):
            self.date += 1
        else:
            if self.season == Season.SPRING:
                self.season = Season.SUMMER
            elif self.season == Season.SUMMER:
                self.season = Season.FALL
            elif self.season == Season.FALL:
                self.season = Season.WINTER
            else:
                self.season = Season.SPRING
            self.date = 1
        self.get_birthday_people()

    def get_location_of_villager(self, villager_name):
        print(f"Where is {villager_name}")

    def get_location_of_everyone(self):
        print(f"Where is everyone?")


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

    stardew = Stardew(season, date)
    stardew.get_birthday_people()
    Command.describe()
    
    while True:
        command_input = input("What do you want to do next? (Press 9 for help menu) ")
        command = Validator.validate_command(command_input)
        if command:
            command.execute(stardew)
        print("----------------------------")


