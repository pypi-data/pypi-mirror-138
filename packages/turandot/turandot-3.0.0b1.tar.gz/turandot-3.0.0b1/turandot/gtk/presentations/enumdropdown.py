from enum import EnumMeta
from typing import Callable, Union
import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import ComboBoxText, ListStore

from turandot.ui import EnumTranslations


class EnumDropdown(ComboBoxText):
    """Enum-based Combobox widget"""

    def _empty_callback(self):
        """Empty callback for initialization"""
        return

    def __init__(self, model: EnumMeta, text_based=False):
        self.text_based = text_based
        self.model = model
        ComboBoxText.__init__(self)
        self._create_options()
        self.change_callback: Callable = self._empty_callback

    def _create_options(self):
        """Set combobox options from enum values"""
        store = ListStore(str, str)
        for i in self.model:
            store.append([EnumTranslations.get(i), str(i.value)])
        self.set_model(store)
        self.set_active(0)

    def get_selected_value(self):
        """Get selected enum member"""
        if self.text_based:
            n = self.get_active_id()
        else:
            n = int(self.get_active_id())
        return self.model(n)

    def set_selected_value(self, active_id: Union[int, str]):
        """Set selected enum member from enum value"""
        self.set_active_id(active_id)

    def set_change_callback(self, f: Callable):
        """Attach new function to call on change"""
        self.change_callback = f
        self.connect("changed", self.change_callback)
