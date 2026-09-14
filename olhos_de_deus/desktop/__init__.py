"""Windows desktop application for Olhos de Deus."""

from .controller import DesktopController
from .paths import AppPaths
from .storage import DesktopStorage

__all__ = ["AppPaths", "DesktopController", "DesktopStorage"]
