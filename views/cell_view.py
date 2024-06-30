from abc import ABC, abstractmethod
from tkinter import Canvas
from typing import cast, Optional

from house_manager import HouseManager
from observers.observer import Observer
from utils.constants import SELECTION_COLOR, BACKGROUND_COLOR, SUBGRID_SIZE
from models.cell_value_type import CellValueType

# Cell colors
CELL_DEFAULT_COLOR = '#333'
CELL_HIGHLIGHT_COLOR = '#4a4a4a'
CELL_MATCHING_COLOR = '#299'
CELL_CONFLICT_COLOR = '#A33'
CELL_SELECTION_COLOR = SELECTION_COLOR


class CellView(Canvas, Observer):
    _WIDTH = 70

    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.model = model
        self.actual_width = CellView._WIDTH
        self.actual_height = CellView._WIDTH
        self.config(width=CellView._WIDTH, height=CellView._WIDTH, bg=CELL_DEFAULT_COLOR)
        self._draw_thick_borders()
        self.on_press_event = None
        self.is_highlighted = False
        self.house_manager = None
        self.model.attach(self)
        self._state_context = StateContext(self)

        self.value_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        self.note_labels = [self.create_text((col + 1) * self.actual_width / 4,
                                             (row + 1) * self.actual_height / 4, fill='white', font=("Arial", 9))
                            for row in range(SUBGRID_SIZE) for col in range(SUBGRID_SIZE)]

    def _draw_thick_borders(self):
        """
        Draws the thicker lines on cells that are on the edge of a subgrid.

        Because this changes the length of the cell, the cell has to be made even long to accommodate them.
        """
        thickness_width = 8
        should_draw_vertical_line = self.model.y % SUBGRID_SIZE == 0 and self.model.y != 0
        should_draw_horizontal_line = self.model.x % SUBGRID_SIZE == 0 and self.model.x != 0
        line_length = CellView._WIDTH * 1.4

        if should_draw_vertical_line:
            self.create_line(0, 0, 0, line_length if should_draw_horizontal_line
                                                  else CellView._WIDTH, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = CellView._WIDTH + thickness_width
            self.config(width=CellView._WIDTH + thickness_width / 2)

        if should_draw_horizontal_line:
            self.create_line(0, 0, line_length if should_draw_vertical_line
                                               else CellView._WIDTH, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = CellView._WIDTH + thickness_width
            self.config(height=CellView._WIDTH + thickness_width / 2)

    def update_color(self, color):
        self.config(bg=color)

    def update_value_label(self):
        self.itemconfig(self.value_label,
                        text=self.model.value if self.model.value is not None else '',
                        fill='white' if self.model.value_type == CellValueType.ENTRY else 'black')

    def update_labels(self):
        """
        Ensures that labels are set properly depending on the value type of the cell.
        Makes sures notes and entries cannot be visible at the same time, and the color of the value is also correct.
        """
        match self.model.value_type:
            case CellValueType.ENTRY:
                self.update_value_label()
                self.clear_notes()
            case CellValueType.NOTES:
                self.clear_entry()

                for i, label in enumerate(self.note_labels):
                    self.itemconfig(label, text=i + 1 if self.model.notes[i] else '')
            case CellValueType.GIVEN:
                self.update_value_label()
            case _:
                self.clear_entry()
                self.clear_notes()

    def clear_entry(self):
        """ Removes the entry label. """
        self.itemconfig(self.value_label, text='')

    def clear_notes(self):
        """ Removes all notes. """
        for label in self.note_labels:
            self.itemconfig(label, text='')

    def update(self):
        if self.model.in_conflict:
            self.enter_conflict()
        else:
            self._state_context.exit_conflict()
        self.update_labels()

    @property
    def x(self):
        return self.model.x

    @x.setter
    def x(self, value):
        self.model.x = value

    @property
    def y(self):
        return self.model.y

    @y.setter
    def y(self, value):
        self.model.y = value

    def get_house(self):
        return self.house_manager.get_house()

    def get_row(self):
        return self.house_manager.get_row()

    def get_column(self):
        return self.house_manager.get_column()

    def get_subgrid(self):
        return self.house_manager.get_subgrid()

    def enter_highlighted(self):
        self._state_context.enter_highlighted()

    def enter_selected(self):
        self._state_context.enter_selected()

    def enter_matching(self):
        self._state_context.enter_matching()

    def enter_conflict(self):
        self._state_context.enter_conflict()

    def reset_state(self):
        """ Resets the state to default or conflicted, depending if a conflict exists. """
        self._state_context.reset_state()

    def return_to_default(self):
        self._state_context.return_to_default()


class CellViewState(ABC):
    priority = 0

    @abstractmethod
    def enter(self, cell_view):
        pass

    def get_rollback_state(self) -> Optional["CellViewState"]:
        return None


class DefaultCellViewState(CellViewState):
    """ The default state with the original color. """
    priority = 1

    def enter(self, cell_view):
        cell_view.update_color(CELL_DEFAULT_COLOR)


class HighlightedCellViewState(CellViewState):
    """ Highlights all cells in the same house in the selected cell, unless its in conflict. """
    priority = 2

    def enter(self, cell_view):
        cell_view.update_color(CELL_HIGHLIGHT_COLOR)


class SelectedCellViewState(CellViewState):
    """ Shows which cell is selected, unless its in conflict. """
    priority = 3

    def enter(self, cell_view):
        cell_view.update_color(CELL_SELECTION_COLOR)


class MatchingCellViewState(CellViewState):
    """ Shows all cells with the same value, unless they are in conflict. """
    priority = 4

    def enter(self, cell_view):
        cell_view.update_color(CELL_MATCHING_COLOR)


class ConflictCellViewState(CellViewState):
    """ When two cells in the same house have the same number and the cell turns to conflict color. """
    priority = 5

    def __init__(self, previous_state):
        self._rollback_state = previous_state

    def enter(self, cell_view):
        cell_view.update_color(CELL_CONFLICT_COLOR)

    def get_rollback_state(self):
        return self._rollback_state


class StateContext:
    def __init__(self, cell_view):
        self.cell_view = cell_view
        self.state = DefaultCellViewState()

    def set_state(self, new_state):
        """ Does a priority check before setting the state to the new state. """
        if new_state.priority > self.state.priority:
            self._rollback_state(new_state)

    def _rollback_state(self, new_state):
        """
        Allows the changing of a state to a state with a lower priority.
        This can occur when resetting to default from any state,
        or default, highlighted, or selected from conflict.
        """
        self.state = new_state
        self.state.enter(self.cell_view)

    def return_to_default(self):
        self._rollback_state(DefaultCellViewState())

    def enter_default(self):
        self.set_state(DefaultCellViewState())

    def enter_highlighted(self):
        self._try_set_state(HighlightedCellViewState())

    def enter_selected(self):
        self._try_set_state(SelectedCellViewState())

    def enter_matching(self):
        self.set_state(MatchingCellViewState())

    def enter_conflict(self):
        self.set_state(ConflictCellViewState(self.state))

    def exit_conflict(self):
        """
        When exiting, checks if the state as a fallback state.
        This can occur when in the conflict state, with fallbacks being either highlighted or selected.
        This returns to those states in the event the user fixes the conflict.
        """
        if self.state.get_rollback_state():
            self._rollback_state(self.state.get_rollback_state())

    def reset_state(self):
        """ Resets the state to default or highlighted depending on the current conditions. """
        if not self.cell_view.model.in_conflict:
            self._rollback_state(DefaultCellViewState())

    def _try_set_state(self, new_state):
        """ Tries to set the state, if in conflict state, simply updates the conflict fallback state. """
        if not self.cell_view.model.in_conflict:
            self.set_state(new_state)
        else:
            self.state = ConflictCellViewState(new_state)
