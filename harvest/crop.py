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

        laptops = None
        learners = None
        activities = None
        instances = None
        launches = None
        counters = None

        # dijkstra... forgive me!
        laptops = [data[0]]
        learners = [[data[0][0]] + data[1]]

        for activity in data[2].keys():
            if activities is None:
                activities = []
            activities.append([activity])

            for instance in data[2][activity]:
                if instances is None:
                    instances = []
                instances.append(instance[:-1] + [activity] + learners[0])

                for launch in instance[-1]:
                    if launches is None:
                        launches = []
                    launches.append(launch + [instance[0]] + learners[0])

        for counter in data[3]:
            if counters is None:
                counters = []
            counters.append(counter + learners[0])

        return laptops, learners, activities, instances, launches, counters
