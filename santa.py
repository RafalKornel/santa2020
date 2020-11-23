from app import create_app, db
from app.models import User, Group
import os

app = create_app( os.environ.get("FLASK_CONFIG", "development"))

@app.cli.command("create_tables")
def create_tables():
    db.create_all()

@app.cli.command("drop_tables")
def drop_tables():
    db.drop_all()

@app.shell_context_processor
def make_shell_context():
    return { "db":db, "User":User, "Group":Group }