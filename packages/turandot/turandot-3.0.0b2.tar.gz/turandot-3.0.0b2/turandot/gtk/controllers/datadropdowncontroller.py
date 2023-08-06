from typing import Optional, Union
from pathlib import Path
from turandot.model import TemplateAsset, CslAsset
from turandot.ui import catch_exception
from turandot.gtk import DropdownPreSelections, TurandotGtkView, TypeFilterEnum
from turandot.gtk.controllers import BaseController, DialogController
from turandot.gtk.presentations import DatabaseDropdown


class DataDropdownController(BaseController):
    """Controller for 'Template' and 'CSL' tabs"""

    def __init__(self, view: TurandotGtkView):
        BaseController.__init__(self, view=view)
        self._update_templates(preselect=DropdownPreSelections.FIRST_ELEMENT)
        self._update_csl(preselect=DropdownPreSelections.FIRST_ELEMENT)

    def _update_templates(self, preselect: Union[DropdownPreSelections, int, type(None)] = None):
        """Update entries in template dropdowns"""
        self.view.get_element("template_dropdown").update(preselect=DropdownPreSelections.SAME_ELEMENT)
        self.view.get_element("template_editor_dropdown").update(preselect=preselect)

    def _update_csl(self, preselect: Union[DropdownPreSelections, int, type(None)] = None):
        """Update entries in CSL dropdowns"""
        self.view.get_element("csl_dropdown").update(preselect=DropdownPreSelections.SAME_ELEMENT)
        self.view.get_element("csl_editor_dropdown").update(preselect=preselect)

    def connect_events(self):
        self.view.get_element("template_editor_dropdown").set_change_callback(self._on_template_editor_dropdown_change)
        self.view.get_element("csl_editor_dropdown").set_change_callback(self._on_csl_editor_dropdown_change)
        self.view.get_element("tmpl_base_select_button").connect("clicked", self._browse_template)
        self.view.get_element("csl_select_button").connect("clicked", self._browse_csl)
        self.view.get_element("tmpl_save_button").connect("clicked", self._save_template)
        self.view.get_element("tmpl_delete_button").connect("clicked", self._delete_template)
        self.view.get_element("csl_save_button").connect("clicked", self._save_csl)
        self.view.get_element("csl_delete_button").connect("clicked", self._delete_csl)

    def _on_template_editor_dropdown_change(self, *args):
        """Draw template settings to 'Template' tab"""
        asset = self.view.get_element("template_editor_dropdown").get_selected_asset()
        if asset is None:
            self.view.get_element("tmpl_delete_button").set_sensitive(False)
            self.view.get_element("tmpl_base_file_enty").set_text("")
            self.view.get_element("tmpl_allow_jinja").set_active(False)
            self.view.get_element("tmpl_allow_mako").set_active(False)
        else:
            self.view.get_element("tmpl_delete_button").set_sensitive(True)
            self.view.get_element("tmpl_base_file_enty").set_text(str(asset.path))
            self.view.get_element("tmpl_allow_jinja").set_active(asset.allow_jinja)
            self.view.get_element("tmpl_allow_mako").set_active(asset.allow_mako)

    def _on_csl_editor_dropdown_change(self, *args):
        """Draw CSL settings to 'CSL' tab"""
        asset = self.view.get_element("csl_editor_dropdown").get_selected_asset()
        if asset is None:
            self.view.get_element("csl_delete_button").set_sensitive(False)
            self.view.get_element("csl_base_file_enty").set_text("")
        else:
            self.view.get_element("csl_delete_button").set_sensitive(True)
            self.view.get_element("csl_base_file_enty").set_text(str(asset.path))

    def _browse_template(self, *args):
        """Create file chooser dialog to pick template base file"""
        DialogController.db_fed_file_chooser_dialog(
            view=self.view,
            return_entry_id="tmpl_base_file_enty",
            typefilter=TypeFilterEnum.TMPL,
            title="Select template base"
        )

    def _browse_csl(self, *args):
        """Create file chooser dialog to pick csl base file"""
        DialogController.db_fed_file_chooser_dialog(
            view=self.view,
            return_entry_id="csl_base_file_enty",
            typefilter=TypeFilterEnum.CSL,
            title="Select csl file"
        )

    @catch_exception
    def _save_template(self, *args):
        """Save data from GUI as template, update menu"""
        asset = self.view.get_element("template_editor_dropdown").get_selected_asset()
        p = Path(self.view.get_element("tmpl_base_file_enty").get_text())
        aj = self.view.get_element("tmpl_allow_jinja").get_active()
        am = self.view.get_element("tmpl_allow_mako").get_active()
        if asset is None:
            asset = TemplateAsset(p, am, aj)
        else:
            asset.path = p
            asset.allow_mako = am
            asset.allow_jinja = aj
        asset.save()
        self._update_templates(preselect=asset.dbid)

    def _delete_template(self, *args):
        """Show delete confirmation dialog"""
        DialogController.show_confirm_dialog(
            self.view,
            "Remove template entry?\n(No files will be deleted)",
            self._delete_template_confirmed
        )

    def _delete_template_confirmed(self, *args):
        """Delete selected template from database, update menu"""
        self.view.get_element("confirm_dialog").hide()
        asset = self.view.get_element("template_editor_dropdown").get_selected_asset()
        if asset is not None:
            asset.delete()
        self._update_templates(DropdownPreSelections.FIRST_ELEMENT)

    @catch_exception
    def _save_csl(self, *args):
        """Save data from GUI as CSL entry, update menus"""
        asset = self.view.get_element("csl_editor_dropdown").get_selected_asset()
        p = Path(self.view.get_element("csl_base_file_enty").get_text())
        if asset is None:
            asset = CslAsset(p)
        else:
            asset.path = p
        asset.save()
        self._update_csl(preselect=asset.dbid)

    def _delete_csl(self, *args):
        """Show delete confirmation dialog"""
        DialogController.show_confirm_dialog(
            self.view,
            "Remove csl entry?\n(No files will be deleted)",
            self._delete_csl_confirmed
        )

    def _delete_csl_confirmed(self, *args):
        """Delete selected csl entry from database, update menus"""
        self.view.get_element("confirm_dialog").hide()
        asset = self.view.get_element("csl_editor_dropdown").get_selected_asset()
        if asset is not None:
            asset.delete()
        self._update_csl(DropdownPreSelections.FIRST_ELEMENT)
