from enum import Enum
from md_citeproc import NotationStyle, OutputStyle
from turandot.model import ModelUtils
from turandot.ui import FrontendUtils
from turandot.gtk.controllers import BaseController
from turandot.gtk.presentations import SettingsControlBase, TitleControl, TextControl, SwitchControl, SpinControl, TextEnumControl


class SettingsController(BaseController):

    @staticmethod
    def _control_factory() -> list[SettingsControlBase]:
        """Build list of widgets to control application preferences"""
        return [
            TitleControl("General"),
            SwitchControl("Remember file input path:", ["general", "file_select_persistence"]),
            SwitchControl("Save intermediate files:", ["general", "save_intermediate"]),
            TitleControl("Zotero"),
            SpinControl("BetterBibtex Port:", ['api', 'zotero', 'port']),
            TitleControl("Table of contents"),
            TextControl("TOC Marker:", ['processors', 'convert_to_html', 'markdown_ext', 'toc', 'marker']),
            TitleControl("Citeproc"),
            TextControl("Locale:", ['processors', 'convert_to_html', 'markdown_ext', 'md_citeproc', 'locale']),
            TextEnumControl("Notation Style:",
                            ['processors', 'convert_to_html', 'markdown_ext', 'md_citeproc', 'notation'],
                            model=NotationStyle, text_based=True),
            TextEnumControl("Rendering Style:",
                            ['processors', 'convert_to_html', 'markdown_ext', 'md_citeproc', 'output'],
                            model=OutputStyle, text_based=True),
            TextControl("Footnotes Marker:",
                        ['processors', 'convert_to_html', 'markdown_ext', 'md_citeproc', 'footnotes_token']),
            TextControl("Bibliography Marker:",
                        ['processors', 'convert_to_html', 'markdown_ext', 'md_citeproc', 'bibliography_token']),
            TitleControl("Optional processors"),
            SwitchControl("Unified math markers:", ['opt_processors', 'unified_math_block_marker', 'enable']),
            SwitchControl("TOC pagination containers:", ['opt_processors', 'toc_pagination_containers', 'enable']),

        ]

    def _controls_to_view(self):
        """Build widget list and add to GUI"""
        clist = SettingsController._control_factory()
        for n, i in enumerate(clist, start=3):
            i.add_to_view(self.view, n)

    @staticmethod
    def _open_config_dir(*args):
        """Open config dir"""
        FrontendUtils.fm_open_path(ModelUtils.get_config_dir())

    def connect_events(self):
        self.view.get_element("config_file_location_entry").set_text(str(ModelUtils.get_config_file()))
        self.view.get_element("config_dir_open_button").connect("clicked", SettingsController._open_config_dir)
        self._controls_to_view()
