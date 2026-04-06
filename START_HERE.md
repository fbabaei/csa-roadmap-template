# Start Here

If you just cloned this repository, use this quick path.

## One-command start

From the repository root (required):

```bash
python scripts/start_portal.py
```

Alternative launcher (works even when your shell starts elsewhere):

```bash
powershell -ExecutionPolicy Bypass -File scripts/start_portal_from_anywhere.ps1
```

If your shell is in a different folder, first change directory:

```bash
cd <path-to-csa-roadmap-template>
python scripts/start_portal.py
```

What this does:

- Starts a local portal server
- Opens the browser to `index.html`
- Prints follow-along steps in the terminal

To run on a different port:

```bash
python scripts/start_portal.py --port 5600
```

To run without auto-opening a browser:

```bash
python scripts/start_portal.py --no-open
```

Troubleshooting:

- If you see `can't open file ...scripts/start_portal.py`, your current directory is not the repo root.
- Run `pwd`/`Get-Location` and switch to this repository before running commands.

## Follow-along order

1. Review `README.md`
2. Use `QUICKSTART.md`
3. Fill `docs/PLAN_TEMPLATE.md`
4. Map projects in `projects/INDEX.md`
5. Start `week-01/WEEK_ASSIGNMENT.md` and `week-01/STATUS.md`
6. Run gap analysis after filling `docs/SKILL_ASSESSMENT_TEMPLATE.md`

## Gap analysis command

```bash
python scripts/analyze_gaps.py --export
```

Then refresh the portal and open the **Gap Analysis** section.

## Internal reference example

Use `docs/WEEK_01_COMPLETED_EXAMPLE.md` as a quality bar for internal week-01 completion.
