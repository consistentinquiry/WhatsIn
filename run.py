#!/usr/bin/env python3
from whatsin import app #import form the whatsin/init.py
from whatsin.models import User, Fridge_item, Cupboard_item
import os
from whatsin.watcher import Watcher

def run():
    """ Sets up paramters of web server & executes"""
    debug = os.environ.get('APP_DEBUG', True)
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = int(os.environ.get('APP_PORT', 80))
    

    app.run(debug=debug, host=host, port=port)
    watcher01 = Watcher()
    watcher01.run()



if __name__ == "__main__":
    run()
