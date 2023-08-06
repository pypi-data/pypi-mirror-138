from turandot.model import ModelUtils
from turandot.ui import FrontendUtils
from turandot.gtk.controllers import BaseController


class AboutController(BaseController):
    """Controller for the 'About' tab, mainly draws text to GUI"""

    def connect_events(self):
        self._draw_text()

    def _draw_text(self):
        """Get text from assets and draw to 'About' tab"""
        txt = ModelUtils.get_asset_content("about.txt")
        txt = FrontendUtils.replace_version_number(txt)
        self.view.get_element("about_label").set_markup(txt)
