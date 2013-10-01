# Copyright (c) 2013 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import json

from tornado.web import RequestHandler

from .error import StoreError
from .decorators import authenticate


class Handler(RequestHandler):

    MSG_OK = ''
    MSG_ENCODE_ERR = 'wrong encoding'
    MSG_STORE_ERR = 'failed to store'
    MSG_OPS_ERR = 'big ops!'

    def initialize(self, datastore, api_key):
        self._datastore = datastore
        self._api_key = api_key

    @authenticate
    def post(self):
        success = False
        message = None

        try:
            self._datastore.store(json.loads(self.request.body))
            self.set_status(200)
            success = True
            message = self.MSG_OK
        except ValueError:
            self.set_status(415)
            message = self.MSG_ENCODE_ERR
        except StoreError:
            self.set_status(400)
            message = self.MSG_STORE_ERR
        except Exception as err:
            print err
            self.set_status(500)
            message = self.MSG_OPS_ERR

        self.write(json.dumps({'success': success, 'message': message}))
        self.finish()
