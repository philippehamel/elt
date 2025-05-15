# elt
## Local Development
### Using venv
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Using Docker (recommended)
```bash
# Build and start the containers
docker-compose up --build

# To run in detached mode
docker-compose up -d

# To stop the containers
docker-compose down
```