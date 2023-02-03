from models.constants import Season


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

