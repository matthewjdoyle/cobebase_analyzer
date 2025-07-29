from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cobebase-analyzer",
    version="2.0.0",
    author="Codebase Analyzer Team",
    author_email="support@codebase-analyzer.com",
    description="A comprehensive, modular command-line tool for analyzing codebases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cobebase-analyzer=cobebase_analyzer.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="codebase analysis metrics statistics code quality development tools",
    project_urls={
        "Bug Reports": "https://github.com/matthewjdoyle/codebase_analyzer/issues",
        "Source": "https://github.com/matthewjdoyle/codebase_analyzer",
        "Documentation": "https://github.com/matthewjdoyle/codebase_analyzer#readme",
    },
)