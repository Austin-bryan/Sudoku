import unittest
from unittest.mock import Mock
from models.subject import Subject  # Replace with the actual import path of your Subject class


class TestSubject(unittest.TestCase):
    def setUp(self):
        """ Set up the test environment by initializing the Subject and mock observers. """
        self.subject = Subject()
        self.observer1 = Mock()
        self.observer2 = Mock()

    def test_attach_observer(self):
        """ Test that an observer is correctly attached to the subject. """
        self.subject.attach(self.observer1)
        self.assertIn(self.observer1, self.subject._observers)

    def test_detach_observer(self):
        """ Test that an attached observer is correctly detached from the subject. """
        self.subject.attach(self.observer1)
        self.subject.detach(self.observer1)
        self.assertNotIn(self.observer1, self.subject._observers)

    def test_notify_observers(self):
        """ Test that all attached observers receive a notify call when the subject's notify method is called. """
        self.subject.attach(self.observer1)
        self.subject.attach(self.observer2)

        self.subject.notify()

        self.observer1.update.assert_called_once()
        self.observer2.update.assert_called_once()

    def test_notify_with_no_observers(self):
        """ Ensure no exceptions are raised when notifying with no observers attached. """
        self.subject.notify()

    def test_detach_observer_not_attached(self):
        """ Ensure that attempting to detach an observer that is not attached does not raise an exception. """
        self.subject.detach(self.observer1)


if __name__ == '__main__':
    unittest.main()
