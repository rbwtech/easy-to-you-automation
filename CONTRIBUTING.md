# Contributing to Easy-To-You Automation

Thank you for your interest in contributing to Easy-To-You Automation! This document provides guidelines and instructions for contributing to our project.

## 🎯 How to Contribute

### Reporting Bugs

1. **Search existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Provide detailed information** including:
   - Operating system and Python version
   - Complete error messages and stack traces
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Sample files (if applicable, without sensitive content)

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Use the feature request template** when available
3. **Describe the problem** your feature would solve
4. **Explain the proposed solution** in detail
5. **Consider the scope** and impact on existing functionality

## 💻 Code Contributions

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/easy-to-you-automation.git
cd easy-to-you-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### Development Workflow

1. **Create a feature branch** from main

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write tests** for new functionality

4. **Run tests and linting**

   ```bash
   # Run tests
   pytest

   # Run linting
   flake8 src/ tests/
   black src/ tests/
   mypy src/
   ```

5. **Commit your changes** with descriptive messages

   ```bash
   git commit -m "feat: add new feature description"
   ```

6. **Push and create a Pull Request**

## 📋 Coding Standards

### Code Style

- **Follow PEP 8** guidelines for Python code
- **Use Black** for code formatting (line length: 88)
- **Add type hints** for function parameters and return values
- **Write docstrings** for all public functions and classes
- **Use meaningful variable names** and avoid abbreviations

### Testing

- **Write unit tests** for new functionality
- **Maintain test coverage** above 80%
- **Test edge cases** and error conditions
- **Mock external dependencies** (easytoyou.eu service)
- **Include integration tests** for critical workflows

### Documentation

- **Update README.md** for user-facing changes
- **Add docstrings** with examples for complex functions
- **Update changelog** for all changes
- **Include inline comments** for complex logic

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** as needed
2. **Add tests** for new functionality
3. **Ensure all tests pass** and code is properly formatted
4. **Update CHANGELOG.md** with your changes
5. **Test with both v1 and v2** scripts if applicable

### PR Requirements

- [ ] Code follows style guidelines
- [ ] Tests are added and passing
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow conventional format

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## 🚀 Release Process

### For Maintainers

1. **Version bump** in `setup.py` and `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create release tag** with semantic versioning
4. **GitHub Actions** will handle package publishing

### Semantic Versioning

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 📞 Getting Help

- **GitHub Discussions** for questions and ideas
- **GitHub Issues** for bugs and feature requests
- **Email** [radipta111@gmail.com](mailto:radipta111@gmail.com) for private matters

## 📄 Code of Conduct

### Our Standards

- **Be respectful** and inclusive in all interactions
- **Provide constructive feedback** rather than criticism
- **Help others learn and grow** within the community
- **Follow GitHub's community guidelines**
- **Respect different viewpoints** and experiences

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing private information without consent
- Any conduct inappropriate in a professional setting

### Enforcement

Project maintainers have the right to remove, edit, or reject comments, commits, code, and other contributions that don't align with this Code of Conduct.

## 🎉 Recognition

### Contributors

All contributors will be recognized in:

- README.md contributors section
- Release notes for their contributions
- GitHub contributors page

### Types of Contributions

We value all types of contributions:

- **Code contributions** (features, bug fixes, optimizations)
- **Documentation improvements** (README, guides, examples)
- **Bug reports** with detailed reproduction steps
- **Feature suggestions** with clear use cases
- **Testing and feedback** on new releases
- **Community support** in discussions and issues

## 🔧 Development Tips

### Local Testing

```bash
# Test package imports
python -c "import sys; sys.path.insert(0, 'src'); from easytoyou import IonicubeDecoder; print('✅ Import successful')"

# Test CLI scripts
python scripts/main.py --help
python scripts/easy4us.py --help

# Run specific tests
pytest tests/test_decoder.py -v

# Test with sample data
mkdir test_data
# Add sample PHP files
python scripts/main.py -u test -p test -s test_data -o test_output -v
```

### Debugging

```bash
# Enable verbose logging
python scripts/main.py -u user -p pass -s source -v

# Monitor log file
tail -f decoder.log

# Debug with pdb
python -m pdb scripts/main.py -u user -p pass -s source
```

### Common Issues

1. **Import errors**: Check Python path and virtual environment
2. **Test failures**: Ensure all dependencies installed correctly
3. **Linting errors**: Run `black` and `flake8` to fix formatting
4. **Type checking**: Run `mypy` to catch type-related issues

Thank you for contributing! 🎉

---

_This project is maintained by the community and we appreciate all contributions, big and small._
