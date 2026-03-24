# Project Agents for Copilot CLI

This repository defines custom agents for GitHub Copilot CLI.

Available agents:

- `python-planner`: Break feature work into implementable steps with risks and tests.
- `python-reviewer`: Review changes for bugs, regressions, security, and missing tests.
- `python-bugfixer`: Propose minimal safe fixes with root-cause focus.
- `python-tester`: Design practical pytest coverage for target code.

Usage examples:

- `copilot --agent python-planner`
- `copilot --agent python-reviewer`
- `copilot --agent python-bugfixer`
- `copilot --agent python-tester`

Tip:

- For non-interactive use: `copilot -p "<task>" --allow-all-tools --agent python-reviewer`
