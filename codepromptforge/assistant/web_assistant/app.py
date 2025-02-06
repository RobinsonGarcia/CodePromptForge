from flask import Flask, render_template, request, jsonify, session
from codepromptforge.assistant import AssistantRegistry
from langchain_ollama import ChatOllama
import ollama
import re
import argparse
import uuid
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__)) 
TEMPLATES_PATH = os.path.join(APP_DIR, "templates")
STATIC_PATH = os.path.join(APP_DIR, "static")

print("🔥 Debug Info 🔥")
print(f"📂 Current Working Directory: {os.getcwd()}")
print(f"📁 Expected Templates Path: {TEMPLATES_PATH}")
print(f"📄 index.html Exists: {os.path.exists(os.path.join(TEMPLATES_PATH, 'index.html'))}")

# Initialize Flask with explicit template directory
app = Flask(__name__, template_folder=TEMPLATES_PATH, static_folder=STATIC_PATH)
app.secret_key = "supersecretkey"  # Required for session tracking

def get_available_models():
    """Returns a list of available models in Ollama."""
    try:
        return [m["name"] for m in ollama.list()["models"]]
    except Exception:
        return []

def format_response(response):
    """Formats assistant response to preserve code formatting."""
    response = re.sub(r"```python\n(.*?)\n```", r'<pre><code class="language-python">\1</code></pre>', response, flags=re.DOTALL)
    response = re.sub(r"```markdown\n(.*?)\n```", r'<pre><code class="language-markdown">\1</code></pre>', response, flags=re.DOTALL)
    return response.replace("\n", "<br>")

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Start web assistant")
parser.add_argument("--model", required=True, help="Ollama model name")
parser.add_argument("--base-dir", required=True, help="Base directory for file operations")
args = parser.parse_args()

# Convert base_dir to an absolute path
BASE_DIR = os.path.abspath(args.base_dir)  # ✅ Ensure correct path

# Change working directory to base_dir
os.chdir(BASE_DIR)  # ✅ Ensure app has access to base_dir files

print(f"🔹 Server running with base directory: {BASE_DIR}")

# Initialize LLM
llm = ChatOllama(model=args.model)

# Retrieve assistant with `base_dir`
assistant_name = "react_assistant"
agent = AssistantRegistry.get_assistant(assistant_name, llm, BASE_DIR)  # ✅ Pass absolute base_dir

@app.route("/")
def index():
    """Render the chat UI."""
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())  # ✅ Generate unique thread_id

    return render_template(
        "index.html",
        models=get_available_models(),
        selected_model=args.model,
        base_dir=BASE_DIR,  # ✅ Pass absolute base_dir
        thread_id=session["thread_id"]
    )

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user input with thread_id for session tracking."""
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Empty input!"}), 400

    thread_id = session.get("thread_id", str(uuid.uuid4()))  # ✅ Ensure thread_id persists

    inputs = {"messages": [("user", user_input)]}
    config = {"configurable": {"thread_id": thread_id}}  # ✅ Include memory tracking

    response = agent.invoke(inputs, config=config)

    assistant_response = response["messages"][-1].content if "messages" in response else response.content
    return jsonify({"message": format_response(assistant_response)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)