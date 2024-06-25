class UndoHistoryManager:
    def __init__(self):
        self.history = []
        self.current_index = -1

    def execute_command(self, command):
        command.execute()
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(command)
        self.current_index += 1

    def undo(self):
        print(f'undo {self.current_index}')
        if self.current_index >= 0:
            self.history[self.current_index].undo()
            self.current_index -= 1

    def redo(self):
        print(f'redo {self.current_index}')
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.history[self.current_index].redo()
