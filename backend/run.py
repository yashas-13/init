"""Entry point for running the Flask application."""

from .app import create_app


def main():
    app = create_app()
    # Running with debug for development
    app.run(debug=True)


if __name__ == "__main__":
    main()

