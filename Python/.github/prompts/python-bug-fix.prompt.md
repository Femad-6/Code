---
agent: ask
description: "Use when: fixing a Python bug with minimal safe changes and verification"
---
Fix this Python bug with minimal, safe changes.

Bug report:
${input:Describe the bug and expected behavior}

Context:
${input:Error logs, stack trace, related files}

Constraints:
1. Keep public APIs unchanged unless required.
2. Prefer the smallest patch that resolves root cause.
3. Add or update tests that reproduce and prevent regression.
4. Do not refactor unrelated code.

Output format:
1. Root cause analysis
2. Minimal patch plan
3. Exact files to edit
4. Test cases to add/update
5. Post-fix verification checklist
