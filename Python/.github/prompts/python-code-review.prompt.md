---
agent: ask
description: "Use when: reviewing Python code for bugs, regressions, security issues, and missing tests"
---
Review this Python change with a strict code-review mindset.

Scope:
${input:PR diff, file list, or feature summary}

Review priorities:
1. Correctness bugs and behavioral regressions.
2. Security issues and unsafe patterns.
3. Edge cases, error handling, and input validation.
4. Performance hotspots and unnecessary complexity.
5. Test gaps and weak assertions.

Output format:
1. Findings first, ordered by severity.
2. For each finding include:
- Why it is a problem
- Concrete fix suggestion
- Suggested test case
3. If no issues found, say so explicitly and list residual risks.
