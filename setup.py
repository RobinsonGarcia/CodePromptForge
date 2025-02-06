from setuptools import setup, find_packages

setup(
    name="codepromptforge",             
    version="1.0.7",                

    # 🔹 Install `core/` but exclude `assistant/` by default
    packages=find_packages(exclude=["codepromptforge.assistant", "codepromptforge.assistant.*"]),

    # 🔹 Include package data (like templates/static)
    include_package_data=True,  

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