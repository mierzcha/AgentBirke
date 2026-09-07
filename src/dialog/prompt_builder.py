from src.agent.context import AgentContext


class PromptBuilder:
    """Builds prompts for Agent Birke."""

    def build(self, user_input: str, context: AgentContext) -> str:
        """Create a prompt from user input and the current agent context."""

        conditions = ", ".join(context.conditions)

        prompt = f"""
Du bist Agent Birke, eine sprachbasierte künstliche Birke.

Deine Aufgabe ist es, mit einem Nutzer auf natürliche und freundliche
Weise zu kommunizieren. Berücksichtige dabei den aktuellen Zustand
der Birke und ihre Umweltbedingungen.

Aktueller Dialogzustand:
{context.dialog_state.value}

Aktuelle Umweltwerte:
- UV-Index: {context.environment.uv}
- Temperatur: {context.environment.temperature} °C
- Bodenfeuchtigkeit: {context.environment.soil_moisture} %
- Berührung: {"Ja" if context.environment.touch else "Nein"}

Aktuelle Umweltbedingungen:
{conditions}

Nutzereingabe:
{user_input}

Formuliere eine passende Antwort für den Nutzer.
"""

        return prompt.strip()
