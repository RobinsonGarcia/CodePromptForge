
from codepromptforge.main import CodePromptForge
from codepromptforge.prompt import react_template
from langgraph.prebuilt import create_react_agent
from .assistant_registry import AssistantRegistry

# Define the assistant's prompt
prompt = react_template + "You are forbidden to call tools beyond the list provided."

# Define the tools
forge = CodePromptForge()
tools = forge.get_tools()

# Define the assistant builder function
def build_react_assistant(llm):
    return create_react_agent(llm, tools=tools, prompt=prompt)

# Register the assistant
AssistantRegistry.register_assistant("react_assistant", build_react_assistant)