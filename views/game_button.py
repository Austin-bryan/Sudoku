import os
from tkinter import *
from abc import ABC
from utils.constants import *
from PIL import Image, ImageTk

# Colors for different states
BUTTON_DEFAULT_COLOR = '#333'
BUTTON_HOVER_COLOR = '#a91'
BUTTON_PRESS_COLOR = SELECTION_COLOR

DEFAULT_FONT_SIZE = 9


class GameButton(Canvas):
    def __init__(self, parent, label, font_size=DEFAULT_FONT_SIZE, width=60, command=None, image_path=None, **kwargs):
        self.WIDTH = width
        self.label = label

        super().__init__(parent, width=self.WIDTH, height=self.WIDTH, highlightthickness=0, **kwargs)

        # Draw the button
        self.rect = self.create_rectangle(0, 0, self.WIDTH, self.WIDTH, fill=BUTTON_DEFAULT_COLOR, outline="")
        self.text = self.create_text(self.WIDTH / 2,
                                     self.WIDTH / 2 if image_path is None else 5 * self.WIDTH / 6,
                                     text=self.label, fill="white", font=("Arial", font_size))

        self.image = None
        if image_path:
            full_image_path = os.path.join('images', image_path)
            image = Image.open(full_image_path)
            image_scale = 0.6
            image = image.resize((int(self.WIDTH * image_scale), int(self.WIDTH * image_scale)))
            self.image = ImageTk.PhotoImage(image)
            self.image_item = self.create_image(self.WIDTH / 2, 2 * self.WIDTH / 5, image=self.image)

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        if command:
            self.bind("<ButtonPress-1>", lambda event: command())
        else:
            self.bind("<ButtonPress-1>", self.on_press)

    def on_enter(self, event):
        """ Applies hover effect. """
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        """ Returns to default on mouse leave. """
        self._set_color(BUTTON_DEFAULT_COLOR)

    def on_press(self, event):
        pass

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)
