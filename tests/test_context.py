from src.agent.context import AgentContext
from src.dialog.states import DialogState
from src.simulation.events import EnvironmentState


def main():

    environment = EnvironmentState(
        uv=5,
        temperature=30,
        soil_moisture=30,
        touch=True,
    )

    context = AgentContext(
        dialog_state=DialogState.DIALOGUE_ACTIVE,
        environment=environment,
        conditions=["Thirsty", "Too_Hot"],
    )

    print("Agent Context:")
    print(context)

    assert context.dialog_state == DialogState.DIALOGUE_ACTIVE
    assert context.environment.temperature == 30
    assert "Thirsty" in context.conditions
    assert "Too_Hot" in context.conditions

    print("\nAgentContext funktioniert.")


if __name__ == "__main__":
    main()
