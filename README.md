#Docker Containers for Cuckoo Malware Sandbox

##jgajek/cuckoo-docker:esxlab
Container holding Cuckoo configuration for vSphere-hosted malware lab

##jgajek/cuckoo-docker:storage
Data container for Cuckoo storage area

##jgajek/cuckoo-docker:1.3-NG
Cuckoo Malware Sandbox build based on:
- Ubuntu 16.04 base OS
- Modified Cuckoo malware sandbox from Spender (https://github.com/spender-sandbox)
- Django web UI behind nginx reverse proxy
- vSphere machinery module
- Tor transparent proxy
- Suricata with ET ruleset
- Cuckoo configuration must be pulled in from a separate container (such as the one above)
- docker-compose file for easy creation and destruction of containers
