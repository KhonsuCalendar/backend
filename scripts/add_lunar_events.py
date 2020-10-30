import pprint
from datetime import datetime
from dataclasses import dataclass
from typing import List

import requests

pp = pprint.PrettyPrinter(indent=4)


@dataclass
class LunarPhase:
    phase: str
    datetime: datetime

def parse_api_response(year: int, month: int, phase_data: dict) -> List[LunarPhase]:
    accepted_events = ["Full moon", "New Moon", "First quarter", "Last quarter"]
    recorded_events = []
    for day, phase in phase_data.items():
        if phase["phaseName"] in accepted_events:
            event = LunarPhase(
                phase=phase["phaseName"],
                datetime=datetime(year=year, month=month, day=int(day))
            )
            recorded_events.append(event)
    return recorded_events


def get_data_for_month(year: int, month: int) -> List[LunarPhase]:
    given_date = datetime(year=year, month=month, day=1)
    epoch = datetime.utcfromtimestamp(0)
    seconds_from_epoch = (given_date - epoch).total_seconds()

    url = "https://www.icalendar37.net/lunar/api/"
    params = {"month": month, "year": year, "LDZ": seconds_from_epoch}
    response = requests.get(url, params=params)
    if not response.ok:
        raise Exception(f"Something went wrong when retrieving data: {str(e)}")
    lunar_events = parse_api_response(year, month, response.json()["phase"])
    # pp.pprint(lunar_events)
    return lunar_events


def get_data_for_year(year: int) -> List[LunarPhase]:
    recorded_events = []
    for month in range(1, 13):
        recorded_events.extend(get_data_for_month(year, month))
    return recorded_events


def submit_events(phase_events: List[LunarPhase]) -> None:
    phase_events = sorted(phase_events, key=lambda x: x.datetime)
    cur_cycle = 0
    for event in phase_events:
        if event.phase == 'New Moon':
            cur_cycle = int(event.datetime.strftime('%Y%m%d'))
        cleaned_event = {
            "cycle": cur_cycle,
            "datetime": event.datetime.isoformat(),
            "phase": event.phase
        }
        response = requests.post('http://localhost:8000/event', json=cleaned_event)
        if not response.status_code == 200:
            raise Exception("something went wrong")


if __name__ == "__main__":
    phases = get_data_for_year(2020)
    phases.extend(get_data_for_year(2021))
    submit_events(phases)
