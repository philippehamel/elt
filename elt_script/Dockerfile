FROM python:3.11-slim

# Add PostgreSQL repository and install version 17 client tools
RUN apt-get update && apt-get install -y curl gnupg2 \
    && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y postgresql-client-17 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the ELT script
COPY elt_script.py .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]