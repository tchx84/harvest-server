Name:           harvest-server
Version:        0.5.1
Release:        0
Summary:        Server for the Harvest Project

License:        GPLv2+
URL:            https://github.com/tchx84/harvest-server
Source0:        %{name}-%{version}.tar.gz

Requires:       python >= 2.7, python-tornado >= 2.2.1, openssl >= 1.0.1, mysql-server >= 5.5, MySQL-python >= 1.2.3 

BuildArch:      noarch

%description
Server for the Harvest Project that aims to make learning visible to educators and decision makers

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/harvest/
cp -r harvest sql server.py migrate.py $RPM_BUILD_ROOT/opt/harvest/

mkdir $RPM_BUILD_ROOT/opt/harvest/misc
cp misc/generate.sh $RPM_BUILD_ROOT/opt/harvest/misc/

mkdir $RPM_BUILD_ROOT/opt/harvest/etc
cp etc/harvest.cfg.example $RPM_BUILD_ROOT/opt/harvest/etc/harvest.cfg.example

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
cp etc/harvest.service $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
exists=$(getent passwd harvest > /dev/null)
if [ $? = "0" -a -z "$exists" ]; then
    echo "Using existing user"
else
    useradd --no-create-home \
            --user-group \
            --shell /sbin/nologin \
            --comment "harvest server" \
            harvest
    echo "Created new harvest user"
fi

%post
if [ ! -f /opt/harvest/etc/harvest.cfg ]; then
    cp /opt/harvest/etc/harvest.cfg.example /opt/harvest/etc/harvest.cfg
    echo "Created new configuration file"
else
    echo "Using existing configuration file"
fi

if [ ! -f /opt/harvest/etc/harvest.crt ] || [ ! -f /opt/harvest/etc/harvest.key ]; then
    /opt/harvest/misc/generate.sh > /dev/null 2>&1
    mv localhost.crt.example /opt/harvest/etc/harvest.crt
    mv localhost.key.example /opt/harvest/etc/harvest.key
    echo "Created new certificate and key files"
else
    echo "Using existing certificate and key files"
fi

exists=$(mysql -u root -e "show databases like 'harvest'")
if [ $? = "0" -a -z "$exists" ]; then
    mysql -u root < /opt/harvest/sql/001-harvest.sql
    echo "Created new harvest database"
else
    echo "Using existing harvest database"
fi
/opt/harvest/migrate.py

%files
%defattr(-,root,root)
%attr(0754, harvest, harvest) /opt/harvest/server.py
%attr(0754, root, root) /opt/harvest/migrate.py
%attr(0754, root, root) /opt/harvest/misc/generate.sh
/opt/harvest/etc/harvest.cfg.example
/opt/harvest/sql/001-harvest.sql
/opt/harvest/sql/002-create-migrations.sql
/opt/harvest/sql/003-rename-foreign-keys.sql
/opt/harvest/sql/004-add-age-and-gender-constraints.sql
/opt/harvest/sql/005-move-serial-position.sql
/opt/harvest/sql/006-hash-serial-number.sql
/opt/harvest/sql/007-add-mime-type-column.sql
/opt/harvest/sql/008-create-laptops-table.sql
/opt/harvest/sql/009-move-spents.sql
/opt/harvest/sql/010-add-grouping-column.sql
/opt/harvest/sql/011-create-counters-table.sql
/opt/harvest/sql/012-add-snapshot-column.sql
/opt/harvest/sql/013-add-extras-table.sql
/opt/harvest/harvest/__init__.py
/opt/harvest/harvest/data_store.py
/opt/harvest/harvest/decorators.py
/opt/harvest/harvest/crop.py
/opt/harvest/harvest/migrator.py
/opt/harvest/harvest/error.py
/opt/harvest/harvest/handler.py
%{_sysconfdir}/systemd/system/harvest.service

%changelog
* Wed Jun 25 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Support snapshots metadata

* Tue Jun 17 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- land grades, time and traffic changes.

* Wed Feb 12 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Remove authbind
- Specify listen address

* Mon Jan 06 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Set instances number in config
- Run as unpriviledge user
- Fix messages style
- Set no_keep_alive in config

* Tue Dec 03 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- Include laptops data
- Fix executable permissions

* Mon Nov 18 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- Fix typo in systemd control script

* Thu Nov 14 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- Start explicit multiple statements transaction

* Sat Nov 9 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- SQL migrations support
- Include mime_type metadata
- Learners uniquely identified by SN, age and birthdate

* Wed Oct 30 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- Initial RPM release
