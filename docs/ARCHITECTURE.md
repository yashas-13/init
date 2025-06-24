# Architecture Overview

```
+-------------------+     HTTP     +-------------------+

|   Dash Frontend   | <---------> |    Flask API w/ Auth|

+-------------------+             +-------------------+
        |                                   |
        | SQLAlchemy ORM                    |
        v                                   v
+-------------------+             +-------------------+
|    SQLite DB      |             |   Models/Tables   |
+-------------------+             +-------------------+
```

The application uses Flask as the API layer (now with bearer-token authentication) and Dash for the UI. SQLAlchemy manages the SQLite database described in `dbsetup.md`. Multiple dashboards (manufacturer, CFA, stockist) connect via authenticated REST calls.
