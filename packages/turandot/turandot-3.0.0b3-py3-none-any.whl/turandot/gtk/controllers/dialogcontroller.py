from typing import Optional, Callable
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from turandot.model import FileSelectPersistApi
from turandot.gtk import TurandotGtkView, FileTypeFilterFactory, TypeFilterEnum
from turandot.gtk.controllers import BaseController


class DialogController(BaseController):
    """Controller to draw various GTK dialogs"""

    def connect_events(self):
        self.view.get_element("confirm_dialog_cancel_button").connect("clicked", self._cancel_confirm)
        self.view.get_element("confirm_dialog").connect("delete_event", self._cancel_confirm)

    def _cancel_confirm(self, *args):
        """Hide delete confirmation dialog on cancel without doing anything"""
        GLib.idle_add(self.view.get_element("confirm_dialog").hide)
        return True

    @staticmethod
    def _file_chooser_dialog(
        view: TurandotGtkView,
        return_entry_id: str,
        init_dir: Optional[Path] = None,
        typefilter: TypeFilterEnum = TypeFilterEnum.ALL,
        title: str = "Choose a file"
    ):
        """Show file chooser dialog"""
        dialog = Gtk.FileChooserDialog(
            title,
            view.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        FileTypeFilterFactory.apply(typefilter, dialog)
        if init_dir is not None:
            dialog.set_current_folder(str(init_dir))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            return_entry = view.get_element(return_entry_id)
            filename = Path(dialog.get_filename())
            return_entry.set_text(str(filename))
            FileSelectPersistApi.set(return_entry_id, filename.parent)
        dialog.destroy()
        return True

    @staticmethod
    def db_fed_file_chooser_dialog(
        view: TurandotGtkView,
        return_entry_id: str,
        typefilter: TypeFilterEnum = TypeFilterEnum.ALL,
        title: str = "Choose a file"
    ):
        """Show file chooser dialog, open recently used directory"""
        path = FileSelectPersistApi.get(return_entry_id)
        DialogController._file_chooser_dialog(view, return_entry_id, path, typefilter, title)
        return True

    @staticmethod
    def show_confirm_dialog(view: TurandotGtkView, labeltext: str, callback: Callable):
        """Show delete confirmation dialog"""
        view.get_element("confirm_dialog_ok_button").connect("clicked", callback)
        view.get_element("confirm_dialog_label").set_text(labeltext)
        view.get_element("confirm_dialog").show()
