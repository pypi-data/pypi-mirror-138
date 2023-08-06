from typing import Optional, Callable, Union
import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import ComboBoxText, ListStore
from turandot.model import DatabaseAsset
from turandot.ui import background
from turandot.gtk import guithread, DropdownPreSelections
from peewee import DoesNotExist


class DatabaseDropdown(ComboBoxText):
    """Database-fed Combobox widget"""

    NEW_OPT_TEXT = "- create new entry -"

    def _empty_callback(self):
        """Empty callback for initialization"""
        return

    def __init__(self, model: type(DatabaseAsset), new_option: bool = False):
        self.model = model
        self.new_option = new_option
        self.change_callback: Callable = self._empty_callback
        self.contains_ids: list[int] = []
        ComboBoxText.__init__(self)

    def set_change_callback(self, f: Callable):
        """Attach new function to call on change"""
        self.change_callback = f
        self.connect("changed", self.change_callback)

    @background
    def update(self, preselect: Union[DropdownPreSelections, int, type(None)] = None):
        """Update ComboBox from database"""
        preupdate = self.get_active_id()
        preupdate = None if preupdate is None else int(preupdate)
        elemls = self.model.get_all(expand=True)
        self.contains_ids = []
        store = ListStore(str, str)
        if self.new_option:
            store.append([DatabaseDropdown.NEW_OPT_TEXT, "0"])
        for i in elemls:
            self.contains_ids.append(i.dbid)
            store.append([i.title, str(i.dbid)])
        self._show_update(store, preselect, preupdate)

    @guithread
    def _show_update(
        self,
        store: ListStore,
        preselect: Union[DropdownPreSelections, int, type(None)] = None,
        preupdate_selection: Optional[int] = None
    ):
        self.set_model(store)
        if preselect is not None:
            self.set_selected_id(preselect, preupdate_selection)
            self.change_callback()

    def set_selected_id(
        self,
        selid: Union[DropdownPreSelections, int],
        preupdate_selection: Optional[int] = None
    ):
        """Set selected value with database id"""
        if selid == DropdownPreSelections.FIRST_ELEMENT:
            self.set_active(0)
        elif selid == DropdownPreSelections.SAME_ELEMENT:
            if preupdate_selection in self.contains_ids:
                self.set_active_id(str(preupdate_selection))
            else:
                self.set_active(0)
        else:
            if selid in self.contains_ids:
                self.set_active_id(str(selid))
            else:
                self.set_active(0)

    def get_selected_asset(self) -> Optional[DatabaseAsset]:
        """Get DatabaseAsset currently selected"""
        dbid = self.get_active_id()
        if dbid is None:
            return None
        dbid = int(dbid)
        try:
            entry = self.model.get(dbid, expand=True)
            return entry
        except DoesNotExist:
            return None
