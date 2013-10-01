## Harvest project
Harvest project aims to make learning visible to educators and decision makers.
Within the context of the Sugar Learning Platform, this can be achieved by
collecting reliable metadata from the Journal.

## Harvest server setup
These instructions were prepared for Fedora 19.

0. Install harvest-server dependencies:

        $yum install git mysql-server python MySQL-python python-pip
        $pip install tornado==3.1.1

1. Get the harvest-server package:

        $cd /path/to/deployments/
        $git clone git@github.com:tchx84/harvest-server.git
        $cd harvest-server

2. Create the database:

        $service mysqld start
        $mysql -u root -p < sql/001-harvest.sql

3. Create the SSL certificates:

        $./misc/generate.sh
        $mv localhost.* etc/

4. Create config file:

        $cp etc/harvest.cfg.example etc/harvest.cfg
        $vim etc/harvest.cfg

6. Run the server:

        $./server.py
