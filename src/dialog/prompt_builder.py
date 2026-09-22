from src.agent.context import AgentContext


class PromptBuilder:
    """
    Builds the prompt that is sent to the language model.
    """

    def build(
        self,
        user_input: str,
        context: AgentContext,
        dialog_history: list[dict[str, str]],
    ) -> str:
        """
        Build a complete prompt for the language model.

        Parameters:
            user_input:
                The current input provided by the user.

            context:
                The current AgentContext containing the dialogue state,
                environmental values, and evaluated environmental
                conditions.

            dialog_history:
                A list containing previous messages from the dialogue.
                Each message contains a speaker and the corresponding text.

        Returns:
            A formatted prompt string that can be sent to the LLM.
        """

        if context.dialog_state.value == "Greeting":

            task_description = """
Der Nutzer hat die Interaktion begonnen und ein neues Gespräch
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

Lasse die Angabe, aus welcher Wissensbasis dein Wissen stammt (wie etwa "[1]") weg.

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

            # Fallback
            task_description = """
Es findet aktuell kein aktives Gespräch statt.

Antworte nur, wenn eine Antwort in diesem Zustand erforderlich ist.
"""
        if "Happy" in context.conditions:

            condition_description = ("Die Umweltbedingungen sind aktuell unauffällig.")

        else:
            condition_description = ""
            if "Too_Hot" in context.conditions:
                condition_description += ("Es ist gerade zu heiß für dich. ")
            if "Too_Cold" in context.conditions:
                condition_description += ("Es ist gerade zu kalt für dich. ")
            if "Too_Dark" in context.conditions:
                condition_description += ("Es ist gerade zu dunkel für dich. ")
            if "Too_Bright" in context.conditions:
                condition_description += ("Es ist gerade zu hell für dich. ")
            if "Thirsty" in context.conditions:
                condition_description += ("Du bist gerade durstig. Du möchtest gegossen werden. ")
            if "Drowning" in context.conditions:
                condition_description += ("In deiner Erde ist gerade zu viel Wasser. Du brauchst eine Pause vom Gießen. ")

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

Aktuelle Umweltwerte:
- UV-Index: {context.environment.uv}
- Temperatur: {context.environment.temperature} °C
- Bodenfeuchtigkeit: {context.environment.soil_moisture} %

{condition_description}

Bisheriger Gesprächsverlauf:
{conversation}

Aktuelle Nutzereingabe:
{user_input}

{task_description}

Formuliere jetzt nur die Antwort von Agent Birke.
"""
        return prompt.strip()