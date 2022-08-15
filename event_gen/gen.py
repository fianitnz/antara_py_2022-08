import random
import datetime
from datetime import date

from mimesis import Generic
from mimesis.locales import Locale

from event_gen.event import Events


class Gen:
    def __init__(self,
                 start_date: date,
                 end_date: date,

                 locale: Locale = Locale.RU,
                 ) -> None:
        self.start_date = start_date
        self.end_date = end_date

        self.random_data = Generic(locale)

    def gen_event(self, count: int = 10):
        while count > 0:
            count -= 1
            yield [self.date_gen(),
                   {
                       'time': self.time_gen(),
                       'timezone': self.timezone_gen(),
                       'event': random.choice(list(Events)).value,
                       'name': self.title_gen(),
                       'members': self.members_gen(random.randint(2, 10)),
                       'location': self.locate_gen()
                   }
                   ]

    def date_gen(self):
        medium_date = self.end_date - self.start_date
        rand_day = random.randrange(medium_date.days)
        rand_date = self.start_date + datetime.timedelta(days=rand_day)

        return rand_date.isoformat()

    def time_gen(self):
        return self.random_data.datetime\
            .time().replace(microsecond=0).isoformat()

    def timezone_gen(self):
        return self.random_data.datetime.gmt_offset()

    def title_gen(self) -> str:
        while True:
            title = self.random_data.text.title()
            if 20 <= len(title) <= 100:
                return title

    def members_gen(self, max_person_quantity=10) -> list:
        members = []
        while max_person_quantity > 0:
            members.append(self.random_data.person.full_name())
            max_person_quantity -= 1

        return members

    def locate_gen(self) -> dict:
        match random.randint(1, 3):
            case 1:
                return {
                    'address':
                        self.random_data.address.city() +
                        ', ' +
                        self.random_data.address.address()}
            case 2:
                return {'telegram': self.random_data.internet.uri()}
            case 3:
                return {'zoom': self.random_data.internet.uri()}
            case _:
                # Хотя скорее забудем увеличить диапазон randomint
                assert True, 'Что то пошло не так'
