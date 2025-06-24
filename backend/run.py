"""Entry point for running the Flask application."""

from .app import create_app


def main(port: int = 5000):
    """Launch the development server on the given port."""
    app = create_app()
    # WHY: allow running on alternate ports when 5000 is taken
    # WHAT: closes #improve-readme
    # HOW: pass a new port or revert to default 5000
    app.run(debug=True, port=port)


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    main(port)

