from kolabobject import KolabObject
from pykolab.xml import Event as XMLEvent

class Event(KolabObject):
    """
        Model class for accessing Kolab Groupware Event data
    """
    def _object_dict(self, raw):
        return XMLEvent(from_string=raw).to_dict()