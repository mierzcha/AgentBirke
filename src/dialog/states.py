from enum import Enum

class DialogState(Enum):
    """States of the user dialogue."""
    IDLE = "Idle"
    GREETING = "Greeting"
    DIALOGUE_ACTIVE = "Dialogue_active"
    GOODBYE = "Goodbye"