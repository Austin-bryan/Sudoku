from undo_history.command import Command


class UndoHistoryManager:
    """
    Manages a stack of commands.
    Using an index, it undoes the current command and moves down the stack for undos,
    and moves back up the stack for redos.
    """
    def __init__(self):
        self.history = []
        self.current_index = -1

    def execute_command(self, command: Command):
        """
        Executes the given command and sets the current index to be the new command.
        If the user has undone changes, then executed a new command,
        the commands above the current index get cleared, preventing them from being redone.
        :param command: The new command to be executed.
        """
        command.execute()
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(command)
        self.current_index += 1

    def undo(self):
        """ Undo the current command and move the index down one spot in the undo history. """
        if self.current_index >= 0:
            self.history[self.current_index].undo()
            self.current_index -= 1

    def redo(self):
        """ Redo the current command and move the index up one spot in the undo history. """
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.history[self.current_index].redo()
