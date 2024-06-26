import os
from tkinter import *
from utils.constants import *
from views.action_button import ActionButton

# Colors for different states
BUTTON_DEFAULT_COLOR = '#333'
BUTTON_HOVER_COLOR = '#a91'
BUTTON_PRESS_COLOR = SELECTION_COLOR

DROPDOWN_BG_COLOR = '#666'
DROPDOWN_HOVER_COLOR = '#a91'
DROPDOWN_TEXT_COLOR = 'white'
DROPDOWN_ARROW_COLOR = '#444'

DEFAULT_FONT_SIZE = 9
DEFAULT_WIDTH = 60


class DropdownMenu(Canvas):
    def __init__(self, parent, options, width=DEFAULT_WIDTH, height=DEFAULT_WIDTH, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=DROPDOWN_BG_COLOR, **kwargs)
        self.options = options
        self.width = width
        self.height = height
        self.is_open = False
        self.selected_option = None

        self.rect = self.create_rectangle(0, 0, width, height, fill=DROPDOWN_BG_COLOR, outline="")
        self.text = self.create_text(width / 2, height / 2, text="Select", fill=DROPDOWN_TEXT_COLOR, font=("Arial", 12))
        self.arrow = self.create_polygon(
            [width - 15, height / 2 + 3, width - 10, height / 2 - 3, width - 20, height / 2 - 3],
            fill=DROPDOWN_ARROW_COLOR
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.toggle_menu)

        # Create a Toplevel window for the dropdown panel
        self.dropdown_panel = Toplevel(parent)
        self.dropdown_panel.withdraw()  # Hide initially
        self.dropdown_panel.overrideredirect(True)  # Remove window decorations
        self.dropdown_panel.configure(bg=DROPDOWN_BG_COLOR)

        self.create_option_buttons()

    def create_option_buttons(self):
        for i, (option, command) in enumerate(self.options):
            wrapped_command = self.wrap_command(command)
            button = ActionButton(self.dropdown_panel, option, width=self.width, height=self.height, command=wrapped_command)
            button.place(x=0, y=i * self.height)
            print(f"Created button for {option} at {i * self.height}")

    def wrap_command(self, command):
        return lambda event: (command(event), self.close_menu())

    def toggle_menu(self, event=None):
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        self.is_open = True
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.height
        self.dropdown_panel.geometry(f"{self.width}x{self.height * len(self.options)}+{x}+{y}")
        self.dropdown_panel.deiconify()
        self.dropdown_panel.lift()

    def close_menu(self):
        self.is_open = False
        self.dropdown_panel.withdraw()

    def select_option(self, option):
        self.selected_option = option
        self.itemconfig(self.text, text=option)
        print(f"Selected: {option}")
        self.close_menu()

    def on_enter(self, event):
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        self._set_color(DROPDOWN_BG_COLOR)

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)
