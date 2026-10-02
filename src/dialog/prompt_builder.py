import json
from pathlib import Path
from src.agent.context import AgentContext

CONFIG_PATH = Path("config/prompt.json")
RULES_PATH = Path("config/rules.json")

class PromptBuilder:
    """Builds the prompt that is sent to the language model."""
    def __init__(self, prompt_config_path: Path = CONFIG_PATH, rules_config_path: Path = RULES_PATH):
        """Load prompt and condition configuration files."""
        self.prompts = self._load_config(prompt_config_path)
        self.rules = self._load_config(rules_config_path)

    def _load_config(self, config_path: Path) -> dict:
        """Load a JSON configuration file."""
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _build_condition_description(self, conditions: list[str]) -> str:
        """Build a description from the currently active conditions."""
        configured_conditions = self.rules["conditions"]
        descriptions = []
        for condition_label in conditions:
            for condition in configured_conditions.values():
                if condition["label"] == condition_label:
                    descriptions.append(condition["description"])
                    break

        return " ".join(descriptions)
        
    def _build_engagement_description(self, engagement: int) -> str:
        """Build a description from the current engagement value."""
        engagement_config = (self.prompts["internal_conditions"]["engagement"])
        for value_range in engagement_config ["ranges"]:
            if (value_range["min"] <= engagement<= value_range["max"]):
                return value_range["description"]

        return ""

    def _build_conversation(self,dialog_history: list[dict[str, str]]) -> str:
        """Build the conversation history from the dialogue messages."""
        if not dialog_history:
            return self.prompts["history_empty"]

        messages = []
        for message in dialog_history:
            messages.append(self.prompts["history_message"]
                .format(speaker=message["speaker"], text=message["text"]))
        return "\n".join(messages)

    def _get_task_description(self,dialog_state: str,) -> str:
        """Get the task description for the current dialogue state."""
        tasks = self.prompts["tasks"]
        return tasks.get(dialog_state,tasks["fallback"])

    def build(self,user_input: str,context: AgentContext,dialog_history: list[dict[str, str]]) -> str:
        """Build a complete prompt for the language model."""
        condition_description = self._build_condition_description(context.conditions)
        engagement_description= self._build_engagement_description(context.engagement)
        conversation = self._build_conversation(dialog_history)
        task_description = self._get_task_description(context.dialog_state.value)
        environment_template = self.prompts["environment_template"].format(context=context)
        input_label = self.prompts["input_label"].format(user_input=user_input)
        prompt = self.prompts["layout"].format(
            role=self.prompts["role"],
            environment_template=environment_template,
            condition_description=condition_description,
            engagement_description=engagement_description,
            conversation=conversation,
            input_label=input_label,
            task_description=task_description,
            output_instruction=self.prompts["output_instruction"],
        )
        return prompt.strip()