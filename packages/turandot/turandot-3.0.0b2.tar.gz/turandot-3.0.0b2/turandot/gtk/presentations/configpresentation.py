from abc import ABC, abstractmethod
from enum import Enum, EnumMeta
from typing import Union
from gi.repository import Gtk
from typing import TYPE_CHECKING
from turandot.model import ConfigModel
from turandot.gtk.presentations import EnumDropdown
if TYPE_CHECKING:
    from turandot.gtk import TurandotGtkView


class SettingsViewBase(ABC):
    """Base class for read-only settings widgets"""

    def __init__(self, label: str):
        self.label = self._create_label(label)

    @abstractmethod
    def _create_label(self, label: str) -> Gtk.Label:
        """Create text label for the configuration control widget"""
        pass

    @abstractmethod
    def add_to_view(self, view: "TurandotGtkView", row: int):
        """Add widget elements to GUI"""
        pass


class SettingsControlBase(SettingsViewBase, ABC):
    """Base class for savable widgets"""

    def __init__(self, label, config_key: Union[str, list]):
        super().__init__(label)
        self.config_key = config_key

    def _create_label(self, label: str) -> Gtk.Label:
        lbl = Gtk.Label(label)
        lbl.set_halign(Gtk.Align.START)
        lbl.show()
        return lbl

    @abstractmethod
    def _attach_callback(self):
        """Attach callback method to specific change event"""
        pass

    @abstractmethod
    def _callback(self):
        """Method to call on change"""
        pass


class TitleControl(SettingsViewBase):
    """Title label, read only"""

    def __init__(self, title: str, vmargins: tuple = (20, 10)):
        super().__init__(title)
        self.label.set_margin_top(vmargins[0])
        self.label.set_margin_bottom(vmargins[1])

    def _create_label(self, label: str) -> Gtk.Label:
        lbl = Gtk.Label()
        lbl.set_markup("<b>" + label + "</b>")
        lbl.set_hexpand(True)
        lbl.set_halign(Gtk.Align.START)
        lbl.show()
        return lbl

    def add_to_view(self, view: "TurandotGtkView", row: int):
        view.get_element("dynamic_settings_grid").attach(self.label, 0, row, 2, 1)


class TextControl(SettingsControlBase):
    """Control widget to set strings in config file"""

    def __init__(self, label: str, config_key: Union[str, list]):
        super().__init__(label, config_key)
        self.entry = Gtk.Entry()
        self.entry.set_text(ConfigModel().get_key(self.config_key, default=""))
        self.entry.set_hexpand(True)
        self.entry.show()
        self._attach_callback()

    def _callback(self, *args):
        ConfigModel().set_key(self.config_key, self.entry.get_text())

    def _attach_callback(self):
        self.entry.connect("changed", self._callback)

    def add_to_view(self, view: "TurandotGtkView", row: int):
        view.get_element("dynamic_settings_grid").attach(self.label, 0, row, 1, 1)
        view.get_element("dynamic_settings_grid").attach(self.entry, 1, row, 1, 1)


class SwitchControl(SettingsControlBase):
    """Control widget to set bools in config file"""

    def __init__(self, label: str, config_key: Union[str, list]):
        super().__init__(label, config_key)
        self.switch = Gtk.Switch()
        self.switch.set_active(ConfigModel().get_key(self.config_key, default=False))
        self.switch.set_hexpand(True)
        self.switch.set_halign(Gtk.Align.END)
        self.switch.show()
        self._attach_callback()

    def _attach_callback(self):
        self.switch.connect("notify::active", self._callback)

    def _callback(self, *args):
        ConfigModel().set_key(self.config_key, self.switch.get_active())

    def add_to_view(self, view: "TurandotGtkView", row: int):
        view.get_element("dynamic_settings_grid").attach(self.label, 0, row, 1, 1)
        view.get_element("dynamic_settings_grid").attach(self.switch, 1, row, 1, 1)


class SpinControl(SettingsControlBase):
    """Control widget to set ints in config file"""

    def __init__(
            self,
            label: str,
            config_key: Union[str, list],
            lower: float = 1024,
            upper: float = 65553,
            step: float = 1,
            decimal: int = 0
    ):
        super().__init__(label, config_key)
        self.decimal = decimal
        adjustment = Gtk.Adjustment(lower=lower, upper=upper, step_increment=step)
        self.spinner = Gtk.SpinButton()
        self.spinner.set_adjustment(adjustment)
        self.spinner.set_numeric(True)
        self.spinner.set_digits(decimal)
        self.spinner.set_update_policy(Gtk.SpinButtonUpdatePolicy.ALWAYS)
        self.spinner.set_value(ConfigModel().get_key(self.config_key, default=False))
        self.spinner.show()
        self._attach_callback()

    def _attach_callback(self):
        self.spinner.connect("value-changed", self._callback)
        self.spinner.connect("scroll-event", self._empty_callback)

    def _callback(self, *args):
        if self.decimal <= 0:
            val = self.spinner.get_value_as_int()
        else:
            val = self.spinner.get_value()
        ConfigModel().set_key(self.config_key, val)

    @staticmethod
    def _empty_callback(*args):
        """empty callback to prevent Spinners from changing on scrolling"""
        return True

    def add_to_view(self, view: "TurandotGtkView", row: int):
        view.get_element("dynamic_settings_grid").attach(self.label, 0, row, 1, 1)
        view.get_element("dynamic_settings_grid").attach(self.spinner, 1, row, 1, 1)


class TextEnumControl(SettingsControlBase):
    """Control widget to set enum values in config file"""

    def __init__(self, label: str, config_key: Union[list, str], model: EnumMeta, text_based: bool = False):
        super().__init__(label, config_key)
        self.combo = EnumDropdown(model, text_based=text_based)
        initval = ConfigModel().get_key(self.config_key, default="")
        self.combo.set_selected_value(initval)
        self.combo.show()
        self._attach_callback()

    def _attach_callback(self):
        self.combo.connect("changed", self._callback)

    def _callback(self, *args):
        val = self.combo.get_selected_value()
        ConfigModel().set_key(self.config_key, val.value)

    def add_to_view(self, view: "TurandotGtkView", row: int):
        view.get_element("dynamic_settings_grid").attach(self.label, 0, row, 1, 1)
        view.get_element("dynamic_settings_grid").attach(self.combo, 1, row, 1, 1)
