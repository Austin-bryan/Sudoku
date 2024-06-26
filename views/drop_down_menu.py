from tkinter import *
from utils.constants import *
from views.action_button import ActionButton, BUTTON_DEFAULT_COLOR, BUTTON_HOVER_COLOR, DEFAULT_WIDTH

# Colors for different states
DROPDOWN_TEXT_COLOR = 'white'
DROPDOWN_ARROW_COLOR = '#555'
DROPDOWN_BUTTON_COLOR = '#444'
DROPDOWN_ARROW_SIZE = 6


class DropdownMenu(Canvas):
    """ Custom dropdown menu class, that has more consistent UI with the rest of the application. """
    def __init__(self, parent, options, width=DEFAULT_WIDTH, height=DEFAULT_WIDTH, **kwargs):
        """ Options is an array of tuples of the option text and option command. """
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=BUTTON_DEFAULT_COLOR, **kwargs)
        self.options = options
        self.width = width
        self.height = height
        self.is_open = False
        self.selected_option, _ = options[0]

        self.rect = self.create_rectangle(0, 0, width, height, fill=BUTTON_DEFAULT_COLOR, outline="")
        self.text = self.create_text(width / 2, height / 2, text="Select", fill=DROPDOWN_TEXT_COLOR, font=("Arial", 12))

        # Create the dropdown arrow
        self.arrow = self.create_polygon([
                width - 15, height / 2 + 5 * DROPDOWN_ARROW_SIZE / 6,  # Bottom point
                width - 15 + DROPDOWN_ARROW_SIZE, height / 2 - 4 * DROPDOWN_ARROW_SIZE / 5,  # Right point
                width - 15 - DROPDOWN_ARROW_SIZE, height / 2 - 4 * DROPDOWN_ARROW_SIZE / 5  # Left point
            ],
            fill=DROPDOWN_ARROW_COLOR
        )

        # Bind events
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

        # Bind the configure event of the root window to a callback function
        parent.bind("<Configure>", self.on_configure)

        # Bind the focus out event of the dropdown panel to hide it when focus is lost
        self.dropdown_panel.bind("<FocusOut>", self.close_menu)

    def create_option_buttons(self):
        """ Uses the options list of tuples to generate all action buttons. """
        for i, (option, command) in enumerate(self.options):
            # Appends a select_option statement to the command
            wrapped_command = self.wrap_command(command, option)
            button = ActionButton(self.dropdown_panel, option, width=self.width, height=self.height,
                                  bg=DROPDOWN_BUTTON_COLOR, command=wrapped_command)
            button.place(x=0, y=i * self.height)

    def wrap_command(self, command, option):
        """ Calls select option to show which option is selected. """
        return lambda event: (command(event), self.select_option(option))

    def toggle_menu(self, event=None):
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        """ Opens the dropdown menu. """
        self.is_open = True
        self.update_dropdown_position()
        self.dropdown_panel.deiconify()
        self.dropdown_panel.lift()
        self.dropdown_panel.focus_set()  # Ensure the dropdown panel gets focus

    def close_menu(self, event=None):
        self.is_open = False
        self.dropdown_panel.withdraw()

    def update_dropdown_position(self):
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.height
        self.dropdown_panel.geometry(f"{self.width}x{self.height * len(self.options)}+{x}+{y}")

    def on_configure(self, event):
        if self.is_open:
            self.close_menu()

    def select_option(self, option):
        """ Changes text of drop down menu and closes menu """
        self.selected_option = option
        self.itemconfig(self.text, text=option)
        self.close_menu()

    def on_enter(self, event):
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        self._set_color(BUTTON_DEFAULT_COLOR)

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)

