from abc import ABC, abstractmethod


class Command(ABC):
    """ Base class for command pattern. """
    @abstractmethod
    def execute(self):
        """ Executes the command. """
        pass

    @abstractmethod
    def undo(self):
        """ Restores the state to the state before the command was executed. """
        pass

    @abstractmethod
    def redo(self):
        """ This is seperated from execute. """
        pass
