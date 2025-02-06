from setuptools import setup, find_packages

# 🔹 Get the list of all packages except `assistant`
default_packages = find_packages(exclude=["codepromptforge.assistant", "codepromptforge.assistant.*"])

# 🔹 Include `assistant` only when `[assistant]` extra is used
all_packages = find_packages()

setup(
    name="codepromptforge",
    version="1.0.8",

    # ✅ Only install `core/` by default; include `assistant/` with extras
    packages=default_packages,  # Default install excludes `assistant/`

    include_package_data=True,  # Ensure non-code files like templates/static are included

    install_requires=[
        "pytest",
        "pydantic",
        "langchain",
        "pathspec",
    ],  # ✅ Core dependencies (installed by default)

    extras_require={
        "assistant": [  # ✅ Optional dependencies for `assistant`
            "langchain_ollama",
            "langgraph",
            "ollama",
            "duckduckgo-search",
            "langchain-community",
            "flask"
        ],
        "full": all_packages  # ✅ Allows installing everything using `[full]`
    },

    entry_points={
        "console_scripts": [
            "codepromptforge=codepromptforge.core.cli:main"
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