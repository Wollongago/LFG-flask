#!/bin/bash

# Adjust somaxcon
if [ -f /wproc/somaxconn ]; then
    echo "64000" > /wproc/somaxconn;
else
	sysctl -w net.core.somaxconn=64000
fi

# Launch Uwsgi Process.
exec uwsgi --hook-master-start "unix_signal:2 gracefully_kill_them_all" --ini /etc/uwsgi/apps-enabled/http/application.ini
