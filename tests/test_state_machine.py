from src.dialog.state_machine import DialogStateMachine
from src.dialog.states import DialogState


def main():
    state_machine = DialogStateMachine()

    assert state_machine.state == DialogState.IDLE
    print("Initialzustand: Idle")

    # Ungültiger Übergang
    state_machine.handle_event("speech")
    assert state_machine.state == DialogState.IDLE
    print("Ungültiger Übergang: Idle + speech bleibt Idle")

    # Idle → Greeting
    state_machine.handle_event("touch")
    assert state_machine.state == DialogState.GREETING
    print("Berührung: Idle → Greeting")

    # Greeting → Dialogue_active
    state_machine.handle_event("speech")
    assert state_machine.state == DialogState.DIALOGUE_ACTIVE
    print("Spracheingabe: Greeting → Dialogue_active")

    # Dialogue_active → Goodbye
    state_machine.handle_event("release")
    assert state_machine.state == DialogState.GOODBYE
    print("Loslassen: Dialogue_active → Goodbye")

    print("\nAlle Tests erfolgreich.")


if __name__ == "__main__":
    main()