from enum import Enum, auto


class OpSys(Enum):
    """Enum representing the running OS"""
    LINUX = 0
    WINDOWS = 1
    MACOS = 2


class Architecture(Enum):
    """Enum representing the running CPU architecture"""
    AMD64 = 0


class ReferenceSource(Enum):
    """Enum representing the source of bibliographic data to be used"""
    NOTHING = 0
    NOSOURCE = 1
    ZOTERO = 2
    JSON = 3


class TemplatingEngine(Enum):
    """Enum representing the templating engine to be used for the conversion"""
    NOTHING = 0
    JINJA2 = 1
    MAKO = 2


class ConversionAlgorithm(Enum):
    """Enum representing the conversion algorithm to be used for the conversion"""
    WEASYPRINT = 0


class OptionalStage(Enum):
    """Enum representing the stage to attach a optional converter to a mandatory one"""
    PRE = 0
    POST = 1


class MessageType(Enum):
    """Enum representing the type of a message in the queue from backend to frontend"""
    STARTED = auto()
    COPY = auto()
    EXCEPTION = auto()
    WARNING = auto()
    NEXT_STEP = auto()
    SUCCESS = auto()
    DIED = auto()
    CANCELED = auto()
