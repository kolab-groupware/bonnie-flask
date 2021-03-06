# -*- coding: utf-8 -*-
#
# Copyright 2014 Kolab Systems AG (http://www.kolabsys.com)
#
# Thomas Bruederli <bruederli at kolabsys.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from event import Event
from task import Task
from note import Note
from system import System
from user import User, Permission, AnonymousUser

__all__ = [
    'System',
    'Event',
    'Task',
    'Note',
    'User',
    'Permission',
    'AnonymousUser',
]

__class_map__ = {
    'event': Event,
    'task': Task,
    'note': Note,
    'system': System,
}

def get_instance(classname, **kw):
    """
        Returns an instance of the given model class
    """
    if __class_map__.has_key(classname):
        return __class_map__[classname](**kw)

    return None