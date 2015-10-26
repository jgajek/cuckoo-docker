#
# PostgreSQL database container for Cuckoo malware sandbox
#

FROM ubuntu:15.04
MAINTAINER Jacob Gajek <jacob.gajek@esentire.com>

# Install the PostgreSQL server
RUN apt-get install -y postgresql-9.4

# Replace the default PostgreSQL configuration files
COPY pg_hba.conf      /etc/postgresql/9.4/main/pg_hba.conf
COPY postgresql.conf  /etc/postgresql/9.4/main/postgresql.conf

# Run the rest of the build as the postgres user
USER postgres

# Start the PostgreSQL service and create the Cuckoo database
RUN service postgresql start &&\
 psql -c "CREATE USER sandbox PASSWORD 'cuck00!'" &&\
 psql -c "CREATE DATABASE cuckoo WITH TEMPLATE template0 ENCODING 'UTF-8'" &&\
 psql -c "GRANT ALL ON DATABASE cuckoo TO sandbox"

# Expose the PostgreSQL TCP port
EXPOSE 5432

# Add volumes to allow persistent data storage
VOLUME ["/var/lib/postgresql", "/var/log/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.4/bin/postgres", "-D", "/var/lib/postgresql/9.4/main", "-c", "config_file=/etc/postgresql/9.4/main/postgresql.conf"]
