from pathlib import Path
from tkinter import filedialog

from turandot.model import FileSelectPersistApi

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from turandot.ttk.view import TurandotTtkView


class DbFedFilePicker:
    """Util class to draw a file picker dialog"""

    @staticmethod
    def draw(view: "TurandotTtkView", return_id: str, filefilter: list[tuple[str]], title="Choose a file"):
        """Draw file picker dialog"""
        initialdir = FileSelectPersistApi.get(return_id)
        chosen = filedialog.askopenfilename(filetypes=filefilter, title=title, initialdir=initialdir)
        if chosen not in [(), ""]:
            FileSelectPersistApi.set(return_id, Path(chosen).parent)
            view.widgets[return_id].set(chosen)
