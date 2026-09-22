from src.agent.context import AgentContext
from src.dialog.states import DialogState
from src.dialog.prompt_builder import PromptBuilder
from src.simulation.events import EnvironmentState


def main():

    environment = EnvironmentState(
        uv=5,
        temperature=30,
        soil_moisture=30,
    )

    context = AgentContext(
        dialog_state=DialogState.DIALOGUE_ACTIVE,
        environment=environment,
        conditions=["Thirsty", "Too_Hot"],
    )

    builder = PromptBuilder()

    prompt = builder.build(
        user_input="Wie geht es dir?",
        context=context,
        dialog_history=[],
    )

    print("Generierter Prompt:")
    print("--------------------------------")
    print(prompt)
    print("--------------------------------")

    assert "Es ist gerade zu heiß für dich." in prompt
    assert "Du bist gerade durstig. Du möchtest gegossen werden." in prompt
    assert "30 °C" in prompt
    assert "30 %" in prompt
    assert "Wie geht es dir?" in prompt

    print("PromptBuilder funktioniert.")


if __name__ == "__main__":
    main()