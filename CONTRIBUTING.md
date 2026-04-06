# Contributing

## Purpose

This repository is a reusable template. Changes should improve clarity, portability, onboarding quality, or validation reliability.

## Contribution workflow

1. Open or reference an issue before making a non-trivial change.
2. Keep the template generic unless a concrete example is clearly marked as optional.
3. Prefer small, reviewable changes.
4. Run local validation before pushing:
   - `python scripts/validate_repository.py`
5. Update documentation when structure, onboarding, or workflow expectations change.

## Internal CI behavior

- In the internal `fbabaei_microsoft` repository path, validation runs on a self-hosted Linux runner.
- In non-internal owner paths (for example public forks), validation runs on GitHub-hosted `ubuntu-latest`.
- If an internal validation run fails before steps start, check self-hosted runner availability first.

## Content rules

- Keep project slots generic and reusable.
- Keep week templates lightweight and repeatable.
- Do not hardcode personal team names, subscriptions, or private environment details.
- If examples are included, present them as examples rather than defaults.

## Governance references

- Review [SECURITY.md](SECURITY.md) before changing workflows, automation, or sensitive guidance.
- Review [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md) when configuring repository protections.

## Pull request checklist

- [ ] Repository validation passes
- [ ] Links in `index.html` still work
- [ ] New docs have a top-level heading
- [ ] Template remains generic and reusable
- [ ] README or portal updated if discoverability changed

## Issue usage

Use the starter issue labels consistently:

- `onboarding` for setup and adoption tasks
- `planning` for roadmap/program definition work
- `first-week` for week-01 execution tasks
- `good-first-issue` for approachable starter work
- `documentation` for docs and guidance updates
- `portal` for portal UX and navigation changes
- `validation` for workflow and repository checks
