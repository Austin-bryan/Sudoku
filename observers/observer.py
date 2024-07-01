from abc import ABC, abstractmethod


class Observer(ABC):
    """ Base class for all observers. """

    @abstractmethod
    def update(self):
        """ Update the observer. """
        pass
