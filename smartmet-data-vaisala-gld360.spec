%define smartmetroot /smartmet

Name:           smartmet-data-vaisala-gld360
Version:        17.6.26
Release:        1%{?dist}.fmi
Summary:        SmartMet Data Vaisala GLD360 Lightning Feed
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-vaisala-gld360
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	smartmet-qdtools
Requires:	bzip2

%description
SmartMet data ingest module for Vaisala global lightning feed.

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{_sysconfdir}/systemd/system
mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/tmp/data/vaisala-gld360
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/vaisala-gld360/{bin,cnf}
mkdir -p .%{smartmetroot}/data/vaisala-gld360/world/lightning/querydata
mkdir -p .%{smartmetroot}/data/incoming/vaisala-gld360

cat > %{buildroot}%{smartmetroot}/run/data/vaisala-gld360/cnf/socketreader-config.json <<EOF
{
    "host": "localhost",
    "port": 12345,
    "saveinterval": 5,
    "dir": "/smartmet/data/incoming/vaisala-gld360/"
}
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/vaisala-gld360.cron <<EOF
*/5 * * * * /smartmet/run/data/vaisala-gld360/bin/doflash.sh &> /smartmet/logs/data/vaisala-gld360.log
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_vaisala-gld360 <<EOF
#!/bin/sh
# Clean Vaisala GLD360 data
cleaner -maxfiles 2 '_gld360_world_lightning.sqd' %{smartmetroot}/data/vaisala-gld360/world
cleaner -maxfiles 2 '_gld360_world_lightning.sqd' %{smartmetroot}/editor/in

# Clean incoming lightning data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/vaisala-gld360 -type f -mmin +10080 -delete
EOF


install -m 755 %_topdir/SOURCES/smartmet-data-vaisala-gld360/vaisala-gld360-socketreader.py %{buildroot}%{smartmetroot}/run/data/vaisala-gld360/bin/
install -m 755 %_topdir/SOURCES/smartmet-data-vaisala-gld360/doflash.sh %{buildroot}%{smartmetroot}/run/data/vaisala-gld360/bin/
install -m 644 %_topdir/SOURCES/smartmet-data-vaisala-gld360/vaisala-gld360-socketreader.service %{buildroot}%{_sysconfdir}/systemd/system/
install -m 644 %_topdir/SOURCES/smartmet-data-vaisala-gld360/vaisala-gld360-sshtunnel.service %{buildroot}%{_sysconfdir}/systemd/system/


%post
systemctl enable vaisala-gld360-sshtunnel
systemctl enable vaisala-gld360-socketreader

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/vaisala-gld360.cron
%config(noreplace) %{smartmetroot}/run/data/vaisala-gld360/cnf/socketreader-config.json
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_vaisala-gld360
%attr(2775,smartmet,smartmet)  %dir %{smartmetroot}/data/incoming/vaisala-gld360
%{smartmetroot}/*
%{_sysconfdir}/systemd/system/*

%changelog
* Mon Jun 26 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.6.26-1.el7.fmi
- Initial Version
