Contribution Guidelines
=======================

Thank you for your interest in contributing to **CaloRhythm**!
We welcome contributions of all types, including bug fixes, feature additions, and documentation improvements.

Getting Started
---------------
To contribute to the codebase, you need to set up the development environment locally.

1. **Fork and Clone** the repository.
2. **Install Dependencies**:
   Ensure you have Python 3.9+ installed, then run:

   .. code-block:: bash

      pip install -r requirements.txt

3. **Prepare Data**:
   Make sure the ``data.xlsx`` file (National Standard Food DB) is placed in the root directory.
   Without this file, the application will not launch.

Branch Strategy
---------------
We follow a strict naming convention to keep our repository organized. Please name your branches as follows:

- **Feature Development**: ``feature/your-feature-name``
    - Example: ``feature/diet-optimizer-ui``
- **Bug Fixes**: ``fix/issue-description``
    - Example: ``fix/nan-error-in-chart``
- **Documentation**: ``docs/update-description``
    - Example: ``docs/update-readme``

Commit Message Convention
-------------------------
To maintain a clean history, please follow these rules for commit messages:

1. **Use the Imperative Mood**: Write "Add feature" instead of "Added feature".
2. **Be Descriptive**: Explain *what* changed and *why*.

**Example:**
``Add safe_percentage function to prevent NaN errors in optimizer``

Pull Request (PR) Process
-------------------------
When you are ready to submit your changes:

1. **Create a Pull Request** against the ``main`` branch.
2. **Link Related Issues**:
   If your PR fixes a specific issue, include the magic keyword in the description.
   - Example: ``Closes #5`` or ``Fixes #3``
   - *This ensures the issue is automatically closed when the PR is merged.*
3. **Request a Review**:
   Assign at least one team member to review your code.
4. **Merge**:
   Once approved, the PR can be merged into the main branch.

Code Style
----------
- **Python**: We follow PEP 8 guidelines.
- **Streamlit**: Ensure UI components are organized logically (e.g., Sidebar configurations first, then Main layout).
- **Comments**: Add comments to complex logic, especially within the optimization algorithm (``scipy`` implementation).

Reporting Bugs
--------------
If you find a bug, please create a new Issue with:
- A clear title.
- Steps to reproduce the error.
- Screenshots (if applicable).
