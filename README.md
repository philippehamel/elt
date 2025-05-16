# elt
## Local Development
### Using venv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```bash
deactivate
```

### Using Docker (recommended)
```bash
# Build and start the containers
docker-compose up -d --build

# To stop the containers
docker-compose down
```