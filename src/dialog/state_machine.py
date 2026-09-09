from dataclasses import dataclass

from .states import DialogState


@dataclass
class StateTransition:
    """Represents a transition between two dialogue states."""

    from_state: DialogState
    event: str
    to_state: DialogState


class DialogStateMachine:
    """Controls the dialogue states and their transitions."""

    def __init__(self):
        self.state = DialogState.IDLE
        self.history = []

    def handle_event(self, event: str) -> DialogState:
        """Process an event and return the new dialogue state."""

        old_state = self.state

        if self.state == DialogState.IDLE:

            if event == "touch":
                self.state = DialogState.GREETING

        elif self.state == DialogState.GREETING:

            if event == "speech":
                self.state = DialogState.DIALOGUE_ACTIVE

            elif event == "release":
                self.state = DialogState.GOODBYE

        elif self.state == DialogState.DIALOGUE_ACTIVE:

            if event == "speech":
                self.state = DialogState.DIALOGUE_ACTIVE

            elif event == "release":
                self.state = DialogState.GOODBYE

        elif self.state == DialogState.GOODBYE:

            if event == "goodbye_finished":
                self.state = DialogState.IDLE

        if self.state != old_state:

            self.history.append(
                StateTransition(
                    from_state=old_state,
                    event=event,
                    to_state=self.state,
                )
            )

        return self.state