from dataclasses import dataclass
from src.dialog.states import DialogState
from src.simulation.events import EnvironmentState

@dataclass
class AgentContext:
    """Contains the current context of Agent Birke."""
    dialog_state: DialogState
    environment: EnvironmentState
    conditions: list[str]
    engagement : int
    
def create_context(dialog_state: DialogState, environment: EnvironmentState, conditions: list[str], engagement : int) -> AgentContext:
    """Create the current context of Agent Birke."""
    return AgentContext(dialog_state=dialog_state, environment=environment, conditions=conditions, engagement=engagement)