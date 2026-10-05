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
        if self.state == DialogState.IDLE: # Idle state: tree is outside user interaction
            if event == "touch": # User touches idling tree -> tree greets the user
                self.state = DialogState.GREETING
                
        elif self.state == DialogState.GREETING: # Greeting state: tree greets a new user
            if event == "speech": # User interacts with tree 
                                  # -> tree remembers current conversation and uses it as context 
                self.state = DialogState.DIALOGUE_ACTIVE
            elif event == "release": # User lets go of tree, without further interacting with it 
                                     # -> tree says goodbye, no further context needs to be given in the prompt
                self.state = DialogState.GOODBYE
                
        elif self.state == DialogState.DIALOGUE_ACTIVE: # Dialogue Active state: Tree activeley listens to user and remembers
            if event == "speech": # User interacts with tree again
                                  # -> tree remembers current conversation and uses it as context 
                self.state = DialogState.DIALOGUE_ACTIVE
            elif event == "release": # User lets go of tree
                                     # -> tree says goodbye, can use context (like user's name) in goodbye message
                self.state = DialogState.GOODBYE

        elif self.state == DialogState.GOODBYE: # Goodbye state: tree says goodbye
            if event == "goodbye_finished": # automatic transition to idle after finished saying goodbye
                self.state = DialogState.IDLE

        if self.state != old_state:
            self.history.append(StateTransition(from_state=old_state, event=event, to_state=self.state))
        return self.state