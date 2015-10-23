Docker containers for Cuckoo malware analysis sandbox.

Split into three containers:

1) Database container running PostgreSQL.

2) Application container running Cuckoo and its Django UI via nginx and uwsgi.

3) Data volume container for the deployment-specific configuration files.

