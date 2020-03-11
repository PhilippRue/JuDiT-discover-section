FROM python:3.7

# Install discover section
ENV AIIDA_PATH /app
ENV PYTHONPATH /app
WORKDIR /app/judit

COPY data ./data
COPY setup.py ./
RUN pip install -e .
RUN reentry scan -r aiida
COPY .docker/serve-app.sh /opt/
COPY .docker/config.json $AIIDA_PATH/.aiida/

# start bokeh server
EXPOSE 5006
CMD ["/opt/serve-app.sh"]
