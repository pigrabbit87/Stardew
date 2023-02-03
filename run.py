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


def get_birthday_people(season, date):
    results = []
    for villager_name, villager in DATA.items():
        if villager.birthday_season == season and villager.birthday_date == date:
            results.append(villager_name)
    return results


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
    print("Data loaded successfully.")

    season_input = input("Please enter the current season (1-Spring, 2-Summer, 3-Fall, 4-Winter): ")
    season = Validator.validate_season_input(season_input)

    date_input = input("Please enter the date (1-28): ")
    date = Validator.validate_date_input(date_input)

    birthday_people = get_birthday_people(season, date)
    if birthday_people:
        print(f"It is {'and'.join(birthday_people)}'s birthday.")
    else:
        print("There is no birthday today.")

