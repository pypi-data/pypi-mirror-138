import sys
import logger, logging
from os import path
from ValidationHandler import ValidationHandler
from FilterHandler import FilterHandler
from OPSHandler import OPSHandler
from GAHandler import GAHandler
from MainHandler import Handler
from HandlerFinder import HandlerFinder
from ResultsHandler import ResultsHandler
from Utils import cleanup_temporary_directory, __DIR__
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def add_all_from_file(files: list, builder: Gtk.Builder) -> None:
    for f in files:
        builder.add_from_file(path.abspath(
            path.join(__DIR__, "Views", f)))


def main():
    logger.init()

    builder: Gtk.Builder = Gtk.Builder()
    add_all_from_file([
        "main.glade",
        "about.glade",
        "ga.glade",
        "ops.glade",
        "varcut.glade",
        "corrcut.glade",
        "autocorrcut.glade",
        "cross_validation.glade",
        "yrlno.glade",
        "external_validation.glade",
        "results.glade",
    ], builder)


    handler = Handler(builder)

    # Register handlers
    handler.register_handler(GAHandler(builder, handler))
    handler.register_handler(OPSHandler(builder, handler))
    handler.register_handler(ResultsHandler(builder))
    handler.register_handler(ValidationHandler(builder, handler))
    handler.register_handler(FilterHandler(builder, handler))

    handlers = [handler] + handler.get_handlers()

    # Connect signals and launch the GUI
    builder.connect_signals(HandlerFinder(handlers))
    window = builder.get_object('main_window')
    window.show_all()
    Gtk.main()

    # Cleanup temporary directory when the GUI is closed
    cleanup_temporary_directory()

if __name__ == '__main__':
    main()