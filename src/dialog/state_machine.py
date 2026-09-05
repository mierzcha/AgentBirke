from .states import DialogState


class DialogStateMachine:
    """Controls transitions between dialogue states."""

    def __init__(self):
        self.state = DialogState.IDLE
        self.history = [DialogState.IDLE]

    def handle_event(self, event: str) -> DialogState:
        """Process an event and return the new dialogue state."""

        old_state = self.state

        if self.state == DialogState.IDLE:
            if event == "touch":
                self.state = DialogState.GREETING

        elif self.state == DialogState.GREETING:
            if event == "speech":
                self.state = DialogState.DIALOGUE_ACTIVE

        elif self.state == DialogState.DIALOGUE_ACTIVE:
            if event == "goodbye":
                self.state = DialogState.GOODBYE

        elif self.state == DialogState.GOODBYE:
            self.state = DialogState.IDLE

        # Only record actual state changes
        if self.state != old_state:
            self.history.append(self.state)

        return self.state