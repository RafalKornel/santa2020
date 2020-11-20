from app import create_app, db
from app.models import User, Group
from flask_migrate import Migrate

app = create_app("development")

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return { "db":db, "User":User, "Group":Group }