from collections import defaultdict
from enum import Enum

from models.cell_model import get_possible_values
from utils.Mocks import MockBoard
from utils.constants import BOARD_SIZE


class Technique(Enum):
    SCANNING = 0
    SINGLE_CANDIDATE = 1
    NAKED_PAIRS = 2
    HIDDEN_PAIRS = 3


class DifficultyRater:
    def __init__(self, board_controller):
        self.board_controller = board_controller

        self.board = MockBoard(self.board_controller)
        self.technique = []

        self.technique_log = defaultdict(int)
        self.techniques = [
            # self._scanning,
            self._single_candidate,
            self._naked_pairs,
            self._hidden_pairs,
            # Add more techniques here
        ]

    def solve(self):
        progress = True
        self._generate_notes()

        while progress and not self._is_solved():
            progress = False
            for technique in self.techniques:
                if technique():
                    progress = True  # Progress made, re-check all techniques
                    break
            # print(f'progress was {'' if progress else 'not '}made')

        # string = ''
        # for row in self.board.cells:
        #     for cell in row:
        #         string += str(cell.value) + ' '
        #     print(string)
        #     string = ''

        # for technique, count in self.technique_log.items():
        #     print(technique, count)

        # for x in range(BOARD_SIZE):
        #     for y in range(BOARD_SIZE):
        #         self.board_controller.cells[x][y].model.toggle_entry(self.board.cells[x][y].value)
        #         self.board_controller.cells[x][y].model.notify()

        # self.board_controller.model.notify()

        # print('solved: ', self._is_solved())
        return self._is_solved()

    def _is_solved(self):
        for row in self.board.cells:
            for cell in row:
                if cell.value is None:
                    return False
        return True

    def _scanning(self):
        progress = False
        for row in self.board.cells:
            for cell in row:
                if cell.value is None:
                    possible_values = self._get_possible_values(cell)
                    if len(possible_values) == 1:
                        cell.value = possible_values.pop()
                        progress = True
                        self.technique_log[Technique.SCANNING] += 1
        return progress

    def _generate_notes(self):
        """ Generate notes for all cells """
        for row in self.board.cells:
            for cell in row:
                if cell.value is None:
                    cell.notes = get_possible_values(cell)

    def _single_candidate(self):

        progress = False
        for row in self.board.cells:
            for cell in row:
                if cell.value is None and len(cell.notes) == 1:
                    cell.value = cell.notes.pop()
                    progress = True
                    for house_cell in cell.get_house():
                        if cell.value in house_cell.notes:
                            house_cell.notes.remove(cell.value)

                    self.technique_log[Technique.SINGLE_CANDIDATE] += 1
                    # self._generate_notes()  # Regenerate notes after each assignment
        return progress

    def _naked_pairs(self):
        pass

    def _hidden_pairs(self):
        pass


