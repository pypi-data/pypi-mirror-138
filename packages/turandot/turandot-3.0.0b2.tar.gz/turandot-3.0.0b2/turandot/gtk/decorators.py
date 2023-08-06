from functools import wraps
from gi.repository import GLib


def guithread(f):
    """Decorator: Push execution to GUI thread"""
    @wraps(f)
    def process(*args, **kwargs):
        GLib.idle_add(f, *args, **kwargs)
    return process
