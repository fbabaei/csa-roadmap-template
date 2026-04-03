# Security Policy

## Scope

This repository is a reusable template and does not ship a running service by default. Security concerns here are primarily about:

- unsafe example content
- accidental inclusion of secrets or private environment details
- broken governance or validation guidance
- insecure automation recommendations

## Reporting a security issue

If you find a security issue in this repository:

1. Do not open a public issue with exploit details.
2. Contact the repository owner directly through internal or approved reporting channels.
3. Include the affected file, risk summary, and reproduction notes.

## Expected contributor behavior

- Never commit credentials, tokens, or private environment details.
- Keep examples generic and safe for public template reuse.
- Prefer least-privilege and secure-by-default guidance in docs and templates.
- Review workflow and automation changes for unintended exposure or privilege escalation.

## Template security expectations

When adapting this template for a real team or program:

- define ownership and approval paths
- review branch protection settings
- review repository visibility and access
- review automation permissions before enabling new workflows
