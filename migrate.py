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

from harvest.migrator import Migrator
from harvest.error import MigrationError


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, 'etc/harvest.cfg')
    migrations_path = os.path.join(script_path, 'sql/')

    config = ConfigParser()
    config.read(config_path)
    migrator = Migrator(migrations_path,
                        config.get('datastore', 'host'),
                        config.getint('datastore', 'port'),
                        config.get('datastore', 'username'),
                        config.get('datastore', 'password'),
                        config.get('datastore', 'database'),
                        ['001-harvest.sql'])
    try:
        migrator.migrate()
    except MigrationError as err:
        print 'Migration failed, please restore and try manually: %s' % err

if __name__ == '__main__':
    main()
