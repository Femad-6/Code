---
agent: ask
description: "Use when: creating or improving Python tests with pytest and meaningful coverage"
---
Design and implement tests for this Python code using pytest.

Target:
${input:Function, class, or module to test}

Context:
${input:Current behavior, edge cases, dependencies}

Testing requirements:
1. Cover happy path, edge cases, and failure paths.
2. Use deterministic tests with clear Arrange-Act-Assert structure.
3. Mock external I/O only when needed.
4. Keep tests readable and maintainable.

Output format:
1. Test plan
2. Proposed test cases
3. Suggested test file locations
4. Notes on fixtures, mocks, and data setup
