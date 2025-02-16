from setuptools import setup, find_packages

# ✅ Find all sub-packages, including `assistant`
core_packages = find_packages(include=["codepromptforge", "codepromptforge.core"])
assistant_packages = find_packages(include=["codepromptforge.assistant", "codepromptforge.assistant.*"])

setup(
    name="codepromptforge",
    version="0.0.7",  # Increment the version

    # ✅ Only install core by default
    packages=core_packages,  

    include_package_data=True,

    install_requires=[
        "pytest",
        "pydantic",
        "langchain",
        "pathspec",
        "langchain_community",
    ],

    extras_require={
        # ✅ When installing `[assistant]`, include both dependencies & assistant package
        "assistant": [
            "langchain_ollama",
            "langgraph",
            "ollama",
            "duckduckgo-search",
            "flask"
        ] + assistant_packages  # <-- Ensure assistant submodules are included
    },

    entry_points={
        "console_scripts": [
            "codepromptforge=codepromptforge.core.cli:main",
            "cli_assistant=codepromptforge.assistant.cli_assistant:main",  # ✅ CLI Assistant
            "web_assistant=codepromptforge.assistant.web_assistant:main",  # ✅ Web Assistant
        ],
    },

    description="A tool to combine code files into a single prompt",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="RG",
    url="https://github.com/RobinsonGarcia/CodePromptForge",
    author_email="rlsgarcia@icloud.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)