import os
from APP import create_app,db
from APP.modle import User
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manger = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app = app,
                db = db,
                User = User)
manger.add_command('shell', Shell(make_context= make_shell_context))
manger.add_command('db', MigrateCommand)

@manger.command
def test():
    """RUN THE UNIT TEST"""
    import unittest
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(test)

if __name__ == '__main__':
    # app.run(debug= True)
    manger.run()