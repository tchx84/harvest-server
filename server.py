#!/usr/bin/env python

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

import os
from ConfigParser import ConfigParser

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.netutil import bind_sockets
from tornado.process import fork_processes

from harvest.handler import Handler
from harvest.data_store import DataStore


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, 'etc/harvest.cfg')

    config = ConfigParser()
    config.read(config_path)

    sockets = bind_sockets(config.get('server', 'port'))
    fork_processes(0)

    datastore = DataStore(config.get('datastore', 'host'),
                          config.getint('datastore', 'port'),
                          config.get('datastore', 'username'),
                          config.get('datastore', 'password'),
                          config.get('datastore', 'database'))

    app = Application([(r"/rpc/store", Handler,
                       {'datastore': datastore,
                        'api_key': config.get('server', 'api_key')})])

    server = HTTPServer(app,
                        ssl_options={
                        'certfile': config.get('server', 'certfile'),
                        'keyfile': config.get('server', 'keyfile')})

    server.add_sockets(sockets)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
