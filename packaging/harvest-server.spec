Name:           harvest-server
Version:        0.2.0        
Release:        1
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

%post
if [ ! -f /opt/harvest/etc/harvest.cfg ]; then
    cp /opt/harvest/etc/harvest.cfg.example /opt/harvest/etc/harvest.cfg
    echo "created new configuration file"
else
    echo "using existing configuration file"
fi

if [ ! -f /opt/harvest/etc/harvest.crt ] || [ ! -f /opt/harvest/etc/harvest.key ]; then
    /opt/harvest/misc/generate.sh > /dev/null 2>&1
    mv localhost.crt.example /opt/harvest/etc/harvest.crt
    mv localhost.key.example /opt/harvest/etc/harvest.key
    echo "created new certificate and key files"
else
    echo "using existing certificate and key files"
fi

exists=$(mysql -u root -e "show databases like 'harvest'")
if [ $? = "0" -a -z "$exists" ]; then
    mysql -u root < /opt/harvest/sql/001-harvest.sql
    echo "created new harvest database"
else
    echo "using existing harvest database"
fi
/opt/harvest/migrate.py

%files
/opt/harvest/server.py
/opt/harvest/migrate.py
/opt/harvest/etc/harvest.cfg.example
/opt/harvest/misc/generate.sh
/opt/harvest/sql/001-harvest.sql
/opt/harvest/sql/002-create-migrations.sql
/opt/harvest/sql/003-rename-foreign-keys.sql
/opt/harvest/sql/004-add-age-and-gender-constraints.sql
/opt/harvest/sql/005-move-serial-position.sql
/opt/harvest/sql/006-hash-serial-number.sql
/opt/harvest/sql/007-add-mime-type-column.sql
/opt/harvest/harvest/__init__.py
/opt/harvest/harvest/data_store.py
/opt/harvest/harvest/decorators.py
/opt/harvest/harvest/crop.py
/opt/harvest/harvest/migrator.py
/opt/harvest/harvest/error.py
/opt/harvest/harvest/handler.py
%{_sysconfdir}/systemd/system/harvest.service

%changelog
* Sat Nov 9 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- SQL migrations support
- Include mime_type metadata
- Learners uniquely identified by SN, age and birthdate

* Wed Oct 30 2013 Martin Abente Lahaye <tch@sugarlabs.org>
- Initial RPM release
