from enum import Enum


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
            stardew.get_location_of_villager("test")
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
