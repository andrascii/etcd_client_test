import logging

log = logging.getLogger('etcd_client_logger')


class KVEvent(object):
    ACTION_NONE = 0
    ACTION_UPDATE = 1
    ACTION_DELETE = 2

    @staticmethod
    def split_value(v):
        idx = v.find(",")
        if idx == -1:
            return "", ""
        return v[0 : idx], v[idx + 1 :]

    def __init__(self, key, action, mod_revision, value = None):
        self.key = key
        self.action = action
        self.modified_revision = mod_revision
        self.value = value

    def __repr__(self):
        return "(%s, %s, %s)" % (self.key, self.action, self.value)

    @property
    def mod_revision(self):
        return self.modified_revision

    @property
    def value_src(self):
        src, v = KVEvent.split_value(self.value)
        return src

    @property
    def value_data(self):
        src, v = KVEvent.split_value(self.value)
        return v
