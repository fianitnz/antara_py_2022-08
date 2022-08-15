import datetime
import zoneinfo
from datetime import date, time

# import hamcrest
import mimesis
import pytest
from hamcrest import *

from event_gen.gen import Gen
from custom_matcher import on_a_saturday


class TestEventGen:
    @pytest.fixture
    def method_before(self, start_date, end_date):
        self.gen = Gen(start_date, end_date)
        yield
        del self.gen

    @pytest.mark.parametrize(
        "start_date, end_date",
        # Добавить генератор случайных цифровых дат
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_date_gen(self, method_before):
        date_result = self.gen._date_gen()
        print(type(date_result))

        assert isinstance(date_result, date), \
            "Возвращаемый тип не: '" + date.__name__ + "'"
        assert date_result >= self.gen._start_date, \
            "Дата меньше указанного диапазона: '" + \
            self.gen._start_date.isoformat() + "'"
        assert date_result <= self.gen._end_date, \
            "Дата больше указанного диапазона: '" + \
            self.gen._end_date.isoformat() + "'"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_locate_gen(self, method_before):
        locate_result: dict = self.gen._locate_gen()

        assert isinstance(locate_result, dict), \
            "Возвращаемый тип не: '" + dict.__name__ + "'"
        assert len(locate_result.keys()) == 1, \
            "Не одной локации или больше одной"
        key = [i for i in locate_result.keys()][0]
        assert key in ("address", "telegram", "zoom"), \
            "Не установленный тип локации: '" + key + "'"
        assert locate_result.get(key), \
            "Не заполненное значение тип локации"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_members_gen(self, method_before):
        members_result = self.gen._members_gen()

        assert isinstance(members_result, list), \
            "Возвращаемый тип не: '" + list.__name__ + "'"
        assert len(members_result) == 10, \
            "Количество участников не равно 10"
        assert "" not in members_result, \
            "Участник не может быть пустой строкой"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_time_gen(self, method_before):
        time_result = self.gen._time_gen()

        assert isinstance(time_result, time), \
            "Возвращаемый тип не: '" + time.__name__ + "'"
        assert time_result.tzinfo == self.gen._tz, \
            "Временная зона не совпадает с указанной: '" + \
            self.gen._tz.key + "'"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_timezone_gen(self, method_before):
        timezone_result = self.gen._timezone_gen()

        assert isinstance(timezone_result, mimesis.Datetime), \
            "Возвращаемый тип не: '" + mimesis.Datetime.__name__ + "'"
        tz_name = timezone_result.timezone()
        assert tz_name in zoneinfo.available_timezones(), \
            "Не существующая тайм зона: '" + tz_name + "'"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_title_gen(self, method_before):
        title_gen_result = self.gen._title_gen()

        assert isinstance(title_gen_result, str), \
            "Возвращаемый тип не: '" + str.__name__ + "'"
        assert 20 <= len(title_gen_result), \
            "Длина возвращаемой строки меньше 20 символов: '" + \
            str(len(title_gen_result)) + "'"
        assert len(title_gen_result) <= 100, \
            "Длина возвращаемой строки больше 100 символов: '" + \
            str(len(title_gen_result)) + "'"

    @pytest.mark.parametrize(
        "start_date, end_date",
        [(date(year=2000, month=7, day=15),
          date(year=2000, month=8, day=20))])
    def test_gen_event(self, method_before):
        gen_event_result = self.gen.gen_event()

        assert_that(next(gen_event_result), instance_of(dict),
                    "Возвращаемый тип не: '" + str.__name__ + "'")
        # print(next(gen_event_result).keys())
        # assert_that(next(gen_event_result).keys(), all_of(instance_of(str)))
        # assert_that(['date', 'time', 'timezone', 'event', 'name', 'members', 'location', 'l'], all_of(only_contains(instance_of(str)))            )
        # assert_that(next(gen_event_result), only_contains(all_of(instance_of(str)))                     )
        # assert_that(next(gen_event_result), only_contains(instance_of(str))                     )
        # assert_that(next(gen_event_result).keys(), only_contains(instance_of(str)))
        # assert_that(next(gen_event_result), only_contains(instance_of(str)))
        assert_that(next(gen_event_result), only_contains(on_a_saturday()))




# json проверка

# за пределами логики и формирования итоговых данных
# files creation фала проверка
# cli командной строки проверка








































