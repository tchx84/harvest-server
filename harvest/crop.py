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


class Crop(object):

    @staticmethod
    def querify(data):
        """ split data for queries format """

        learners = None
        activities = None
        instances = None
        launches = None

        #  dijkstra... forgive me!
        if data[0] and data[0][0]:
            learners = [data[0]]

        for activity in data[1].keys():
            if activities is None:
                activities = []
            activities.append([activity])

            for instance in data[1][activity]:
                if instances is None:
                    instances = []
                instances.append(instance[:-1] + [data[0][0]] + [activity])

                for launch in instance[-1]:
                    if launches is None:
                        launches = []
                    launches.append([launch] + [instance[0]] + [data[0][0]])

        return learners, activities, instances, launches
