from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
templates = Jinja2Templates(directory=str(BASE_DIR))
TEMPLATES_DIR = BASE_DIR / "templates"

print("TEMPLATES_DIR:", TEMPLATES_DIR)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
