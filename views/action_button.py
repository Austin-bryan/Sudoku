import os
import tkinter as tk
from tkinter import *
from utils.constants import *
from PIL import Image, ImageTk
from typing import Callable

# Colors for different states
BUTTON_DEFAULT_COLOR = '#333'
BUTTON_HOVER_COLOR = '#a91'
BUTTON_PRESS_COLOR = SELECTION_COLOR

DEFAULT_FONT_SIZE = 9
DEFAULT_WIDTH = 60


class ActionButton(Canvas):
    """ Custom button used for app. """
    def __init__(self, parent: tk.Frame, label: str, font_size: int = DEFAULT_FONT_SIZE,
                 width: int = DEFAULT_WIDTH, height: int = DEFAULT_WIDTH,
                 command: Callable[[Event], None] = None, image_path: str = None,
                 bg: str = BUTTON_DEFAULT_COLOR, **kwargs):
        self.label = label
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.bg = bg

        # Draw the button
        self.rect = self.create_rectangle(0, 0, width, height, fill=bg, outline="")
        self.text = self.create_text(width / 2,
                                     height / 2 if image_path is None else 5 * height / 6,
                                     text=self.label, fill="white", font=("Arial", font_size))

        self.photo_image = None
        if image_path:
            # These need to be cached or else they don't show
            self.photo_image, self.image_item = self.create_icon(width, height, image_path)
        self.command = command

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)

    def create_icon(self, width: int, height: int, image_path: str):
        """
        Creates icon based on image path.
        :return: The photo image and image item.
        """
        full_image_path = os.path.join('images', image_path)
        image = Image.open(full_image_path)
        image_scale = 0.5
        image = image.resize((int(width * image_scale), int(height * image_scale)))
        photo_image = ImageTk.PhotoImage(image)
        image_item = self.create_image(width / 2, 2 * height / 5, image=photo_image)

        return photo_image, image_item

    def on_enter(self, event: Event):
        """ Applies hover effect. """
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event: Event):
        """ Returns to default on mouse leave. """
        self._set_color(self.bg)

    def on_press(self, event: Event):
        """ Executes the command. """
        self.command(event)

    def _set_color(self, color: str):
        """ Sets color of button. """
        self.itemconfig(self.rect, fill=color)
