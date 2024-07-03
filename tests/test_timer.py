import unittest
from unittest.mock import MagicMock
import tkinter as tk
from utils.timer import Timer


class TestTimer(unittest.TestCase):
    """ Unit tests for the Timer class. """

    def setUp(self):
        """ Set up the test environment by creating a Timer instance. """
        self.root = tk.Tk()
        self.root.withdraw()
        self.frame = tk.Frame(self.root)
        self.timer = Timer(self.frame)
        self.timer.pack()
        self.timer.update()
        self.timer.update_idletasks()

    def tearDown(self):
        """ Tear down the test environment by destroying the Timer instance. """
        self.timer.destroy()
        self.frame.destroy()
        self.root.destroy()

    def test_start_timer(self):
        """ Test that the timer starts correctly. """
        self.timer.running = False
        self.timer.start()
        self.assertTrue(self.timer.running)
        self.assertEqual(str(self.timer.timer_label.cget('foreground')), 'green')
        self.assertEqual(self.timer.time, 0)
        self.assertEqual(self.timer.timer_label.cget('text'), '00:00:00')

    def test_start_timer_when_running(self):
        """ Test that starting the timer when it's already running does nothing. """
        self.timer.running = True
        self.timer.start()
        self.assertTrue(self.timer.running)  # Should still be running
        self.assertNotEqual(self.timer.timer_label.cget('foreground'), 'green')

    def test_stop_timer(self):
        """ Test that the timer stops correctly. """
        self.timer.running = True
        self.timer.stop()
        self.assertFalse(self.timer.running)
        self.assertEqual(str(self.timer.timer_label.cget('foreground')), 'red')

    def test_stop_timer_when_not_running(self):
        """ Test that stopping the timer when it's not running does nothing. """
        self.timer.running = False
        self.timer.stop()
        self.assertFalse(self.timer.running)  # Should still not be running
        self.assertNotEqual(self.timer.timer_label.cget('foreground'), 'red')

    def test_reset_timer(self):
        """ Test that the timer resets correctly. """
        self.timer.time = 100
        self.timer.reset()
        self.assertEqual(self.timer.time, 0)
        self.assertEqual(self.timer.timer_label.cget('text'), '00:00:00')

    def test_update_timer(self):
        """ Test that the timer display updates correctly based on the elapsed time. """
        self.timer.time = 3661  # 1 hour, 1 minute, and 1 second
        self.timer.update_timer()
        self.assertEqual(self.timer.timer_label.cget('text'), '01:01:01')

    def test_update(self):
        """ Test that the timer increments correctly when running. """
        self.timer.running = True
        self.timer._update = MagicMock(wraps=self.timer._update)
        self.timer._update()
        self.assertEqual(self.timer.time, 1)
        self.timer._update.assert_called()

    def test_update_when_not_running(self):
        """ Test that the timer does not increment when not running. """
        self.timer.running = False
        self.timer._update()
        self.assertEqual(self.timer.time, 0)  # Should not update time


if __name__ == '__main__':
    unittest.main()
