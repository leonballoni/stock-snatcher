FROM apache/airflow:slim-latest-python3.12

RUN pip install --no-cache-dir psycopg2-binary

COPY src/airflow/dags/ /opt/airflow/dags
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint to the custom script
ENTRYPOINT ["/entrypoint.sh"]

# Default command to start the web server
CMD ["airflow", "webserver"]
