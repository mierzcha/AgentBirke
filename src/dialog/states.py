from enum import Enum


class DialogState(Enum):
    """States of the dialogue between Agent Birke and the user."""

    IDLE = "Idle"
    GREETING = "Greeting"
    DIALOGUE_ACTIVE = "Dialogue_active"
    GOODBYE = "Goodbye"
