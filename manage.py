import os
import sys
import subprocess
from dartplan import create_app
from dartplan.database import db
from flask.ext.script import Manager, Shell, Server

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)

TEST_CMD = "py.test --cov-report term-missing --cov-config .coveragerc \
                    --cov . --boxed -n2 tests/"


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db}


@manager.command
def tests():
    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
