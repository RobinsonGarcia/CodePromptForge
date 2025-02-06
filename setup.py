from setuptools import setup, find_packages

setup(
    name="codepromptforge",             
    version="0.0.3",                
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pydantic",
        "langchain",
        "pathspec",
    ],  # ✅ Core dependencies

    extras_require={  
        "assistant": [  
            "langchain_ollama",  # ✅ Dependencies required for the assistant module
            "langgraph",
            "ollama",
            "duckduckgo-search",
            "langchain-community"
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
    python_requires=">=3.7",  # Specify Python version requirement if needed
)