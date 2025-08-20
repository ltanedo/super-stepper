from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="super-stepper",
    version="0.1.0",
    author="Developer",
    author_email="lloydtan@buffalo.com",
    description="A Python decorator module for creating beautiful, organized workflow displays with phases, tasks, and comprehensive error handling",
    url="https://github.com/ltanedo/super-stepper",
    license="MIT",
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    py_modules="["super_stepper"]  # For single-file packages",
    install_requires=["rich>=10.0.0"],
    keywords=["python", "workflow", "decorator", "progress", "phases", "tasks", "automation", "devops", "rich", "console"],
    classifiers=["Development Status :: 4 - Beta", "Intended Audience :: Developers", "Intended Audience :: System Administrators", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8", "Programming Language :: Python :: 3.9", "Programming Language :: Python :: 3.10", "Programming Language :: Python :: 3.11", "Programming Language :: Python :: 3.12", "Topic :: Software Development :: Libraries :: Python Modules", "Topic :: System :: Systems Administration", "Topic :: Utilities", "Topic :: Software Development :: User Interfaces", "Topic :: Terminals"],
    project_urls={"Bug Reports": "https://github.com/yourusername/super-stepper/issues","Source": "https://github.com/yourusername/super-stepper","Documentation": "https://github.com/yourusername/super-stepper#readme"},
    long_description=long_description,
    packages=find_packages(),
)
