from typing import Optional
from turandot.ui import CatcherStrategy
from turandot.gtk import TurandotGtkView, guithread


class GtkCatcher(CatcherStrategy):

    def __init__(self, view: TurandotGtkView):
        self.view = view
        self._connect_events()

    def _connect_events(self):
        """Connect event listeners to GUI"""
        self.view.elements.get_object("error_dialog").connect("delete_event", self._hide_dialog)
        self.view.elements.get_object("error_dialog_close_button").connect("clicked", self._hide_dialog)

    @guithread
    def handle_exception(self, e: Exception, tb: str):
        self.view.elements.get_object("error_type_dialog_label").set_text(str(type(e).__name__))
        self.view.elements.get_object("error_dialog_text_buffer").set_text(str(e) + "\n\n" + tb)
        self.view.elements.get_object("error_dialog").show()

    @guithread
    def _hide_dialog(self, *args):
        """Hide exception dialog"""
        self.view.elements.get_object("error_dialog").hide()
        # Returning false instead of true avoids a problem where method gets called over and over again
        return False
