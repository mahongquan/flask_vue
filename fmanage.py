#!/usr/bin/env python

import flask_script

#from myapp.comm import send_update
from server import app

manager = flask_script.Manager(app)


@manager.command
def runserver(debug=True, use_reloader=True):
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=debug,
        use_reloader=use_reloader,
    )

if __name__ == '__main__':
    try:
        manager.run()
    except KeyboardInterrupt:
        pass
