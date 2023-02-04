from models.constants import Season, VILLAGERS


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
            return int(command_input)
        except ValueError:
            print(f"{command_input} is not a valid command.")

    @classmethod
    def validate_villager(cls, villager_input):
        villager_input = villager_input.lower().capitalize()
        if villager_input not in VILLAGERS:
            print(f"{villager_input} is not a villager.")
        else:
            return villager_input

    @classmethod
    def validate_time(cls, time_input):
        hour, minute = time_input.split(':')
        if int(hour) not in range(0, 24):
            print(f"Hour should be between 0 and 23")
            return

        if int(minute) not in range(0, 60):
            print(f"Minute should be between 0 and 59")
            return

        return int(hour), int(minute)
