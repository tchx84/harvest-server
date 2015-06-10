## Harvest project
Harvest project aims to make learning visible to educators and decision makers.
Within the context of the Sugar Learning Platform, this can be achieved by
collecting reliable metadata from the Journal.

## Harvest server setup

0. Install harvest-server dependencies:

On Fedora 18/19.

        $yum install git openssl httpd-tools mysql-server python MySQL-python tornado

On Debian 6.0

        $apt-get install git openssl mysql python python-mysqldb python-tornado python-pip build-essential python-dev
        $pip install tornado

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

On Fedora 18/19.

        $service mysqld start

On Debian mysql package already start the service.

        $mysql -u root -p < sql/001-harvest.sql
        $./migrate.py

5. Run the server:

        $./server.py

On Debian or distributions without systemd, you can use the file etc/harvest.init to
start/stop the deamon. Copy the file in as /etc/init.d/harvest and create a
symlink in the directory /etc/rc3.d

## More Information

If you just want to use this, I recommend you to read the
wiki documentation at http://wiki.sugarlabs.org/go/Harvest
