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

from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from app.auth import auth, permission_required
from ..model import Permission

root = Blueprint('root', __name__)

@root.route('/')
@login_required
@permission_required(Permission.WEB_ACCESS)
def index():
    nav = {}
    # add admin tasks
    if current_user.can(Permission.ADMINISTRATOR):
        nav['users'] = _("Users")

    return render_template('window.html', mainnav=nav.items())
