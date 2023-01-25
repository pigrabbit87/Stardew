import requests, bs4, json, time

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

DATES = ['1st', '2nd', '3rd', *[f'{num}th' for num in range(4, 29)]]

# Process from raw html data
def process_person(name):
    # Scrape or load
    raw_data = load_raw_villager_data(name)

    soup = bs4.BeautifulSoup(raw_data, 'html.parser')

    person_data = {}

    # Parse info
    person_data['basic'] = parse_info(soup)

    # Parse schedule
    if name not in {"Wizard", "Sandy", "Dwarf"}:
        person_data['schedule'] = process_schedules(soup)

    with open(f'villagers/parsed/{name}.json', 'w') as f:
            json.dump(person_data, f, indent=2)


# Improve from parsed json
def improve_person(name):
    with open(f'villagers/parsed/{name}.json', 'r') as f:
        person_data = json.load(f)

    person_data = improve_schedule(person_data)

    with open(f'villagers/parsed/{name}.json', 'w') as f:
        json.dump(person_data, f, indent=2)


def improve_schedule(person_data):
    # Raining
    schedules = person_data["schedule"]
    for idx, schedule in enumerate(schedules):
        if "raining" in schedule["name"].lower():
            person_data["schedule"][idx]["has_rain"] = True

    return person_data


def load_raw_villager_data(name):
    with open(f'villagers/raw/{name}.html', 'r') as f:
        return f.read()


def scrape(name):
    url = f'https://stardewvalleywiki.com/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'villagers/raw/{person}.html', 'w') as f:
            f.write(response.text)
        return bs4.BeautifulSoup(response.text, 'html.parser')
    else:
        raise UrlNotFound


def parse_info(soup):
    info_data = {}
    # Info table
    info_table = soup.find("table", {"id": "infoboxtable"})
    info_attributes = info_table.find_all("tr")

    for attribute in info_attributes:
        header = attribute.find('td', {"id": "infoboxsection"})
        detail = attribute.find('td', {"id": "infoboxdetail"})
        if header and detail:
            header_text = header.text.strip()
            if header_text == "Best Gifts":
                info_data[header_text] = process_gifts(detail)
            else:
                info_data[header_text] = detail.text.strip()

    return info_data


def process_gifts(element):
    gifts_span = element.find_all('span', {"class": "nametemplate"})
    return [gift.text.strip() for gift in gifts_span]


def process_schedules(soup):
    schedule = soup.find("span", {"id": "Schedule"})
    schedule_tables = []
    for element in schedule.parent.next_siblings:
        if type(element) == bs4.element.NavigableString:
            continue
        if element.name == "table":
            # Some person has nested table
            if "wikitable" in element["class"]:
                table = element.find('tbody')
                if table:
                    schedule_tables.append(process_schedule_table(table))
            else:
                table = element.find('tbody')
                if table:
                    schedule_tables.extend(process_nested_schedule_table(table))
        elif schedule_tables:
            break
    return schedule_tables


def process_nested_schedule_table(element):
    section_header = element.find('th').text.strip()
    schedules = []

    details = element.find('td').children
    schedule_name = None

    for detail in details:
        if detail.name == 'p':
            schedule_name = f"{section_header} {detail.text.strip()}"
        if detail.name == 'table':
            rows = detail.find_all('tr')
            time_and_locations = []
            for row in rows[1:]:
                details = row.find_all('td')
                if details:
                    time = details[0].text.strip()
                    description = details[1].text.strip()
                    time_and_locations.append({
                        "time": time,
                        "description": description
                    })
            schedules.append({"name": schedule_name, **parse_schedule_name(schedule_name), "schedules": time_and_locations})

    return schedules

def process_schedule_table(element):
    time_and_locations = []

    rows = element.find_all('tr')
    schedule_name = rows[0].text.strip()
    for row in rows[1:]:
        details = row.find_all('td')
        if details:
            time = details[0].text.strip()
            description = details[1].text.strip()
            time_and_locations.append({
                "time": time,
                "description": description
            })

    return {"name": schedule_name, **parse_schedule_name(schedule_name), "schedules": time_and_locations}


def parse_schedule_name(schedule_name):
    """
    {
        "season": "",
        "DOW": [],
        "has_rain":,
        "date": []
    }
    """

    schedule_name = schedule_name.lower().replace(',', '')
    default = "regular schedule" in schedule_name

    schedule_tokens = schedule_name.split(' ')
    uncertain = "deviations" in schedule_tokens

    heart_dependent = "heart" in schedule_tokens or "hearts" in schedule_tokens

    heart_condition = {}
    if "less than 6 hearts" in schedule_name or "not at 6 hearts" in schedule_name:
        with_index = schedule_tokens.index('with')
        heart_condition['less_than_six'] = " ".join(schedule_tokens[with_index+1:])
    elif "6+ hearts" in schedule_name:
        with_index = schedule_tokens.index('with')
        heart_condition['more_than_six'] = " ".join(schedule_tokens[with_index+1:])

    community_center_repaired_dependent = "community center repaired" in schedule_name

    # Not doing marriage for now
    if "marriage" in schedule_tokens:
        return {}

    try:
        season = next(s for s in ['spring', 'summer', 'fall', 'winter'] if s in schedule_tokens)
    except StopIteration:
        season = None

    dow = [d for d in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] if d in schedule_tokens]

    has_rain = "rain" in schedule_tokens or "rainy" in schedule_tokens or "raining" in schedule_tokens

    date = [idx+1 for idx, date in enumerate(DATES) if date in schedule_tokens]

    return {
        "season": season,
        "default": default,
        "uncertain": uncertain,
        "heart_dependent": heart_dependent,
        "heart_condition": heart_condition,
        "community_center_repaired_dependent": community_center_repaired_dependent,
        "DOW": dow,
        "has_rain": has_rain,
        "date": date
    }

class UrlNotFound(Exception):
    pass


if __name__ == "__main__":
    for person in VILLAGERS:
        print(f"Processing {person}.")
        improve_person(person)

        