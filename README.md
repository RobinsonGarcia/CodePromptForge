# **CodePromptForge ToolKit for Agent Development**

## **Overview**
The **CodePromptForge ToolKit** provides a set of **LangChain-compatible tools** for developing **AI agents** that can **read, analyze, modify, and write code**. These tools enable agents to explore a codebase, extract insights, generate new content, and modify files dynamically.

## **Features**
- **File and Directory Inspection**: Retrieve file contents, list directory structures, and analyze project organization.
- **Automated Code Processing**: Identify and manipulate specific code files based on extensions.
- **Code Modification**: Write and update files programmatically.
- **Cleanup and Maintenance**: Remove unnecessary files from results folders.
- **Seamless Integration**: Designed to work with **LangChain's** agent framework.

---

## **Available Tools**
### 🔍 **1. get_directory_tree**
> **Retrieve the structure of a directory**  
Returns a list of all files in a specified directory, ignoring files in `.gitignore` or explicitly excluded.

#### **Usage**
```python
tool = GetDirectoryTreeTool()
tool.run(folder_path="src")
```
#### **Response**
```json
["src/main.py", "src/utils/helpers.py", "src/config/settings.json"]
```

---

### 📄 **2. get_file_content**
> **Read the content of a specific file**  
Retrieves the contents of a file for analysis or processing.

#### **Usage**
```python
tool = GetFileContentTool()
tool.run(file_path="src/main.py")
```
#### **Response**
```json
"def main():\n    print('Hello, world!')"
```

---

### 📂 **3. get_files_in_folder**
> **List all files in a specific folder with their contents**  
Provides a dictionary where keys are file names and values are their contents.

#### **Usage**
```python
tool = GetFilesInFolderTool()
tool.run(folder_path="src")
```
#### **Response**
```json
{
    "main.py": "def main():\n    print('Hello, world!')",
    "config.json": "{'debug': true, 'version': '1.0'}"
}
```

---

### 📁 **4. get_files_recursively**
> **Retrieve all files in a folder and its subdirectories**  
Useful for analyzing an entire project structure.

#### **Usage**
```python
tool = GetFilesRecursivelyTool()
tool.run(folder_path="src")
```
#### **Response**
```json
{
    "src/main.py": "def main():\n    print('Hello, world!')",
    "src/utils/helpers.py": "def helper():\n    return 'Helper function'"
}
```

---

### 🔎 **5. find_files**
> **Find all files matching specific extensions in the base directory**  
Helpful for searching for specific types of files, such as Python scripts or Markdown documentation.

#### **Usage**
```python
tool = FindFilesTool()
tool.run(extensions=["py", "md"])
```
#### **Response**
```json
["src/main.py", "docs/readme.md"]
```

---

### ✍️ **6. write_file**
> **Write or modify a file**  
Creates or modifies a file inside the `.result` folder.

#### **Usage**
```python
tool = WriteFileTool()
tool.run(file_path="output.txt", content="New content for the file")
```
#### **Response**
```json
"File written successfully: .result/output.txt"
```

---

### 🧹 **7. clean_result_folder**
> **Remove unnecessary files from the `.result` folder**  
Ensures that old files don’t clutter the workspace.

#### **Usage**
```python
tool = CleanResultFolderTool()
tool.run(excluded_files=["output.txt"])
```
#### **Response**
```json
"Cleaned .result folder. Removed files: ['output.txt']"
```

---

### 🛠 **8. forge_prompt**
> **Merge multiple files into a single prompt**  
Key feature for creating **context-rich** inputs for LLMs.

#### **Usage**
```python
tool = ForgePromptTool()
tool.run(extensions=["py", "md"])
```
#### **Response**
```json
"Merged files: ['src/main.py', 'docs/readme.md']"
```

---

### 🚀 **9. run**
> **Runs the forge process on specified file extensions**  
Automates the process of finding, merging, and generating code prompts.

#### **Usage**
```python
tool = RunTool()
tool.run(extensions=["py", "txt"])
```
#### **Response**
```json
"Generated combined prompt in output.txt"
```

---

## **Building AI Agents with the ToolKit**
The **CodePromptForge ToolKit** is designed to be **integrated into LangChain agents** for intelligent code analysis. Here’s how you can create a **React agent** that uses these tools:

```python
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from codepromptforge.main import CodePromptForge

# Initialize the CodePromptForge toolkit
forge = CodePromptForge(base_dir=".")

# Create an agent with the tools
agent = initialize_agent(
    tools=forge.get_tools(),
    llm=ChatOpenAI(temperature=0),
    agent="zero-shot-react-description",
    verbose=True
)

# Example: Ask the agent to analyze the project directory
agent.run("List all Python files in the project and summarize their content.")
```

### **Expected Behavior**
1. The agent will call `get_directory_tree()` to explore the project structure.
2. It will filter files using `find_files(["py"])` to locate Python scripts.
3. It will use `get_file_content()` to analyze each file.
4. Based on the retrieved content, it will generate a **summary**.

---

## **Conclusion**
The **CodePromptForge ToolKit** provides a **ready-to-use suite of tools** that can be seamlessly integrated into **AI agents** for **code reading, modification, and generation**. Whether you're building **LLM-based code assistants**, **automated reviewers**, or **code refactoring agents**, these tools **simplify and automate complex workflows**.

---
🚀 **Start developing with CodePromptForge today!** 🚀