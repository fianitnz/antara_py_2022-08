import argparse
import json
import random
import zoneinfo
from datetime import datetime
from itertools import groupby
from zoneinfo import ZoneInfo

from event_gen.event import Events
from event_gen.gen import Gen


def cli():
    pars = argparse.ArgumentParser()

    pars.add_argument('start_date',
                      help='Начало диапазона дат в формате YYYY-mm-dd')
    pars.add_argument('end_date',
                      help='Конец диапазона дат в формате YYYY-mm-dd')
    pars.add_argument('-time_zone', type=str, default="UTC",
                      help='Часовой пояс хранения сгенерированных событий, '
                           'например UTC, Europe/Moscow')
    pars.add_argument('-max_events', type=int, default=10,
                      help='Максимальное количество событий, но не больше 100')
    pars.add_argument('-dateformat', type=str, default='%Y-%m-%d',
                      help='Входной формат даты, по умолчанию:'
                           ' %%Y-%%m-%%d (1970-01-01)')
    pars.add_argument('-f', type=str, default='json',
                      help='Имя выходного файла, по умолчанию json')

    return pars.parse_args()


def cli_arg_check():
    assert arg.time_zone in zoneinfo.available_timezones(), \
        "Не найден часовой пояс: '" + arg.time_zone + "'"
    assert arg.max_events < 100, 'Многовато будет'
    assert start_date < end_date, 'Начальная дата не может быть ' \
                                  'больше конечной'


if __name__ == "__main__":
    arg = cli()

    start_date = datetime \
        .strptime(arg.start_date, arg.dateformat) \
        .replace(tzinfo=ZoneInfo(arg.time_zone)) \
        .date()
    end_date = datetime \
        .strptime(arg.end_date, arg.dateformat) \
        .replace(tzinfo=ZoneInfo(arg.time_zone)) \
        .date()

    cli_arg_check()

    gen = Gen(start_date, end_date)

    event_gen = gen.gen_event(random.randint(1, arg.max_events))

    event_list = [x for x in event_gen]

    # Фильтруем
    event_list = [i for i in event_list
                  if i.get('event') != Events.OTHER.value]

    # Сортируем
    # event_list = sorted(event_list, key=lambda x: x['date'])

    # Формируем группировку по дате:
    # event_list = {k: [x for x in v]                                                  for k, v in groupby(event_list, key=lambda x: x['date'])}
    # плюс Удаляем дату так как уже есть в ключе:
    event_list = {
        k: [{k3: v3 for k3, v3 in v2.items() if k3 != 'date'} for v2 in v] for k, v in groupby(event_list, key=lambda x: x['date'])}  # Да длинная строка страшная и в документации прямо пишут так делать не надо, но уж очень хотелось Х-D

    with open(arg.f + ".json", "w") as json_file:
        json.dump(event_list, json_file,
                  ensure_ascii=False, indent=4, sort_keys=True)
