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

from kolabobject import KolabObject
from pykolab.xml import todo_from_message

class Task(KolabObject):
    """
        Model class for accessing Kolab Groupware Task data
    """

    def __init__(self, *args, **kw):
        KolabObject.__init__(self, *args, **kw)
        self.folder_type = 'task'
        self.x_kolab_type = 'application/x-vnd.kolab.task'

    def _object_from_message(self, message):
        return todo_from_message(message)
