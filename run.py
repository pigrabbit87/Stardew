import json
import sys

from enum import Enum

from models.constants import VILLAGERS, Season, bcolors
from models.validator import Validator
from models.command import Command
from models.villager import Villager
from models.stardew import Stardew


def load_data():
    data = {}
    folder_path = 'villagers/parsed'
    for villager in VILLAGERS:
        with open(f'{folder_path}/{villager}.json', 'r') as f:
            data[villager] = Villager(villager, json.load(f))
    return data


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

    raining_input = input("Is it raining (T/F)? ")

    stardew = Stardew(season, date, raining_input == "T", data)
    stardew.get_birthday_people()
    Command.describe()
    
    while True:
        command_input = input("What do you want to do next? (Press 9 for help menu) ")
        command = Validator.validate_command(command_input)
        if command is not None:
             Command(command).execute(stardew)
        print("----------------------------")


