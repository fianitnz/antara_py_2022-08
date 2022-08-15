import argparse
import json
import random
from datetime import datetime

from event_gen.event import Events
from event_gen.gen import Gen

if __name__ == "__main__":

    pars = argparse.ArgumentParser()

    pars.add_argument('start_date',
                      help='Начало диапазона дат в формате YYYY-mm-dd')
    pars.add_argument('end_date',
                      help='Конец диапазона дат в формате YYYY-mm-dd')
    pars.add_argument('-max_events', type=int, default=10,
                      help='Максимальное количество событий, но не больше 100')
    pars.add_argument('-dateformat', type=str, default='%Y-%m-%d',
                      help='Входной формат даты, по умолчанию %%Y-%%m-%%d')
    pars.add_argument('-f', type=str, default='json',
                      help='Имя выходного файла, по умолчанию json')

    args = pars.parse_args()

    start_date = datetime.strptime(args.start_date, args.dateformat).date()
    end_date = datetime.strptime(args.end_date, args.dateformat).date()

    assert args.max_events < 100, 'Многовато будет'
    assert start_date < end_date, 'Начальная дата не может быть больше конечной'

    gen = Gen(start_date, end_date)

    event_list = {}
    event_gen = gen.gen_event(random.randint(1, args.max_events))
    for name, content in event_gen:
        if event_list.get(name) is None:
            event_list[name] = []
            event_list[name].append(content)
        else:
            event_list[name].append(content)

    event_list_clear = {}
    for k in event_list.keys():
        if event_list_clear.get(k) is None:
            event_list_clear[k] = []
            event_list_clear[k].extend(
                list(filter(lambda d: d['event'] != Events.OTHER.value,
                            event_list[k])))
        else:
            event_list_clear[k].extend(
                list(filter(lambda d: d['event'] != Events.OTHER.value,
                            event_list[k])))

    with open(args.f + ".json", "w") as json_file:
        json.dump(event_list_clear, json_file,
                  ensure_ascii=False, indent=4, sort_keys=True)
