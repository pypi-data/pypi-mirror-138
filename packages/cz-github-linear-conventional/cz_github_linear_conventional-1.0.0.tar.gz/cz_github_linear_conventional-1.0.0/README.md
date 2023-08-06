# cz-github-linear-conventional

# pre-commit

Add this plugin to the dependencies of your commit message linting with pre-commit.

Example .pre-commit-config.yaml file.

```yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v2.17.13
    hooks:
      - id: commitizen
        stages: [commit-msg]
        additional_dependencies: [cz-github-jira-conventional]
```

Install the hook with

```bash
pre-commit install --hook-type commit-msg
```
