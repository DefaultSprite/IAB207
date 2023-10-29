"""
create_database (formerly known as createddatabase.py) creates the database.
"""

from server import db, create_app

def create_database() -> None:
    """
    This function creates a database. It firstly creates an App and assigns it's
    AppContent to ctx and pushes that AppContext to the current context so that
    when the database is created it can use that context.
    """
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    quit() # It is possible that this is redundant

create_database()