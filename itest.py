from data import KVEvent
from abc import ABCMeta, abstractmethod


class ITest:
    __metaclass__ = ABCMeta

    def __call__(self, event_list: list):
        self._transaction_event_count(len(event_list))

        for event in event_list:
            self._perform_test(event)

    @abstractmethod
    def _perform_test(self, event: KVEvent):
        raise NotImplementedError

    @abstractmethod
    def _transaction_event_count(self, event_count):
        raise NotImplementedError
