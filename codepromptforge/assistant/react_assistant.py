
from codepromptforge.main import CodePromptForge
from codepromptforge.prompt import react_template
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from .assistant_registry import AssistantRegistry

# Define the assistant's prompt
prompt = react_template + "You are forbidden to call tools beyond the list provided."
memory = MemorySaver()


# Define the assistant builder function
def build_react_assistant(llm, base_dir):
    # Define the tools
    forge = CodePromptForge(base_dir=base_dir)
    tools = forge.get_tools()
    return create_react_agent(llm, tools=tools, prompt=prompt, checkpointer=memory)

# Register the assistant
AssistantRegistry.register_assistant("react_assistant", build_react_assistant)