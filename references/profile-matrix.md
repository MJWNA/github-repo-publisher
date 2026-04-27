# Repo Publisher Profile Matrix

Choose one profile before creating or updating files. Profiles prevent overbuilding tiny repos and under-protecting important ones.

## Profiles

| Profile | Best for | Required | Optional / conditional |
|---|---|---|---|
| `minimal` | Scratch, demo, private experiment | README, `.gitignore`, visibility, description | License, CI, issue templates |
| `internal-tool` | Private business apps and operations tools | README-private, `.repo-publisher.yml`, SECURITY, CODEOWNERS, PR template, issue templates, CI, Dependabot, secret preflight | rulesets, Actions read-only setting, CodeQL, runbook links |
| `public-oss` | Public/open-source repos | README-public, LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, SUPPORT, issue/PR templates, topics, CI, Dependabot, rulesets | Scorecard, CodeQL, release automation, social preview |
| `package` | npm/Python/Ruby/etc packages | public-oss baseline, package metadata, changelog/release flow, semver guidance | Release Please, semantic-release, provenance/trusted publishing |
| `docs-site` | Documentation sites and examples | README, license decision, deploy notes, CI, link checking, docs publish workflow | Pages/Vercel/Netlify settings, release notes |
| `strict` | Sensitive internal repos or mature public repos | strongest internal/public baseline, rulesets, CODEOWNERS, least privilege Actions, Dependabot, secret scanning, security read-back | CodeQL advanced setup, Scorecard, settings-as-code |

## New Repo Versus Existing Repo

New repo:

- Generate `.repo-publisher.yml` first.
- Generate files from templates with placeholders replaced.
- Create repo with explicit visibility.
- Push initial commit.
- Apply settings after the default branch exists.
- Verify via read-back.

Existing repo:

- Inspect current files and remotes first.
- Do not overwrite valuable README/community files blindly.
- Show a patch summary: create, update, leave unchanged, skipped.
- Prefer small additive improvements.
- Use `.repo-publisher.yml` if present to identify expected profile and prior decisions.

## Drift / Update Mode

Use this when a repo was previously published but standards improved:

1. Read `.repo-publisher.yml`.
2. Compare current files/settings against the selected profile.
3. Report drift as `missing`, `stale`, `manual`, or `intentionally skipped`.
4. Patch only clear gaps.
5. Record skipped items with reasons in the final report.

## Research-Backed Source Patterns

- DSACMS repo-scaffolder: maturity tiers and existing-repo patch mode.
- projen: generated config as source of truth and drift detection.
- Copier/Cruft: committed answers and update/check/diff workflows.
- PyScaffold/Scientific Python Cookie: one command creates serious project hygiene.
- GitHub Safe Settings / Probot Settings: settings-as-code works best when protected by CODEOWNERS.

