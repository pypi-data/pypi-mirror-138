import gi
gi.require_version('Gtk', '3.0')
from typing import Union
from tempfile import NamedTemporaryFile
from gi.repository import Gtk
from turandot.model import ModelUtils
from turandot.gtk.presentations import DatabaseDropdown, EnumDropdown
from turandot.model import TemplateAsset, CslAsset, ReferenceSource, ConversionAlgorithm


class TurandotGtkView:
    """Launch GTK application"""

    @staticmethod
    def _get_glade() -> str:
        """Get Glade file from assets"""
        return ModelUtils.get_asset_content("mainwindow.glade")

    @staticmethod
    def _get_icon() -> NamedTemporaryFile:
        """Dump icon to a temp file to use as GTK icon"""
        icon = NamedTemporaryFile(mode='w')
        icon.write(ModelUtils.get_asset_content("turandot.svg"))
        return icon

    def __init__(self):
        glade_str = self._get_glade()
        builder = Gtk.Builder()
        self.elements = builder.new_from_string(glade_str, len(glade_str))
        self.datadropdowns: dict[str, DatabaseDropdown] = {
            "template_dropdown": DatabaseDropdown(model=TemplateAsset),
            "template_editor_dropdown": DatabaseDropdown(model=TemplateAsset, new_option=True),
            "csl_dropdown": DatabaseDropdown(model=CslAsset),
            "csl_editor_dropdown": DatabaseDropdown(model=CslAsset, new_option=True)
        }
        self.enumdropdowns: dict[str, EnumDropdown] = {
            "conversion_algorithm_dropdown": EnumDropdown(ConversionAlgorithm),
            "reference_source_dropdown": EnumDropdown(ReferenceSource)
        }
        self.addressable_fields: dict[str, Gtk.Widget] = {}
        self.window: Gtk.ApplicationWindow = self.elements.get_object("mainwindow")
        self._add_datadropdowns()
        self._add_enumdropdowns()

    def _add_datadropdowns(self):
        """Add database-fed dropdowns to GUI"""
        self.get_element("template_dropdown_container").add(self.get_element("template_dropdown"))
        self.get_element("csl_dropdown_container").add(self.get_element("csl_dropdown"))
        self.get_element("template_editor_dropdown_container").add(self.get_element("template_editor_dropdown"))
        self.get_element("csl_editor_dropdown_container").add(self.get_element("csl_editor_dropdown"))
        self.get_element("template_dropdown").show()
        self.get_element("template_editor_dropdown").show()
        self.get_element("csl_editor_dropdown").show()

    def _add_enumdropdowns(self):
        """Add enum-based dropdowns to the GUI"""
        self.get_element("conversion_algorithm_dropdown_container").add(self.get_element("conversion_algorithm_dropdown"))
        self.get_element("conversion_algorithm_dropdown").show()
        self.get_element("reference_source_dropdown_container").add(self.get_element("reference_source_dropdown"))
        self.get_element("reference_source_dropdown").show()

    def get_element(self, element_id: str) -> Union[DatabaseDropdown, EnumDropdown, Gtk.Widget, None]:
        """Get widget from view"""
        dd = self.datadropdowns.get(element_id, None)
        if dd is not None:
            return dd
        ed = self.enumdropdowns.get(element_id, None)
        if ed is not None:
            return ed
        af = self.addressable_fields.get(element_id, None)
        if af is not None:
            return af
        return self.elements.get_object(element_id)

    def show_main(self):
        """Show main window"""
        self.window.connect("destroy", Gtk.main_quit)
        icon = self._get_icon()
        self.window.set_icon_from_file(icon.name)
        icon.close()
        self.window.show()
        Gtk.main()
