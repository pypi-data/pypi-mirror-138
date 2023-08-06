import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from enum import Enum


class TypeFilterEnum(Enum):
    """Enumeration of different file type filters"""
    ALL = "all"
    MARKDOWN = "markdown"
    CSL = "csl"
    JSON = "json"
    HTML = "html"
    TMPL = "tmpl"


class FileTypeFilterFactory:
    """File ending based type filters for file picker dialogs"""

    @staticmethod
    def apply(t: TypeFilterEnum, dialog: Gtk.FileChooserDialog):
        """Apply filter to dialog"""
        lookup = {
            TypeFilterEnum.ALL: FileTypeFilterFactory._make_all(),
            TypeFilterEnum.MARKDOWN: FileTypeFilterFactory._make_markdown(),
            TypeFilterEnum.CSL: FileTypeFilterFactory._make_csl(),
            TypeFilterEnum.JSON: FileTypeFilterFactory._make_json(),
            TypeFilterEnum.HTML: FileTypeFilterFactory._make_html(),
            TypeFilterEnum.TMPL: FileTypeFilterFactory._make_tmpl()
        }
        if t != TypeFilterEnum.ALL:
            dialog.add_filter(lookup.get(t))
        dialog.add_filter(lookup.get(TypeFilterEnum.ALL))

    @staticmethod
    def _make_all() -> Gtk.FileFilter:
        """Create all files filter"""
        tf = Gtk.FileFilter()
        tf.set_name("All files")
        tf.add_pattern("*")
        return tf

    @staticmethod
    def _make_markdown() -> Gtk.FileFilter:
        """Create markdown file filters"""
        tf = Gtk.FileFilter()
        tf.set_name("Markdown files")
        tf.add_pattern("*.markdown")
        tf.add_pattern("*.mdown")
        tf.add_pattern("*.mkdn")
        tf.add_pattern("*.mkd")
        tf.add_pattern("*.md")
        tf.add_pattern("*.txt")
        return tf

    @staticmethod
    def _make_csl() -> Gtk.FileFilter:
        """Create csl file filter"""
        tf = Gtk.FileFilter()
        tf.set_name("CSL files")
        tf.add_pattern("*.csl")
        tf.add_pattern("*.xml")
        return tf

    @staticmethod
    def _make_json() -> Gtk.FileFilter:
        """Create json file filter"""
        tf = Gtk.FileFilter()
        tf.set_name("JSON files")
        tf.add_pattern("*.csljson")
        tf.add_pattern("*.json")
        return tf

    @staticmethod
    def _make_html() -> Gtk.FileFilter:
        """Create html file filter"""
        tf = Gtk.FileFilter()
        tf.set_name("HTML files")
        tf.add_pattern("*.html")
        tf.add_pattern("*.htm")
        tf.add_pattern("*.xml")
        return tf

    @staticmethod
    def _make_tmpl() -> Gtk.FileFilter:
        """Create template file filter"""
        tf = Gtk.FileFilter()
        tf.set_name("Template files")
        tf.add_pattern("*.tmpl")
        tf.add_pattern("*.zip")
        tf.add_pattern("*.yaml")
        return tf
