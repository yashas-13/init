# Architecture Overview

```
+-------------------+     HTTP     +-------------------+
|   Dash Frontend   | <---------> |    Flask API      |
+-------------------+             +-------------------+
        |                                   |
        | SQLAlchemy ORM                    |
        v                                   v
+-------------------+             +-------------------+
|    SQLite DB      |             |   Models/Tables   |
+-------------------+             +-------------------+
```

The application uses Flask as the API layer and Dash for the UI. SQLAlchemy manages the SQLite database described in `dbsetup.md`.
