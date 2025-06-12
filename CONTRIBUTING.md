Contributing to Easy-To-You Automation
Thank you for your interest in contributing to Easy-To-You Automation! This document provides guidelines and instructions for contributing.
🎯 How to Contribute
Reporting Bugs

Search existing issues to avoid duplicates
Use the bug report template when creating new issues
Provide detailed information including:

Operating system and Python version
Complete error messages and stack traces
Steps to reproduce the issue
Expected vs actual behavior

Suggesting Features

Check existing feature requests to avoid duplicates
Use the feature request template
Describe the problem your feature would solve
Explain the proposed solution in detail

Code Contributions
Setup Development Environment
bash# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/easy-to-you-automation.git
cd easy-to-you-automation

# Create virtual environment

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install development dependencies

pip install -r requirements-dev.txt

# Install pre-commit hooks

pre-commit install
Development Workflow

Create a feature branch from main
bashgit checkout -b feature/your-feature-name

Make your changes following our coding standards
Write tests for new functionality
Run tests and linting
bash# Run tests
pytest

# Run linting

flake8 src/ tests/
black src/ tests/
mypy src/

Commit your changes with descriptive messages
bashgit commit -m "feat: add new feature description"

Push and create a Pull Request

📋 Coding Standards
Code Style

Follow PEP 8 guidelines
Use Black for code formatting
Add type hints for function parameters and return values
Write docstrings for all public functions and classes

Testing

Write unit tests for new functionality
Maintain test coverage above 80%
Test edge cases and error conditions

Documentation

Update README.md for user-facing changes
Add docstrings with examples for complex functions
Update changelog for all changes

🔄 Pull Request Process

Update documentation as needed
Add tests for new functionality
Ensure all tests pass and code is properly formatted
Update CHANGELOG.md with your changes
Create a detailed PR description using our template

PR Requirements

Code follows style guidelines
Tests are added and passing
Documentation is updated
CHANGELOG.md is updated
No breaking changes (or clearly documented)

🚀 Release Process

Version bump in setup.py and pyproject.toml
Update CHANGELOG.md with release notes
Create release tag with semantic versioning
GitHub Actions will handle the rest

📞 Getting Help

GitHub Discussions for questions and ideas
GitHub Issues for bugs and feature requests
Email radipta111@gmail.com for private matters

📄 Code of Conduct

Be respectful and inclusive
Provide constructive feedback
Help others learn and grow
Follow GitHub's community guidelines

Thank you for contributing! 🎉
