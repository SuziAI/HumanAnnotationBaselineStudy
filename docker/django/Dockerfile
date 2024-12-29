FROM python:3.12-slim-bookworm

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install required packages
RUN apt-get update \
    && apt-get install -y \
        gosu \
        dos2unix \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/development.txt

# Set up entrypoint script
COPY ./docker/django/docker-entrypoint.sh /docker-entrypoint.sh
RUN dos2unix /docker-entrypoint.sh \
    && chmod 755 /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh" ]