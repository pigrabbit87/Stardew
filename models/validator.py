from models.command import Command
from models.constants import Season


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
