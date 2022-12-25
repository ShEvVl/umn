from app.routes import main
from app.models import Data, db
from app.fill_db import test_db


@main.shell_context_processor
def make_shell_context():
    return {"db": db, "Data": Data, "test_db": test_db}
