import sys
import subprocess
import uuid
from .common import AssistantRegistry
from langchain_ollama import ChatOllama
import ollama

#############################
# Assistant Module Utilities#
#############################
class ModelNotFoundError(Exception):
    """Custom exception to handle missing Ollama models."""
    pass

def check_if_model_exists(model_name):
    available_models = [m["name"] for m in ollama.list()["models"]]
    if model_name in available_models:
        return True
    else:
        error_message = (
            f"❌ Model '{model_name}' not found in Ollama.\n"
            f"📥 To download it, run:\n\n"
            f"   ollama pull {model_name}\n"
            f"\n🔹 Available models: {', '.join(available_models) if available_models else 'None'}"
        )
        raise ModelNotFoundError(error_message)

#########################
# Assistant CLI Handlers#
#########################
def start_assistant(model_name, base_dir, temperature, num_ctx):
    try:
        check_if_model_exists(model_name)
        print("✅ Model is available.")
    except ModelNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    llm = ChatOllama(model=model_name, temperature=temperature, num_ctx=num_ctx)
    assistant_name = "react_assistant"
    if assistant_name not in AssistantRegistry.list_assistants():
        print(f"Error: Assistant '{assistant_name}' is not available.", file=sys.stderr)
        sys.exit(1)
    agent = AssistantRegistry.get_assistant(assistant_name, llm, base_dir)
    print(f"🔹 Running '{assistant_name}' assistant with Ollama model: {model_name}")
    print("💬 Type your messages below. Type 'exit' to quit.\n")
    thread_id = str(uuid.uuid4())
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🔻 Exiting assistant.")
            break
        try:
            inputs = {"messages": [("user", user_input)]}
            config = {"configurable": {"thread_id": thread_id}}
            response = agent.invoke(inputs, config=config)
            if isinstance(response, dict) and "messages" in response:
                print(f"Assistant: {response['messages'][-1].content}")
            else:
                print(f"Assistant: {response.content}")
        except Exception as e:
            print(e, file=sys.stderr)

def start_server(model_name, base_dir):
    print(f"🚀 Starting web server with model '{model_name}' and base directory '{base_dir}'...")
    subprocess.run(["python", "codepromptforge/assistant/web_assistant/app.py", "--model", model_name, "--base-dir", base_dir])

###############################
# Assistant Commands Registration
###############################
def register_commands(subparsers):
    # Register CLI assistant command
    parser_assistant = subparsers.add_parser("cli_assistant", help="Run the advanced assistant CLI")
    parser_assistant.add_argument("--model", required=True, help="Ollama model to use (e.g., llama3.3, qwen2.5:14b)")
    parser_assistant.add_argument("--base-dir", required=True, help="Base directory for assistant operations")
    parser_assistant.add_argument("--temperature", type=float, default=0.0, help="Temperature setting for the model")
    parser_assistant.add_argument("--num_ctx", type=int, default=80000, help="Context length for the model")
    parser_assistant.set_defaults(func=handle_assistant)

    # Register web assistant command
    parser_web = subparsers.add_parser("web_assistant", help="Start the advanced web assistant server")
    parser_web.add_argument("--model", required=True, help="Ollama model to use")
    parser_web.add_argument("--base-dir", required=True, help="Base directory for assistant operations")
    parser_web.set_defaults(func=handle_web)

def handle_assistant(args):
    start_assistant(args.model, args.base_dir, args.temperature, args.num_ctx)

def handle_web(args):
    start_server(args.model, args.base_dir)