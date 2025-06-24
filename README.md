# Pharma SCM Application

Version: 0.1.0

This project implements an initial prototype for the pharmaceutical supply chain management app described in `Pharmaceutical Supply Chain App Design_.md` and `dbsetup.md`.

## Today's Changes

- Added Flask/Dash backend with SQLite database models.
- Implemented `/api/organizations` endpoint for creating organizations.
- Provided minimal Dash UI placeholder.
- Included database initialization on startup.

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:

   ```bash
   python -m backend.run
   ```

3. Create an organization (example using `curl`):

   ```bash
   curl -X POST http://localhost:5000/api/organizations \
        -H 'Content-Type: application/json' \
        -d '{"name": "Test Org", "type": "Manufacturer"}'
   ```

SQLite database `pharma.db` will be created automatically in the project root.
