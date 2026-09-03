from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState


def mainTest():
    state_machine = DialogStateMachine()

    # Initial state
    assert state_machine.state == DialogState.IDLE
    print("Initialzustand: Idle")

    # Idle → Greeting
    state = state_machine.handle_event("touch")
    assert state == DialogState.GREETING
    print("Berührung: Idle → Greeting")

    # Greeting → Dialogue_active
    state = state_machine.handle_event("speech")
    assert state == DialogState.DIALOGUE_ACTIVE
    print("Spracheingabe: Greeting → Dialogue_active")

    # Dialogue_active → Goodbye
    state = state_machine.handle_event("goodbye")
    assert state == DialogState.GOODBYE
    print("Verabschiedung: Dialogue_active → Goodbye")

    # Goodbye → Idle
    state = state_machine.handle_event("anything")
    assert state == DialogState.IDLE
    print("Goodbye → Idle")

    print("\nAlle Tests erfolgreich.")

def test_invalid_transition():
    state_machine = DialogStateMachine()

    # Speech should not start the dialogue directly from Idle
    state_machine.handle_event("speech")

    assert state_machine.state == DialogState.IDLE

    print("Ungültiger Übergang wird ignoriert")


if __name__ == "__main__":
    mainTest()
    test_invalid_transition()
