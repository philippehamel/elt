import subprocess
import time
import sys


def wait_for_postgres(host, max_retries=10, delay=10):
    """
    Wait for PostgreSQL to be ready.

    :param host: Hostname of the PostgreSQL server
    :param max_retries: Maximum number of retries
    :param delay: Delay between retries in seconds
    """
    for attempt in range(max_retries):
        try:
            subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True
            )
            print("PostgreSQL is ready!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"error connecting to PostgreSQL: {e}")
            print(f"retrying in {delay} seconds")
            print(f"attempt {attempt + 1} of {max_retries}")
            time.sleep(delay)
    print("max retries reached")
    return False


def test_db_connection(config):
    try:
        test_command = [
            "psql",
            "-h",
            config["host"],
            "-U",
            config["user"],
            "-d",
            config["dbname"],
            "-c",
            "SELECT 1",
        ]
        subprocess.run(
            test_command,
            env=dict(PGPASSWORD=config["password"]),
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Database connection failed: {e.stderr.decode()}")
        return False


source_config = {
    "dbname": "source_db",
    "user": "postgres",
    "password": "postgres",
    "host": "source_db",
}

destination_config = {
    "dbname": "destination_db",
    "user": "postgres",
    "password": "postgres",
    "host": "destination_db",
}

dump_command = [
    "pg_dump",
    "-h",
    source_config["host"],
    "-U",
    source_config["user"],
    "-d",
    source_config["dbname"],
    "-f",
    "/app/data_dump.sql",  # Use absolute path with WORKDIR
    "-w",  # Do not prompt for password
]

load_command = [
    "psql",
    "-h",
    destination_config["host"],
    "-U",
    destination_config["user"],
    "-d",
    destination_config["dbname"],
    "-a",
    "-f",
    "/app/data_dump.sql",  # Use absolute path with WORKDIR
]
source_subprocess_env = dict(PGPASSWORD=source_config["password"])
destination_subprocess_env = dict(PGPASSWORD=destination_config["password"])

print("checking source database connection...")
if not wait_for_postgres(source_config["host"]):
    print("could not connect to source database")
    sys.exit(1)

print("checking destination database connection...")
if not wait_for_postgres(destination_config["host"]):
    print("could not connect to destination database")
    sys.exit(1)

if not test_db_connection(source_config):
    print("failed to connect to source database")
    sys.exit(1)

try:
    print("starting database dump...")
    subprocess.run(
        dump_command, env=source_subprocess_env, check=True, capture_output=True
    )
    print("dump completed successfully")
except subprocess.CalledProcessError as e:
    print(f"dump failed: {e.stderr.decode()}")
    sys.exit(1)

try:
    print("starting database load...")
    subprocess.run(
        load_command, env=destination_subprocess_env, check=True, capture_output=True
    )
    print("load completed successfully")
except subprocess.CalledProcessError as e:
    print(f"load failed: {e.stderr.decode()}")
    sys.exit(1)
