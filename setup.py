from setuptools import setup, find_packages

setup(
    name="promptforge",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "promptforge = promptforge.cli:main",
        ],
    },
    description="A tool to combine code files into prompts for LLM-based code improvements",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
)