__version__ = "0.1.0"
from fastapi.staticfiles import StaticFiles
from .core.main import create_app

app = create_app()
