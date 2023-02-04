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


class Season(Enum):
    SPRING = 1
    SUMMER = 2
    FALL = 3
    WINTER = 4


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
