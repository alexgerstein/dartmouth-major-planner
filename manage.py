import os
import sys
import subprocess
from dartplan import create_app
from dartplan.database import db
from dartplan.models import *
from scrapers.scrape_all import scrape_all
from scrapers.scrape_update import scrape_update
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from flask_assets import ManageAssets

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the models by default."""
    return {'app': app, 'db': db, 'User': User, 'Offering': Offering,
            'Course': Course, 'Hour': Hour, 'Plan': Plan,
            'Department': Department, 'Distributive': Distributive,
            'Term': Term}


@manager.command
def test():
    status = subprocess.call("bash ./scripts/test.sh", shell=True)
    sys.exit(status)


@manager.command
def scrape(all=False):
    if all:
        scrape_all()
    else:
        scrape_update()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets)

if __name__ == '__main__':
    manager.run()
