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
import time
import MySQLdb

from .error import MigrationError


class Migrator:

    SQL_GET = 'SELECT * FROM migrations ORDER BY filename DESC LIMIT 1'
    SQL_SET = 'INSERT INTO migrations VALUES (%s, %s)'

    def __init__(self, path, host, port, user, passwd, db, banned):
        self._banned = banned
        self._path = path
        self._connection = MySQLdb.connect(host=host,
                                           port=port,
                                           user=user,
                                           passwd=passwd,
                                           db=db)

    def _execute(self, sql, values):
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, values)
            self._connection.commit()
            return cursor.fetchone()
        except Exception as err:
            self._connection.rollback()
            raise MigrationError(err)
        finally:
            cursor.close()

    def _get_last_migration(self):
        try:
            result = self._execute(self.SQL_GET, None)
            return result[0]
        except Exception:
            return None

    def _extract_sqls(self, raw_content):
        return [line
                for line in raw_content.replace('\n', '').split(';')
                if line]

    def _time_now(self):
        return int(time.mktime(time.gmtime()))

    def _apply(self, filename):
        with open(os.path.join(self._path, filename)) as file:
            for sql in self._extract_sqls(file.read()):
                self._execute(sql, None)
            self._execute(self.SQL_SET, [filename, self._time_now()])
            print 'Migrated to %s.' % filename

    def migrate(self):
        last_migration = self._get_last_migration()
        for filename in sorted(os.listdir(self._path)):
            if filename.endswith('.sql') and\
                filename not in self._banned and\
                    filename > last_migration:
                self._apply(filename)
        print 'All migrations done.'

    def __del__(self):
        if hasattr(self, '_connection'):
            self._connection.close()
