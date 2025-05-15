FROM python:3.11-slim

# Install PostgreSQL client
RUN apt-get update \
    && apt-get install -y wget gnupg2 lsb-release \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/postgresql.list \
    && apt-get update \
    && apt-get install -y postgresql-client-15 \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy script
COPY elt_script.py .

# Create directory for dump file
RUN mkdir -p /app/data

CMD [ "python", "elt_script.py" ]