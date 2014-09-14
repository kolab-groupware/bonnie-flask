from event import Event
from system import System

__class_map__ = { 'event': Event, 'system': System }

def get_instance(classname, **kw):
    """
        Returns an instance of the given model class
    """
    if __class_map__.has_key(classname):
        return __class_map__[classname](**kw)

    return None