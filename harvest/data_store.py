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

import MySQLdb

from .error import StoreError
from .crop import Crop


class DataStore(object):

    QUERY_LAPTOP = 'INSERT INTO laptops '\
                   '(serial_number, build, snapshot, '\
                   'updated, collected, stored) '\
                   'values (%s, %s, %s, %s, %s, UNIX_TIMESTAMP(now())) '\
                   'ON DUPLICATE KEY UPDATE '\
                   'build = VALUES(build), '\
                   'snapshot = VALUES(snapshot), '\
                   'updated = VALUES(updated), '\
                   'collected = VALUES(collected), '\
                   'stored = values(stored)'

    QUERY_LEARNER = 'INSERT INTO learners '\
                    '(serial_number, birthdate, gender, grouping) '\
                    'values (%s, %s, %s, %s) '\
                    'ON DUPLICATE KEY UPDATE '\
                    'grouping = VALUES(grouping)'

    QUERY_ACTIVITY = 'INSERT INTO activities '\
                     '(bundle_id) '\
                     'values (%s) '\
                     'ON DUPLICATE KEY UPDATE '\
                     'bundle_id = VALUES(bundle_id)'

    QUERY_INSTANCE = 'INSERT INTO instances '\
                     '(object_id, filesize, creation_time, timestamp, '\
                     'buddies, share_scope, title_set_by_user, '\
                     'keep, mime_type, bundle_id, serial_number, '\
                     'birthdate, gender, grouping) '\
                     'values (%s, %s, %s, %s, %s, %s, '\
                     '%s, %s, %s, %s, %s, %s, %s, %s) '\
                     'ON DUPLICATE KEY UPDATE ' \
                     'filesize = VALUES(filesize), '\
                     'timestamp = VALUES(timestamp), '\
                     'buddies = VALUES(buddies), '\
                     'share_scope = VALUES(share_scope), '\
                     'title_set_by_user = VALUES(title_set_by_user), '\
                     'keep = VALUES(keep), '\
                     'mime_type = VALUES(mime_type)'

    QUERY_LAUNCH = 'INSERT INTO launches '\
                   '(timestamp, spent_time, object_id, serial_number, '\
                   'birthdate, gender, grouping) '\
                   'values (%s, %s, %s, %s, %s, %s, %s) '\
                   'ON DUPLICATE KEY UPDATE '\
                   'spent_time = VALUES(spent_time)'

    QUERY_COUNTER = 'INSERT INTO counters '\
                    '(timestamp, download, upload, '\
                    'serial_number, birthdate, gender, grouping) '\
                    'values (%s, %s, %s, %s, %s, %s, %s) '\
                    'ON DUPLICATE KEY UPDATE '\
                    'download = VALUES(download), '\
                    'upload = VALUES(upload)'

    QUERY_EXTRAS = 'INSERT INTO extras '\
                   '(serial_number, object_id, metadata_key, metadata_value) '\
                   'values (%s, %s, %s, %s) '\
                   'ON DUPLICATE KEY UPDATE ' \
                   'metadata_value = VALUES(metadata_value)'

    def __init__(self, host, port, username, password, database):
        self._connection = MySQLdb.connect(host=host,
                                           port=port,
                                           user=username,
                                           passwd=password,
                                           db=database)

    def store(self, data):
        """ extracts metadata and inserts to the database """
        laptops, learners, activities, instances, launches, counters, \
            extras, = Crop.querify(data)

        self._connection.ping(True)
        try:
            self._connection.begin()
            cursor = self._connection.cursor()
            if laptops is not None:
                cursor.executemany(self.QUERY_LAPTOP, laptops)
            if learners is not None:
                cursor.executemany(self.QUERY_LEARNER, learners)
            if activities is not None:
                cursor.executemany(self.QUERY_ACTIVITY, activities)
            if instances is not None:
                cursor.executemany(self.QUERY_INSTANCE, instances)
            if launches is not None:
                cursor.executemany(self.QUERY_LAUNCH, launches)
            if counters is not None:
                cursor.executemany(self.QUERY_COUNTER, counters)
            if extras is not None:
                cursor.executemany(self.QUERY_EXTRAS, extras)
            self._connection.commit()
        except Exception as err:
            print err
            self._connection.rollback()
            raise StoreError
        finally:
            cursor.close()

    def __del__(self):
        if hasattr(self, '_connection') and self._connection is not None:
            self._connection.close()
