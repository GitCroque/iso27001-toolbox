from setuptools import setup, find_packages
import os
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lire la version depuis __init__.py
def get_version():
    init_path = os.path.join("src", "iso27001_toolkit", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="iso27001-toolkit",
    version=get_version(),
    author="ISO27001 Toolkit Contributors",
    description="Suite d'outils CLI pour gérer la certification ISO 27001",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GitCroque/iso27001-toolbox",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
        "python-dateutil>=2.8.0",
        "cryptography>=41.0.0",
    ],
    extras_require={
        "pdf": [
            "weasyprint>=60.0",
            "markdown2>=2.4.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "bandit>=1.7.0",
        ],
        "all": [
            "weasyprint>=60.0",
            "markdown2>=2.4.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "bandit>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iso27001=iso27001_toolkit.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "iso27001_toolkit": ["templates/**/*.md", "templates/**/*.yml"],
    },
)
