
# Pharma SCM Application

Version: 0.2.2

This project implements an initial prototype for the pharmaceutical supply chain management app described in `dbsetup.md`.

## Today's Changes

- Seeded database with sample organizations, users, and a product.
- Added authentication with `/api/login` and bearer tokens.
- Created endpoints for users, products, inventory, requests, approvals, and audit logs.
- Implemented role-based access on sensitive routes.
- Added multipage Dash dashboards for manufacturer, CFA, and stockist.
- Now reads `DATABASE_URL` from environment for DB connection.
- Added `/api/version` endpoint to report backend version.

## Quick Start

1. (Optional) set a custom database URL:

   ```bash
   export DATABASE_URL=sqlite:///pharma.db
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server (optional port arg):

   ```bash
   python -m backend.run 5055
   ```

4. Check the backend version:

   ```bash
   curl http://localhost:5055/api/version
   ```

5. Obtain a token and create a product (example):

   ```bash
   # login with seeded admin user
   curl -X POST http://localhost:5055/api/login \
        -H 'Content-Type: application/json' \
        -d '{"email": "admin@pharma.com", "password": "adminpass"}'

   # set TOKEN from response and create product
   curl -X POST http://localhost:5055/api/products \
        -H "Authorization: Bearer $TOKEN" \
        -H 'Content-Type: application/json' \
        -d '{"name": "Pain Reliever", "sku": "PR001", "manufacturer_org_id": "MANUF1"}'
   ```

If `DATABASE_URL` is not set, SQLite database `pharma.db` will be created automatically in the project root.
