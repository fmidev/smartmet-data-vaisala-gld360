# SmartMet Data Ingestion Module for Vaisala GLD360 Lightning Feed

* edit /home/smartmet/.ssh/config
```
Host vaisala-gld360
Hostname FILL_IP_FROM_VAISALA
User FILL_USER_FROM_VAISALA
LocalForward 12345 127.0.0.1:FILL_PORT_FROM_VAISALA
```
* check /smartmet/run/data/vaisala-gld360/cnf/socketreader-config.json
```
{
    "host": "localhost",
    "port": 12345,
    "saveinterval": 5,
    "dir": "/smartmet/data/incoming/vaisala-gld360/"
}
```
* both files should have same port, you can choose freely (default 12345)
* systemctl restart vaisala-gld360-sshtunnel restart
* systemctl restart vaisala-gld360-socketreader restart
* check log: journalctl -f -u vaisala-gld360-sshtunnel and journalctl -f -u vaisala-gld360-socketreader
