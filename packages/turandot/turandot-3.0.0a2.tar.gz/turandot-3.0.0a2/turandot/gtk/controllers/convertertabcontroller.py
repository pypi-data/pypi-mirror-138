from turandot.gtk.controllers import BaseController, DialogController
from turandot.ui import background, catch_exception
from turandot.gtk import guithread, TypeFilterEnum
from turandot.model import ReferenceSource, ZoteroConnector, ConfigModel
import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import ComboBoxText, ListStore
from gi.repository import GLib


class ConverterTabController(BaseController):
    """Controller for the ComboBoxes on the 'Converter' tab"""

    def connect_events(self):
        self.view.get_element("reference_source_dropdown").set_change_callback(self.reference_source_callback)
        self.view.get_element("source_file_select_button").connect("clicked", self.select_source_file)
        self.view.get_element("csljson_file_select_button").connect("clicked", self.select_csljson_file)
        self.view.get_element("button_zotero_update_button").connect("clicked", self.update_zotero_libs)

    def select_source_file(self, *args):
        DialogController.db_fed_file_chooser_dialog(
            view=self.view,
            return_entry_id="source_file_entry",
            typefilter=TypeFilterEnum.MARKDOWN
        )

    @guithread
    def reference_source_callback(self, *args):
        entry = self.view.get_element("reference_source_dropdown").get_selected_value()
        if entry.value <= 1:
            self.view.get_element("citation_style_label").hide()
            self.view.get_element("csl_dropdown").hide()
        else:
            self.view.get_element("citation_style_label").show()
            self.view.get_element("csl_dropdown").show()
        if entry == ReferenceSource.ZOTERO:
            self.view.get_element("zotero_lib_label").show()
            self.view.get_element("zotero_lib_dropdown").show()
            self.view.get_element("button_zotero_update_button").show()
            self.update_zotero_libs()
        else:
            self.view.get_element("zotero_lib_label").hide()
            self.view.get_element("zotero_lib_dropdown").hide()
            self.view.get_element("button_zotero_update_button").hide()
        if entry == ReferenceSource.JSON:
            self.view.get_element("csljson_file_label").show()
            self.view.get_element("csljson_file_entry").show()
            self.view.get_element("csljson_file_select_button").show()
        else:
            self.view.get_element("csljson_file_label").hide()
            self.view.get_element("csljson_file_entry").hide()
            self.view.get_element("csljson_file_select_button").hide()

    @background
    @catch_exception
    def update_zotero_libs(self, *args):
        libs = ZoteroConnector(ConfigModel().get_dict()).get_libraries()
        store = ListStore(str, str)
        for i in libs:
            store.append([i["name"], str(i["id"])])
        self.draw_zotero_options(store)

    @guithread
    def draw_zotero_options(self, store: ListStore):
        self.view.get_element("zotero_lib_dropdown").set_model(store)
        self.view.get_element("zotero_lib_dropdown").set_active(0)

    def select_csljson_file(self, *args):
        DialogController.db_fed_file_chooser_dialog(
            view=self.view,
            return_entry_id="csljson_file_entry",
            typefilter=TypeFilterEnum.JSON
        )
