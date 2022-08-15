from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.hasmethod import hasmethod

class IsGivenDayOfWeek(BaseMatcher):

    def __init__(self, day):
        self.day = day  # Monday is 0, Sunday is 6

    def _matches(self, item):
        if not hasmethod(item, 'weekday'):
            return False
        return item.weekday() == self.day

    def describe_to(self, description):
        day_as_string = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                         'Friday', 'Saturday', 'Sunday']
        description.append_text('calendar date falling on ')    \
                   .append_text(day_as_string[self.day])

    def describe_mismatch(self, item, mismatch_description):
        day_as_string = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                         'Friday', 'Saturday', 'Sunday']
        mismatch_description.append_text('got ') \
                            .append_description_of(item) \
                            .append_text(' which is a ') \
                            .append_text(day_as_string[item.weekday()])


def on_a_saturday():
    return IsGivenDayOfWeek(5)
