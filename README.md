#Docker Containers for Cuckoo Malware Sandbox

##jgajek/cuckoo:esxlab
Data container holding Cuckoo configuration for vSphere-hosted malware lab

##jgajek/cuckoo:1.3-Optiv
Cuckoo Malware Sandbox build based on:
- Ubuntu 15.04 base OS
- Modified Cuckoo malware sandbox from Optiv (https://github.com/brad-accuvant)
- Django web UI behind nginx reverse proxy
- PostgreSQL database
- vSphere machinery module
- Cuckoo configuration must be pulled in from a data container (such as the one above)
- docker-compose file for easy creation and destruction of containers
