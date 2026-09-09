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

        if context.dialog_state.value == "Greeting":

            task_description = """
Der Nutzer hat die Birke gerade berührt und ein neues Gespräch
beginnt.

Begrüße den Nutzer freundlich.

Die Begrüßung soll nur aus einer kurzen Begrüßung bestehen.
Beginne keine weiteren Gesprächsthemen und beantworte noch keine
inhaltliche Frage.

Verwende den bisherigen Gesprächsverlauf nicht für die Begrüßung.
"""

        elif context.dialog_state.value == "Dialogue_active":

            task_description = """
Das Gespräch mit dem Nutzer ist bereits aktiv.

Beantworte die aktuelle Nutzereingabe direkt und passend.

Begrüße den Nutzer NICHT erneut.
Beginne deine Antwort NICHT mit "Hallo" oder einer anderen
Begrüßung.

Berücksichtige den bisherigen Gesprächsverlauf. Informationen,
die der Nutzer im bisherigen Gespräch genannt hat, dürfen in
späteren Antworten verwendet werden.
"""

        elif context.dialog_state.value == "Goodbye":

            task_description = """
Das Gespräch mit dem Nutzer wird beendet.

Verabschiede dich freundlich und kurz vom Nutzer.

Beginne kein neues Gesprächsthema und stelle keine weitere Frage.
"""

        else:

            task_description = """
Es findet aktuell kein aktives Gespräch statt.

Antworte nur, wenn eine Antwort in diesem Zustand erforderlich ist.
"""

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

Du führst natürliche und kurze Gespräche mit einem Nutzer.
Antworte freundlich und verständlich.

{task_description}

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

{task_description}

Formuliere jetzt nur die Antwort von Agent Birke.
"""

        return prompt.strip()