from itest import ITest
from data import KVEvent
from common import critical_message


class ABIncrementorTest(ITest):
    def __init__(self):
        self.__reset_state()

    def _perform_test(self, event: KVEvent):
        self.__prev_event_action = self.__current_event_action
        self.__current_event_action = event.action

        if event.action != KVEvent.ACTION_DELETE:
            self.__prev_event_value = self.__current_event_value
            self.__current_event_value = int(event.value)

        self.__write_critical_log_if_needed()

    def _transaction_event_count(self, event_count):
        if event_count > 2:
            critical_message('events length grater than one and equal to: {0}'.format(event_count))

    def __write_critical_log_if_needed(self):
        if self.__current_event_action == self.__prev_event_action:
            critical_message('invalid sequence of put/delete events')
            self.__reset_state()

        if (self.__current_event_value - self.__prev_event_value) != 1:
            critical_message('skipped some events!!!')

    def __reset_state(self):
        self.__current_event_action = object
        self.__prev_event_action = object
        self.__current_event_value = -1
        self.__prev_event_value = -2
