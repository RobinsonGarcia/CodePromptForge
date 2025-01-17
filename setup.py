from setuptools import setup, find_packages

setup(
    name="codepromptforge",             
    version="0.1.0",                
    packages=find_packages(),
    install_requires=[],            
    entry_points={
        "console_scripts": [
            "codepromptforge=codepromptforge.cli:main"
        ],
    },
    description="A tool to combine code files into a single prompt",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="RG",
    author_email="rlsgarcia@icloud.com",
    url="https://github.com/RobinsonGarcia/PromptForge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Specify Python version requirement if needed
)