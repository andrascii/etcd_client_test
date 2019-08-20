import etcd3
import threading
from data import KVEvent
from six.moves import queue
from common import message, critical_message


class Watcher:
    def __init__(self, etcd_client, test):
        self.__etcd_client = etcd_client
        self.__watcher_iter = None
        self.__prefix = '/'
        self.__test = test

    def start_watcher(self):
        event_queue = queue.Queue()

        def callback(event):
            event_queue.put(event)

        range_end = etcd3.utils.increment_last_byte(etcd3.utils.to_bytes(self.__prefix))
        watch_id = self.__etcd_client.add_watch_callback(self.__prefix, callback, range_end=range_end)
        canceled = threading.Event()

        def cancel():
            try:
                canceled.set()
                event_queue.put(None)
                self.__etcd_client.cancel_watch(watch_id)

            except Exception as error:
                critical_message('some error:' + error)

        def iterator():
            while not canceled.is_set():
                try:
                    event = event_queue.get()

                    if event is None:
                        canceled.set()

                    if isinstance(event, Exception):
                        canceled.set()
                        raise event

                    if not canceled.is_set():
                        yield event

                except queue.Empty:
                    critical_message('queue.Empty error')

        self.__watcher_iter = iterator()
        return cancel

    def run(self):
        for response in self.__watcher_iter:
            self.__on_events([
                KVEvent(evt.key, KVEvent.ACTION_DELETE
                if isinstance(evt, etcd3.events.DeleteEvent)
                else KVEvent.ACTION_UPDATE, evt.value) for evt in response.events], response.header.revision)

    def __on_events(self, events, revision):
        def action_string(action):
            if action == KVEvent.ACTION_DELETE:
                return "ACTION_DELETE"
            if action == KVEvent.ACTION_UPDATE:
                return "ACTION_UPDATE"

        self.__perform_test(events)

        for event in events:
            message(action_string(event.action))

            if event.action == KVEvent.ACTION_UPDATE:
                message('key: ' + event.key.decode('ascii') + ' value: ' + event.value.decode('ascii'))

            else:
                message('key: ' + event.key.decode('ascii'))

    def __perform_test(self, *args):
        if self.__test is not None:
            self.__test(*args)
