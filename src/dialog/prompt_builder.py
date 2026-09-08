from src.agent.context import AgentContext


class PromptBuilder:
    """Builds prompts for Agent Birke."""

    def build(
        self,
        user_input: str,
        context: AgentContext,
        dialog_history: list[dict[str, str]],
    ) -> str:
        """Create a prompt from user input, context and dialog history."""

        if context.dialog_state.value == "Dialogue_active":
            dialog_description = (
                "Der Nutzer befindet sich aktuell in einem aktiven "
                "Gespräch mit der Birke."
            )
        elif context.dialog_state.value == "Greeting":
            dialog_description = (
                "Der Nutzer befindet sich gerade in der "
                "Begrüßungsphase."
            )
        elif context.dialog_state.value == "Goodbye":
            dialog_description = (
                "Das Gespräch mit dem Nutzer wird gerade beendet."
            )
        else:
            dialog_description = (
                "Aktuell findet kein aktives Gespräch statt."
            )

        if "Happy" in context.conditions:
            condition_description = (
                "Die Umweltbedingungen sind aktuell unauffällig."
            )
        else:
            condition_description = (
                "Aktuell liegen folgende Umweltbedingungen vor: "
                + ", ".join(context.conditions)
                + "."
            )

        touch_description = (
            "Der Berührungssensor ist aktiviert."
            if context.environment.touch
            else "Der Berührungssensor ist nicht aktiviert."
        )

        conversation = ""

        for message in dialog_history:
            conversation += (
                f"{message['speaker']}: {message['text']}\n"
            )

        if not conversation:
            conversation = "Noch kein bisheriger Gesprächsverlauf."

        prompt = f"""
Du bist Agent Birke, eine freundliche künstliche Birke.

Du führst einen kurzen, natürlichen Dialog mit einem Nutzer.
Antworte freundlich und verständlich.

{dialog_description}

Aktuelle Umweltwerte:
- UV-Index: {context.environment.uv}
- Temperatur: {context.environment.temperature} °C
- Bodenfeuchtigkeit: {context.environment.soil_moisture} %

{condition_description}

{touch_description}

Bisheriger Gesprächsverlauf:
{conversation}

Aktuelle Nutzereingabe:
{user_input}

Beziehe den bisherigen Gesprächsverlauf in deine Antwort ein.
Wenn der Nutzer beispielsweise seinen Namen genannt hat, kannst du
diesen Namen im weiteren Gespräch verwenden.

Antworte passend auf die aktuelle Nutzereingabe.
"""

        return prompt.strip()