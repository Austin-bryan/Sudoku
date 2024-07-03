from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from observers.observer import Observer  # pragma: no cover


class Subject:
    """ Subjects are capable of being observed by observers. """
    def __init__(self):
        self._observers = []

    def attach(self, observer: 'Observer'):
        """
        Add an observer to the list of observers to notify.
        :param observer: Observer to add
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer'):
        """
        Remove an observer from the list of observers to notify.
        :param observer: Observer to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """ Notify all observers that a change has occurred. """
        for observer in self._observers:
            observer.update()
