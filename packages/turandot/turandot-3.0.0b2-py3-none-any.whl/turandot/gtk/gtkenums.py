from enum import Enum


class DropdownPreSelections(Enum):
    """Enum values to preselect certain values on ComboBox updates"""
    FIRST_ELEMENT = -2
    SAME_ELEMENT = -1
