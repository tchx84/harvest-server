## Harvest project
Harvest project aims to make learning visible to educators and decision makers.
Within the context of the Sugar Learning Platform, this can be achieved by
collecting reliable metadata from the Journal.

## Harvest server setup
These instructions were prepared for Fedora 18/19.

0. Install harvest-server dependencies:

        $yum install git openssl httpd-tools mysql-server python MySQL-python tornado

1. Get the harvest-server package:

        $cd /path/to/deployments/
        $git clone https://github.com/tchx84/harvest-server.git
        $cd harvest-server

2. Create the SSL certificates:

        $./misc/generate.sh
        $mv localhost.* etc/

3. Create config file:

        $cp etc/harvest.cfg.example etc/harvest.cfg
        $vim etc/harvest.cfg

4. Create the database:

        $service mysqld start
        $mysql -u root -p < sql/001-harvest.sql
        $./migrate.py


5. Run the server:

        $./server.py

## More Information

If you just want to use this, I recommend you to read the
wiki documentation at http://wiki.sugarlabs.org/go/Harvest
