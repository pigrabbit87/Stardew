from models.constants import Season, bcolors, DateOfWeek


class Stardew:
    def __init__(self, season, date, is_raining, data):
        self.season = season
        self.date = date
        self.is_raining = is_raining
        self.data = data

    @property
    def dow(self):
        return self.get_dow(self.date)

    @property
    def weather(self):
        if self.is_raining:
            return "rainy"
        else:
            return "sunny"

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
        # TODO: Is it raining?
        self.get_birthday_people()

    def get_location_of_villager(self, villager_name, hour, minute):
        valid_schedule = self.get_valid_schedule(self.data[villager_name].schedules)

        # The starting schedule is everyone at their home location
        current_location = f"at their home in {self.data[villager_name].home_location}"
        current_time = self.convert_hour_and_minute_to_number(hour, minute)
        next_time = self.convert_standard_time_to_number(valid_schedule["schedules"][0]["time"])

        for schedule in valid_schedule["schedules"]:
            schedule_time = self.convert_standard_time_to_number(schedule["time"])
            if schedule_time > current_time:
                next_time = schedule_time
                break

            current_location = schedule['description']

        print(f" > [{valid_schedule['name']}]")
        print(f" > Between {bcolors.OKBLUE}{self.convert_to_readable_time(current_time)} and " \
              f"{self.convert_to_readable_time(next_time)}{bcolors.ENDC}, {bcolors.OKGREEN}{villager_name}{bcolors.ENDC}" \
              f" {self.beautify_location_string(current_location)}")

    def beautify_location_string(self, location_string):
        first_word, rest_words = location_string.split(' ', 1)
        if first_word.lower() in {'in', 'at'}:
            return f"is {first_word.lower()} {rest_words}"
        else:
            return f"{first_word.lower()} {rest_words}"

    def get_location_of_everyone(self):
        print(f"Where is everyone?")

    def get_valid_schedule(self, schedules):
        for schedule in schedules:
            if schedule["season"] and schedule["season"] != self.season.name.lower():
                continue

            if schedule["has_rain"] != self.is_raining:
                continue

            if schedule["DOW"] and self.dow.name not in schedule["DOW"]:
                continue

            if schedule["date"] and self.date not in schedule["date"]:
                continue

            return schedule

    """
    Return the day of the week from the date
    """
    def get_dow(self, date):
        return DateOfWeek(date % 7)

    def convert_standard_time_to_number(self, time):
        """
        time in the format of 08:00 AM
        """
        time, morning_or_night = time.split(' ')
        hour, minute = map(int, time.split(":"))
        if morning_or_night.lower() == "pm" and hour != 12:
            hour += 12
        return self.convert_hour_and_minute_to_number(hour, minute)

    def convert_hour_and_minute_to_number(self, hour, minute):
        return hour * 100 + minute

    def convert_to_readable_time(self, time_number, standard=True):
        hour = time_number // 100
        minute = time_number % 100
        if minute < 10:
            minute = f"0{minute}"

        if standard:
            if hour > 12:
                hour -= 12
                return f"{hour}:{minute} PM"
            elif hour == 12:
                return f"{hour}:{minute} PM"
            else:
                return f"{hour}:{minute} AM"

        else:
            # TODO implement non standard
            return ""


