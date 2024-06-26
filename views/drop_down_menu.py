from tkinter import *
from utils.constants import *
from views.action_button import ActionButton, BUTTON_DEFAULT_COLOR, BUTTON_HOVER_COLOR, DEFAULT_WIDTH

# Colors for different states
DROPDOWN_TEXT_COLOR = 'white'
DROPDOWN_ARROW_COLOR = '#555'
DROPDOWN_BUTTON_COLOR = '#444'
DROPDOWN_ARROW_SIZE = 6


class DropdownMenu(Canvas):
    def __init__(self, parent, options, width=DEFAULT_WIDTH, height=DEFAULT_WIDTH, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=BUTTON_DEFAULT_COLOR, **kwargs)
        self.options = options
        self.width = width
        self.height = height
        self.is_open = False

        self.rect = self.create_rectangle(0, 0, width, height, fill=BUTTON_DEFAULT_COLOR, outline="")
        self.text = self.create_text(width / 2, height / 2, text="Select", fill=DROPDOWN_TEXT_COLOR, font=("Arial", 12))
        # Create the triangle using the size parameter
        self.arrow = self.create_polygon(
            [
                width - 15, height / 2 + 5 * DROPDOWN_ARROW_SIZE / 6,  # Bottom point
                width - 15 + DROPDOWN_ARROW_SIZE, height / 2 - 4 * DROPDOWN_ARROW_SIZE / 5,  # Right point
                width - 15 - DROPDOWN_ARROW_SIZE, height / 2 - 4 * DROPDOWN_ARROW_SIZE / 5  # Left point
            ],
            fill=DROPDOWN_ARROW_COLOR
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.toggle_menu)

        # Create a Toplevel window for the dropdown panel
        self.dropdown_panel = Toplevel(parent)
        self.dropdown_panel.withdraw()  # Hide initially
        self.dropdown_panel.overrideredirect(True)  # Remove window decorations
        self.dropdown_panel.configure(bg=BUTTON_DEFAULT_COLOR)

        self.create_option_buttons()
        self.select_option(self.options[0][0])  # Set the first option as the default selection

    def create_option_buttons(self):
        for i, (option, command) in enumerate(self.options):
            wrapped_command = self.wrap_command(command, option)
            button = ActionButton(self.dropdown_panel, option, width=self.width, height=self.height,
                                  bg=DROPDOWN_BUTTON_COLOR, command=wrapped_command)
            button.place(x=0, y=i * self.height)

    def wrap_command(self, command, option):
        return lambda event: (command(event), self.select_option(option))

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
        self.close_menu()

    def on_enter(self, event):
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        self._set_color(BUTTON_DEFAULT_COLOR)

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)
