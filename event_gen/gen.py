import datetime
import random
from datetime import date, time
from zoneinfo import ZoneInfo

from mimesis import Generic
from mimesis.locales import Locale

from event_gen.event import Events


class Gen:
    def __init__(self, start_date: date, end_date: date,
                 tz: ZoneInfo = ZoneInfo("UTC"), locale: Locale = Locale.RU) -> None:
        self._start_date = start_date
        self._end_date = end_date
        self._tz = tz

        self._random_data = Generic(locale)

    def _date_gen(self) -> date:
        medium_date = self._end_date - self._start_date
        rand_day = random.randrange(medium_date.days)
        rand_date = self._start_date + datetime.timedelta(days=rand_day)

        return rand_date

    def _locate_gen(self) -> dict:
        match random.randint(1, 3):
            case 1:
                return {
                    'address':
                        self._random_data.address.city() +
                        ', ' +
                        self._random_data.address.address()}
            case 2:
                return {'telegram': self._random_data.internet.uri()}
            case 3:
                return {'zoom': self._random_data.internet.uri()}
            case _:
                # Хотя скорее забудем увеличить диапазон randomint
                assert True, 'Что то пошло не так'

    def _members_gen(self, max_person_quantity: int = 10) -> list:
        members = []
        while max_person_quantity > 0:
            members.append(self._random_data.person.full_name())
            max_person_quantity -= 1

        return members

    def _time_gen(self) -> datetime:
        return self._random_data.datetime \
            .time().replace(microsecond=0, tzinfo=self._tz)

    def _timezone_gen(self) -> datetime:
        return self._random_data.datetime

    def _title_gen(self) -> str:
        while True:
            title = self._random_data.text.title()
            if 20 <= len(title) <= 100:
                return title

    def gen_event(self, count: int = 10) -> dict[str:str]:
        while count > 0:
            count -= 1
            yield {
                'date': self._date_gen().isoformat(),
                'time': self._time_gen().isoformat()+"+"+self._tz.key,
                'timezone': self._timezone_gen().timezone(),
                'event': random.choice(list(Events)).value,
                'name': self._title_gen(),
                'members': self._members_gen(random.randint(2, 10)),
                'location': self._locate_gen(),
                # 'l': self._locate_gen(),
                # 1: self._locate_gen()
            }
