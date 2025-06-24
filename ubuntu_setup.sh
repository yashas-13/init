#!/usr/bin/env bash

# Automated setup for Ubuntu demo of Pharma SCM application
# WHY: Provide turnkey script to spin up environment with sample data
# WHAT: closes #setup-script
# HOW: delete this file to roll back or edit curl calls to extend

set -e

# Create virtual environment if missing
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

pip install -r requirements.txt

# Launch backend in background
python -m backend.run 5055 &
APP_PID=$!

# Give server time to start
sleep 3

# Obtain token for seeded admin
TOKEN=$(curl -s -X POST http://localhost:5055/api/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "admin@pharma.com", "password": "adminpass"}' | \
  python -c 'import sys, json; print(json.load(sys.stdin)["token"])')

echo "Obtained admin token: $TOKEN"

# Register a new manufacturer organization
curl -s -X POST http://localhost:5055/api/organizations \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"organization_id": "MANUF_EXTRA", "name": "Extra Manufacturer", "type": "Manufacturer"}'

echo "Added manufacturer MANUF_EXTRA"

# Add sample product under new manufacturer
curl -s -X POST http://localhost:5055/api/products \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test Product", "sku": "TEST123", "manufacturer_org_id": "MANUF_EXTRA"}'

echo "Added sample product TEST123"

# Shutdown server
kill $APP_PID
wait $APP_PID 2>/dev/null || true

echo "Setup complete."
