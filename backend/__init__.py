"""Backend package initialization."""

from .app import create_app
from .version import VERSION  # central version constant

__all__ = ["create_app"]
