from setuptools import setup, find_packages

# Function to read requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="codepromptforge",             
    version="1.0.1",                
    packages=find_packages(),
    install_requires=read_requirements(),  # ✅ Read dependencies from requirements.txt
    entry_points={
        "console_scripts": [
            "codepromptforge=codepromptforge.cli:main"
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