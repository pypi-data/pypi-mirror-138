import os
from turandot import SysInfo, OpSys
from turandot.model import ModelUtils
from turandot.gtk.controllers import BaseController, DialogController, DataDropdownController, SettingsController, ConverterTabController, AboutController, ExportController
from turandot.ui import ExceptionCatcher, TurandotFrontend
from turandot.gtk import GtkCatcher, TurandotGtkView


class TurandotGtk(TurandotFrontend):
    """Launch GTK GUI for Turandot"""

    def __init__(self):
        # Create view
        self.view = TurandotGtkView()
        # Create concrete exception catcher and pass the view to it
        concrete_catcher = GtkCatcher(self.view)
        self.catcher = ExceptionCatcher()
        self.catcher.set_strategy(concrete_catcher)
        self.controllers: list[BaseController] = [
            DialogController(self.view),
            DataDropdownController(self.view),
            SettingsController(self.view),
            ConverterTabController(self.view),
            AboutController(self.view),
            ExportController(self.view)
        ]
        for i in self.controllers:
            i.connect_events()

    def run(self):
        """Run application"""
        self.view.show_main()


if __name__ == "__main__":
    TurandotGtk().run()
