# Architecture Overview

```
+-------------------+     HTTP     +-------------------+

|   Dash Frontend   | <---------> |    Flask API w/ Auth|

+-------------------+             +-------------------+
        |                                   |
        | SQLAlchemy ORM                    |
        v                                   v
+-------------------+             +-------------------+
|  DB via DATABASE_URL |             |   Models/Tables   |
+-------------------+             +-------------------+
```

The application uses Flask as the API layer (now with bearer-token authentication) and Dash for the UI. SQLAlchemy manages the database configured through the `DATABASE_URL` environment variable (defaulting to SQLite). Multiple dashboards (manufacturer, CFA, stockist) connect via authenticated REST calls.
