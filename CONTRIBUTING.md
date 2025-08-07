# Contributing to YouTube Transcript Grabber

Thank you for your interest in contributing! 🎉 This document provides guidelines and information for contributors.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/yourusername/youtube-transcript-grabber/issues) to avoid duplicates.

When creating a bug report, include:
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Python version and operating system
- Full error message/traceback
- Video ID that causes the issue (if applicable)

Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml).

### 💡 Suggesting Features

Feature suggestions are welcome! Please:
- Check existing [feature requests](https://github.com/yourusername/youtube-transcript-grabber/issues?q=is%3Aissue+label%3Aenhancement)
- Provide clear use case and rationale
- Consider implementation complexity
- Be open to discussion and feedback

Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml).

### 🔧 Code Contributions

#### Development Setup

1. **Fork the repository**

2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/youtube-transcript-grabber.git
   cd youtube-transcript-grabber
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies:**
   ```bash
   pip install -e .[dev]
   playwright install chromium
   ```

5. **Verify setup:**
   ```bash
   pytest --version
   black --version
   youtube-transcript-grabber --help
   ```

#### Making Changes

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write your code:**
   - Follow the existing code style
   - Add docstrings for new functions
   - Include type hints where appropriate
   - Add tests for new functionality

3. **Run quality checks:**
   ```bash
   # Format code
   black src/ tests/ examples/
   isort src/ tests/ examples/
   
   # Run linter
   flake8 src/ tests/
   
   # Type checking
   mypy src/youtube_transcript_grabber
   
   # Run tests
   pytest
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

#### Pull Request Process

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request** using our [PR template](.github/PULL_REQUEST_TEMPLATE.md)

3. **Ensure all checks pass:**
   - All tests pass
   - Code coverage maintained
   - No linting errors
   - Documentation updated

4. **Respond to feedback** and make requested changes

5. **Celebrate!** 🎉 Your contribution will be merged once approved.

## Development Guidelines

### Code Style

- **Python Style**: Follow PEP 8
- **Line Length**: 88 characters (Black default)
- **Imports**: Use isort for consistent import ordering
- **Docstrings**: Google-style docstrings for public functions
- **Type Hints**: Use type hints for function parameters and returns

Example:
```python
def extract_transcript(self, video_id: str) -> List[Tuple[str, str]]:
    """
    Extract transcript from a YouTube video.
    
    Args:
        video_id: YouTube video ID (e.g., "Iv-u8hwjHw4")
        
    Returns:
        List of (timestamp, text) tuples
        
    Raises:
        VideoNotFoundError: If video is not accessible
        TranscriptNotFoundError: If no transcript is available
    """
```

### Testing

- **Write tests** for all new functionality
- **Maintain coverage** at current levels or higher  
- **Use descriptive test names**: `test_extract_transcript_with_invalid_video_id`
- **Test edge cases**: Empty responses, network errors, etc.
- **Mock external services** when appropriate

### Documentation

- **Update README** for user-facing changes
- **Add examples** for new features
- **Update API docs** in `docs/api.md`
- **Include troubleshooting** tips for common issues

### Commit Messages

Use conventional commit format:

- `Add:` New features
- `Fix:` Bug fixes  
- `Update:` Modifications to existing features
- `Remove:` Removing features or files
- `Docs:` Documentation changes
- `Test:` Test-related changes
- `Refactor:` Code refactoring
- `Style:` Code style/formatting changes

Examples:
- `Add: support for batch transcript extraction`
- `Fix: handle missing transcript button in new YouTube layout`
- `Update: improve error messages for network timeouts`

## Areas for Contribution

### 🔥 High Priority

- **Test coverage**: Expand test suite
- **Error handling**: Improve error messages and recovery
- **Performance**: Optimize extraction speed
- **Documentation**: More examples and use cases

### 🚀 Feature Ideas

- **Multiple language support**: Extract transcripts in different languages
- **Caching system**: Cache results to avoid re-extraction  
- **Progress tracking**: Better progress indication for batch operations
- **Export formats**: Support for SRT, VTT, and other subtitle formats
- **Async support**: Async/await API for better performance

### 🛠️ Technical Improvements

- **Browser optimization**: Faster browser startup and navigation
- **Selector robustness**: Better handling of YouTube UI changes
- **Memory efficiency**: Reduce memory usage for large batches
- **Error recovery**: Better retry mechanisms and fallbacks

### 📚 Documentation

- **Video tutorials**: Screen recordings showing usage
- **Use case examples**: Real-world application examples
- **API reference**: Complete API documentation
- **Troubleshooting**: Expand troubleshooting guide

## Testing Guidelines

### Running Tests

```bash
# All tests
pytest

# Specific test file  
pytest tests/test_grabber.py

# With coverage
pytest --cov=youtube_transcript_grabber

# Verbose output
pytest -v
```

### Test Categories

1. **Unit tests**: Test individual functions
2. **Integration tests**: Test full workflows
3. **CLI tests**: Test command-line interface
4. **Error handling tests**: Test exception scenarios

### Mock Guidelines

- **Mock external services**: Don't make real YouTube requests in tests
- **Use fixtures**: Create reusable test data
- **Test error conditions**: Mock failures and edge cases

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release PR
- [ ] Tag release after merge
- [ ] GitHub Actions deploys to PyPI

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Email**: Maintainer contact for sensitive issues

### Resources

- **Documentation**: [docs/](docs/) directory
- **Examples**: [examples/](examples/) directory  
- **API Reference**: [docs/api.md](docs/api.md)
- **Troubleshooting**: [docs/troubleshooting.md](docs/troubleshooting.md)

## Recognition

Contributors are recognized in:
- **CHANGELOG.md**: Major contributions noted in release notes
- **README.md**: Contributors section
- **GitHub**: Contributor statistics and commit history

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to YouTube Transcript Grabber! 🙏

Your contributions help make this tool better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, every contribution is valuable and appreciated.