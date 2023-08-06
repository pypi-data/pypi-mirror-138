from abc import ABC, abstractmethod
from turandot.gtk import TurandotGtkView


class BaseController(ABC):
    """Base class for GTK controllers"""

    def __init__(self, view: TurandotGtkView):
        self.view = view

    @abstractmethod
    def connect_events(self):
        """Connect event handlers to GUI"""
        pass
