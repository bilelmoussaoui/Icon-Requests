#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys
sys.path.insert(1, '@pyexecdir@')
sys.path.insert(1, '@pythondir@')
from gi.repository import Gio
import application
import logging
import locale
import gettext
_ = gettext.gettext
import argparse
import faulthandler
from os import path, environ as env

if __name__ == "__main__":

    #locale.bindtextdomain('Bullet', "@localedir@")
    locale.textdomain('Bullet')
    #gettext.bindtextdomain('Bullet', "@localedir@")
    gettext.textdomain('Bullet')

    #env["DATA_DIR"] = "@pkgdatadir@"
    #env["LOCALE_DIR"] = "@localedir@"

    parser = argparse.ArgumentParser(prog="Gnome Bullet")
    parser.add_argument("--debug", "-d", action="store_true",
                        help=_("start in debug mode"))
    parser.add_argument("--version", "-v", action="store_true",
                        help=_("Gnome Bullet version number"))
    parser.add_argument("--about", action="store_true",
                        help=_("Show about dialog"))
    args = parser.parse_args()

    level = logging.ERROR
    if args.debug:
        level = logging.DEBUG
        faulthandler.enable()
    logging.basicConfig(level=level,
                        format='[%(levelname)s] - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    #resource = Gio.resource_load(path.join('@pkgdatadir@',
    #                                        'gnome-bullet.gresource'))
    #Gio.Resource._register(resource)
    if args.version:
        sys.exit("Version : @VERSION@")
    elif args.about:
        about_dialog = application.Application.about_dialog()
        about_dialog.run()
        about_dialog.destroy()
        sys.exit()
    else:
        app = application.Application()
        exit_status = app.run(None)
        sys.exit(exit_status)
