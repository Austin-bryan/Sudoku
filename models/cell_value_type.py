from enum import Enum


class CellValueType(Enum):
    """ CellModels can be in the following states: """
    BLANK = 0  # No value or notes, can be written with anything
    GIVEN = 1  # An assigned clue, cannot be changed by the user
    ENTRY = 2  # User has entered what they think is the correct value into this cell
    NOTES = 3  # Has at least one active note. Notes can be cached for later if the user overrides it with an entry.
