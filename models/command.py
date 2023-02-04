from enum import Enum
from models.validator import Validator
from models.constants import bcolors


class Command(Enum):
    NEXT_DAY = 1
    LOCATION_OF_SINGLE_VILLAGER = 2
    LOCATION_OF_ALL_VILLAGERS = 3
    COMMAND = 9
    EXIT = 0

    def execute(self, stardew):
        if self == self.NEXT_DAY:
            stardew.to_next_day()
        elif self == self.LOCATION_OF_SINGLE_VILLAGER:
            print("╔═════════════════✿═════════════════╗")
            print(f" On {stardew.season.name.capitalize()} {stardew.date}, "\
                  f"a {stardew.weather} {stardew.dow.name.capitalize()}...")
            print(" ----------------------------------")

            villager_name = None
            hour = None
            minute = None

            while True:
                if villager_name is None:
                    villager_input = input(f" {bcolors.BOLD}Name:{bcolors.ENDC} ")
                    villager_name = Validator.validate_villager(villager_input)
                else:
                    villager_input = input(f" {bcolors.BOLD}Name{bcolors.ENDC} (Press enter if it's {villager_name}): ")
                    if villager_input:
                        villager_name = Validator.validate_villager(villager_input)

                if hour is None:
                    time_input = input(f" {bcolors.BOLD}Time (HH:mm - 24 hr):{bcolors.ENDC} ")
                    hour, minute = Validator.validate_time(time_input)
                else:
                    time_input = input(f" {bcolors.BOLD}Time (HH:mm - 24 hr):{bcolors.ENDC} (Press enter if it's {hour}:{minute}): ")
                    if time_input:
                        hour, minute = Validator.validate_time(time_input)

                if villager_name and hour is not None and minute is not None:
                    stardew.get_location_of_villager(villager_name, hour, minute)

                next_command = input(" continue(c) ")
                if next_command != "c":
                    break
                print("--------------------------------------")

            print("╚═════════════════✿═════════════════╝")

        elif self == self.LOCATION_OF_ALL_VILLAGERS:
            stardew.get_location_of_everyone()
        elif self == self.COMMAND:
            self.describe()
        elif self == self.EXIT:
            print("Terminating program... Bye byeeeee!")
            quit()

    @classmethod
    def describe(cls):
        description = \
            "******************************************\n" \
            "* Available commands:                    *\n" \
            "* 1 - To go to the next day              *\n" \
            "* 2 - Get location of a villager         *\n" \
            "* 3 - Get location of all the villagers  *\n" \
            "* 9 - Help menu                          *\n" \
            "* 0 - Exit program                       *\n" \
            "******************************************"
        print(description)
