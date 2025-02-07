from setuptools import setup, find_packages

setup(
    name="codepromptforge",
    version="1.1.0",

    # ✅ Explicitly define packages; assistant is excluded by default
    packages=["codepromptforge", "codepromptforge.core"],  

    include_package_data=True,

    install_requires=[
        "pytest",
        "pydantic",
        "langchain",
        "pathspec",
        "langchain_community",  # ✅ Moved to core dependencies
    ],  # ✅ Core dependencies

    extras_require={
        "assistant": [  # ✅ Installs assistant when `[assistant]` is used
            "langchain_ollama",
            "langgraph",
            "ollama",
            "duckduckgo-search",
            "flask"
        ],
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