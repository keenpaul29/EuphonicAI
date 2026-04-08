```markdown
# EuphonicAI Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the EuphonicAI Python codebase. You will learn about file naming, import/export styles, commit message habits, and how to write and run tests. This guide is designed to help contributors quickly align with the project's established practices.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `audioProcessor.py`, `dataLoader.py`

### Import Style
- Use **aliasing** when importing modules.
  - Example:
    ```python
    import numpy as np
    import pandas as pd
    ```

### Export Style
- **Mixed**: Both explicit and implicit exports are used.
  - Example:
    ```python
    # Explicit export
    def processAudio(data):
        ...

    # Implicit export (no __all__ specified)
    class AudioModel:
        ...
    ```

### Commit Patterns
- **Freeform** commit messages, typically around 51 characters.
- No enforced prefix or structure.

## Workflows

### Adding a New Feature
**Trigger:** When implementing a new capability or function  
**Command:** `/add-feature`

1. Create a new Python file using camelCase (e.g., `featureName.py`).
2. Use aliasing for all imports.
3. Implement your feature.
4. Export classes/functions as needed.
5. Write corresponding tests in a `*.test.*` file.
6. Commit with a concise, descriptive message.

### Fixing a Bug
**Trigger:** When resolving a defect or issue  
**Command:** `/fix-bug`

1. Locate the relevant file (use camelCase).
2. Apply the fix.
3. Update or add tests in the related `*.test.*` file.
4. Commit with a message describing the fix.

### Writing and Running Tests
**Trigger:** When verifying code correctness  
**Command:** `/run-tests`

1. Create or update a test file matching `*.test.*` (e.g., `audioProcessor.test.py`).
2. Write test cases for your functions/classes.
3. Use the project's preferred (unknown) test runner to execute tests.
   - Example (if using pytest):
     ```
     pytest
     ```
4. Ensure all tests pass before committing.

## Testing Patterns

- Test files follow the `*.test.*` naming convention.
  - Example: `audioProcessor.test.py`
- The testing framework is **unknown**; check project documentation or existing test files for specifics.
- Place tests alongside or near the code they test.

## Commands
| Command      | Purpose                                 |
|--------------|-----------------------------------------|
| /add-feature | Start the process for adding a feature  |
| /fix-bug     | Begin workflow for fixing a bug         |
| /run-tests   | Run all test files in the codebase      |
```
