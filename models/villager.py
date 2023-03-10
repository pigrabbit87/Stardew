from models.constants import Season


class Villager:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.parse_birthday()

    def parse_birthday(self):
        birthday = self.basic_info["Birthday"]
        self.birthday_season = Season[birthday.split(' ')[0].upper()]
        self.birthday_date = int(birthday.split(' ')[-1])

    @property
    def best_gifts(self):
        return self.basic_info["Best Gifts"]

    @property
    def schedules(self):
        return self.data["schedule"]

    @property
    def home_location(self):
        return f'{self.basic_info["Address"]}, {self.basic_info["Lives In"]}'

    @property
    def basic_info(self):
        return self.data["basic"]
