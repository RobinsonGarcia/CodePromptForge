import argparse
import json
import sys
import subprocess
from codepromptforge.main import (
    CodePromptForge, 
    InvalidBaseDirectoryError, 
    NoFilesFoundError, 
    OutputFileAlreadyExistsError
)

from codepromptforge.assistant import AssistantRegistry
from langchain_ollama import ChatOllama
import ollama
import uuid


class ModelNotFoundError(Exception):
    """Custom exception to handle missing Ollama models."""
    pass


def check_if_model_exists(model_name):
    """
    Checks if the given model is available in Ollama.
    
    Args:
        model_name (str): The name of the model to check.

    Returns:
        bool: True if the model exists, otherwise raises an error.
    
    Raises:
        ModelNotFoundError: If the model is not available in Ollama.
    """
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


def start_assistant(model_name, base_dir, **kwargs):
    """
    Instantiates an Ollama LLM model and runs an interactive assistant session.
    
    Args:
        model_name (str): The name of the Ollama model (e.g., "qwen2.5:14b", "llama3.3").
        **kwargs: Optional parameters for configuring the LLM model.
    """
    # Initialize Ollama model with optional parameters
    try:
        check_if_model_exists(model_name)  # Replace with your desired model
        print("✅ Model is available.")
    except ModelNotFoundError as e:
        print(e)
        sys.exit(1)
    llm = ChatOllama(model=model_name, **kwargs)

    # Retrieve the assistant (defaults to "react_assistant")
    assistant_name = "react_assistant"
    if assistant_name not in AssistantRegistry.list_assistants():
        print(f"Error: Assistant '{assistant_name}' is not available.", file=sys.stderr)
        sys.exit(1)

    agent = AssistantRegistry.get_assistant(assistant_name, llm, base_dir)

    # Interactive CLI session
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


            # Print the response
            if isinstance(response, dict) and "messages" in response:
                print(f"Assistant: {response['messages'][-1].content}")
            else:
                print(f"Assistant: {response.content}")
                
        except Exception as e:
            print(e)


def start_server(model_name, base_dir):
    """
    Launches the web server with specified model and base directory.
    
    Args:
        model_name (str): The Ollama model name.
        base_dir (str): The base directory for assistant operations.
    """
    print(f"🚀 Starting web server with model '{model_name}' and base directory '{base_dir}'...")
    subprocess.run(["python", "codepromptforge/web_assistant/app.py", "--model", model_name, "--base-dir", base_dir])


def main():
    parser = argparse.ArgumentParser(description="Code management CLI.")
    parser.add_argument(
        "command",
        choices=["tree", "file", "files", "files_recursive", "write", "combine", "clean_result", "cli_assistant", "web_assistant"],
        help="Command to execute"
    )
    parser.add_argument("--folder", help="Folder path")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--content", help="Content for writing")
    parser.add_argument("--base-dir", help="Base directory")
    parser.add_argument("--extensions", nargs="*", default=[], help="File extensions for combining")
    parser.add_argument("--output-file", help="Output file for combination")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing output file")
    parser.add_argument("--exclude", nargs="*", default=[], help="List of files to exclude from concatenation")
    parser.add_argument("--exclude-clean", nargs="*", default=[], help="Files to remove from .result folder")
    
    # Arguments for Assistant
    parser.add_argument("--model", help="Ollama model to use (e.g., llama3.3, qwen2.5:14b)")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature setting for the model")
    parser.add_argument("--num_ctx", type=int, default=80000, help="Context length for the model")

    args = parser.parse_args()

    # Handle assistant command
    if args.command == "cli_assistant":
        if not args.model:
            print("Error: --model argument is required for 'assistant' command.", file=sys.stderr)
            sys.exit(1)
        if not args.base_dir:
            print("Error: --base_dir argument is required for 'assistant' command.", file=sys.stderr)
            sys.exit(1)
        # Collect optional LLM parameters
        llm_params = {
            "temperature": args.temperature,
            "num_ctx": args.num_ctx,
        }

        start_assistant(args.model, args.base_dir, **llm_params)
        return  # Exit after running assistant mode
    
    if args.command == "web_assistant":
        if not args.model or not args.base_dir:
            print("Error: --model and --base-dir are required for 'server' command.", file=sys.stderr)
            sys.exit(1)

        start_server(args.model, args.base_dir)
        return

    # Regular CLI Commands
    forge = CodePromptForge(
        base_dir=args.base_dir,
        output_file=args.output_file,
        force=args.force,
        excluded=args.exclude
    )

    try:
        if args.command == "tree":
            if not args.folder:
                print("Error: The --folder argument is required for 'tree' command.", file=sys.stderr)
                sys.exit(1)
            print(forge.get_directory_tree(args.folder))

        elif args.command == "file":
            if not args.file:
                print("Error: The --file argument is required for 'file' command.", file=sys.stderr)
                sys.exit(1)
            print(forge.get_file_content(args.file))

        elif args.command == "files":
            if not args.folder:
                raise ValueError("The --folder argument is required for 'files' command.")
            print(json.dumps(forge.get_files_in_folder(args.folder), indent=2))

        elif args.command == "files_recursive":
            if not args.folder:
                raise ValueError("The --folder argument is required for 'files_recursive' command.")
            print(json.dumps(forge.get_files_recursively(args.folder), indent=2))

        elif args.command == "write":
            if not args.file or not args.content:
                raise ValueError("Both --file and --content arguments are required for 'write' command.")
            print(forge.write_file(args.file, args.content))

        elif args.command == "combine":
            if not args.extensions or not args.output_file:
                raise ValueError("--extensions and --output-file are required for 'combine'.")
            forge.forge_prompt(args.extensions)

        elif args.command == "clean_result":
            if not args.exclude_clean:
                raise ValueError("--exclude-clean argument is required for 'clean_result'.")
            forge.clean_result_folder(args.exclude_clean)

    except (InvalidBaseDirectoryError, NoFilesFoundError, OutputFileAlreadyExistsError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()