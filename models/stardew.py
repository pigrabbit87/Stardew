from models.constants import Season, bcolors


class Stardew:
    def __init__(self, season, date, data):
        self.season = season
        self.date = date
        self.data = data

    def get_birthday_people(self):
        birthday_people = []
        for villager_name, villager in self.data.items():
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

    def get_location_of_villager(self, villager_name, hour, minute):
        print(f"Where is {villager_name} at {hour}:{minute}")

    def get_location_of_everyone(self):
        print(f"Where is everyone?")
