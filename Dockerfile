FROM python:3.7

# Install discover section
ENV AIIDA_PATH /app/.aiida
ENV PYTHONPATH /app

# AiiDA profile vars
ENV AIIDA_PROFILE judit
ENV AIIDADB_ENGINE postgresql_psycopg2
ENV AIIDADB_PASS aiida
ENV AIIDADB_NAME judit
ENV AIIDADB_HOST localhost
ENV AIIDADB_BACKEND django
ENV AIIDADB_PORT 5432
ENV AIIDADB_REPOSITORY_URI file:///app/.aiida/repository/judit
ENV AIIDADB_USER ruess
ENV default_user_email p.ruessmann@fz-juelich.de

# Materials Cloud vars
ENV EXPLORE_URL https://dev-www.materialscloud.org/explore/judit
ENV BOKEH_PREFIX "/judit"

# set workdir in container
WORKDIR /app

# copy files and directories
COPY judit-app ./judit-app
COPY prepare* ./

# install dependencies
RUN pip3 install -e judit-app
RUN reentry scan -r aiida

# prepare aiida config file
RUN ./prepare_db_connection.sh

# finally copy serve-app script 
COPY ./serve-app.sh /opt/

# start bokeh server
EXPOSE 5006
CMD ["/opt/serve-app.sh"]
