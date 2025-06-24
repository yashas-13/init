# Pharma SCM Application

Version: 0.2.0

This project implements an initial prototype for the pharmaceutical supply chain management app described in `Pharmaceutical Supply Chain App Design_.md` and `dbsetup.md`.

## Today's Changes

- Added sample seed data for organizations, users, product and inventory.
- Implemented authentication endpoints `/api/users` and `/api/login`.
- Added protected `/api/inventory` endpoint.
- Created Dash dashboards for manufacturer, CFA and stockist roles.
- Server now listens on port `8787`.

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:

   ```bash
   python -m backend.run
   ```

3. Authenticate and list inventory (examples using `curl`):

   ```bash
   # login with seeded manufacturer user
   curl -X POST http://localhost:8787/api/login \
        -H 'Content-Type: application/json' \
        -d '{"email": "manuf@example.com", "password": "password"}'
   # use the returned token
   curl http://localhost:8787/api/inventory \
        -H "Authorization: <TOKEN>"
   ```

SQLite database `pharma.db` will be created automatically in the project root.
