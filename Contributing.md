# Contributing to CaloRhythm

CaloRhythm is an open-source project, and we welcome contributions from anyone interested in improving the system.

---

## Getting Started

Before contributing, please prepare your development environment:

1. **Fork and Clone** the repository.

2. **Install Dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Prepare Required Data**

   CaloRhythm requires the **National Standard Food Composition Database (v10.3)**.  
   Download the Excel file, clean the sheets according to the documentation,  
   and place it in the project root as:

   ```
   data.xlsx
   ```

   Without this file, the application will not run.

---

## Branch Strategy

CaloRhythm uses a simple and clean branching model:

- **feature/your-feature-name**  
  Example: `feature/diet-optimizer-ui`

- **fix/issue-description**  
  Example: `fix/nan-error-in-optimizer`

- **docs/update-description**  
  Example: `docs/update-api-reference`

All branches should originate from **main**.

After completing your work:

1. Open a Pull Request (PR) into **main**  
2. Request a review  
3. After approval, changes will be merged into the next release

---

## Issues

Please use the provided issue templates.

### For bug reports, include:
- Steps to reproduce  
- Expected behavior  
- Actual behavior  
- Screenshots (if relevant)

### For feature requests, include:
- The problem you're trying to solve  
- Why the feature is useful  
- Suggested approach (optional)

---

## Pull Request Guidelines

- Provide a clear summary of your changes  
- Reference related issues using keywords such as:  
  `Fixes #3`  
  `Closes #5`
- Keep commits focused and descriptive  
- Ensure your changes follow the project's coding style

---

## Community Principles

All contributors must follow the project's Code of Conduct to ensure  
a respectful, inclusive, and collaborative environment.

We appreciate your contributions —  
together, we improve CaloRhythm for everyone.
