from dataclasses import dataclass
from datetime import datetime


from .states import DialogState


@dataclass
class StateTransition:
    """Represents a transition between two dialogue states."""

    from_state: DialogState
    event: str
    to_state: DialogState


class DialogStateMachine:
    """Controls transitions between dialogue states."""

    GOODBYE_DURATION = 2.0

    def __init__(self):
        self.state = DialogState.IDLE
        self.history = []
        self.goodbye_started_at = None

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
            if event == "release":
                self.state = DialogState.GOODBYE
                self.goodbye_started_at = datetime.now()

        if self.state != old_state:
            self.history.append(
                StateTransition(
                    from_state=old_state,
                    event=event,
                    to_state=self.state,
                )
            )

        return self.state

    def update(self) -> DialogState:
        """Perform automatic state transitions."""

        if self.state == DialogState.GOODBYE:

            elapsed_time = (
                datetime.now() - self.goodbye_started_at
            ).total_seconds()

            if elapsed_time >= self.GOODBYE_DURATION:

                old_state = self.state

                self.state = DialogState.IDLE
                self.goodbye_started_at = None

                self.history.append(
                    StateTransition(
                        from_state=old_state,
                        event="automatic",
                        to_state=self.state,
                    )
                )

        return self.state