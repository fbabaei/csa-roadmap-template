# Branch Protection Guidance

## Recommended baseline for `main`

Enable these settings on the default branch:

- Require a pull request before merging
- Require at least 1 approval
- Dismiss stale approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict direct pushes to the default branch
- Require conversation resolution before merging

## Recommended status checks

At minimum, require:

- `Validate Repository`

## Suggested operating model

- Use short-lived branches for changes
- Link pull requests to issues when possible
- Keep template changes small and reviewable
- Use CODEOWNERS to request review from the repository owner

## Team adaptation notes

If this template is reused in a larger org:

- increase required approvals for shared ownership
- add security review for workflow or automation changes
- protect release branches if you introduce them
