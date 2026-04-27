---
name: github-repo-publisher
description: Use when creating, preparing, publishing, or polishing a GitHub repository so it has complete metadata, README documentation, community files, security defaults, branch rules, and public/private visibility safeguards.
---

# GitHub Repo Publisher

Use this skill to turn a local project or new idea into a complete GitHub repository. It complements `github-repo-discovery`: discovery finds repos; this skill creates or publishes them.

## Operating Modes

Pick the mode first and say it back before writing or publishing:

| Mode | Use when | Default posture |
|---|---|---|
| `new-repo` | Creating a repo from a local directory or idea | Generate manifest, files, repo, settings, then verify. |
| `existing-repo` | Polishing a repo that already exists | Audit first, show patch summary, preserve existing docs unless replacing is clearly better. |
| `audit` | Checking repo readiness without changing it | Report gaps against the selected profile. |
| `update` | Bringing an older repo up to the current publisher baseline | Use `.repo-publisher.yml` when present; show drift before patching. |
| `release` | Tagging or drafting a release after repo setup | Use draft/review gates unless full automation is explicitly part of the repo contract. |

Use profiles rather than one-size-fits-all defaults: `minimal`, `internal-tool`, `public-oss`, `package`, `docs-site`, and `strict`. Read `references/profile-matrix.md` when choosing a profile.

## Non-negotiables

- Treat visibility as a security decision, not a cosmetic setting.
- Do not publish secrets, customer data, exports, backups, `.env` files, private keys, credentials, or production dumps.
- For existing local projects, inspect the worktree before creating/pushing anything: `git status`, `git remote -v`, `git branch --show-current`, and likely secret-bearing files.
- For public repos, include a real license or explicitly state that no open-source license has been chosen.
- For private/internal repos, prefer least-privilege team access, CODEOWNERS, secret scanning, push protection, Dependabot, and read-only Actions token defaults where available.
- Treat `README.md` as the repo's operating explanation, not a placeholder: it must explain plain-English value, technical mechanics, workflow, commands, problems solved, and why the repo matters.
- Prefer non-overwrite updates for existing repos: show what will change, preserve useful existing content, and make the smallest patch that raises repo quality.
- When docs/settings may have changed, refresh with official GitHub docs, GitHub CLI help, or Context7 before applying risky settings.

## Workflow

1. Define the repo contract.
   - mode, profile, owner/org, repo name, description, homepage, visibility, default branch, source path, license, gitignore template, topics, maintainers, support/security contact, and whether it is public/open-source or private/internal.
   - If visibility is not explicit and the project may contain proprietary or client/business data, default to private and say why.
   - Create or update `.repo-publisher.yml` so future sessions can audit/update the repo without re-deriving decisions.
2. Audit local source before publishing.
   - Check current git status/remotes and scan for obvious secret files.
   - Run `scripts/secret-preflight.sh <path>` from this skill when publishing local code.
   - Run `scripts/readme-completeness.py <path>/README.md` after generating or changing a README.
   - Do not push unrelated user changes or accidental local artifacts.
3. Generate the repository files.
   - Always: `README.md`, `.gitignore`, `SECURITY.md`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/*`, `.github/CODEOWNERS` when owners are known, and CI if commands are known.
   - The README must be complete enough for a stakeholder to understand the value and for an engineer to run, verify, maintain, and extend the repo.
   - Public/community-facing: add `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, release/changelog guidance, discoverability topics, and social preview notes.
   - Private/internal: add ownership, environment, deployment, data classification, access boundaries, and runbook links without exposing sensitive detail.
   - Reuse files under `templates/` when they fit; replace placeholders before committing.
4. Create or update the GitHub repo.
   - Prefer `gh repo create` for creation and `gh repo edit` for supported settings.
   - Use `gh api` for topics, rulesets, branch protection, Actions permissions, custom properties, and security settings not exposed by high-level `gh` flags.
   - Use git push or the contents API for files.
5. Apply protections after the default branch exists.
   - Prefer rulesets when plan/org support allows; use classic branch protection as fallback.
   - Require PRs, status checks once CI names are known, code-owner review where CODEOWNERS exists, no force pushes, no branch deletion, and linear history when it matches the repo workflow.
   - Use `templates/api/ruleset-main-light.json`, `templates/api/ruleset-main-strict.json`, or `templates/api/ruleset-tags-release.json` as starting points.
6. Verify.
   - Re-read repo metadata with `gh repo view`.
   - Check topics, files, default branch, rules/protection, Actions permissions, and security features.
   - Check README completeness and unresolved placeholders.
   - For public repos, check the GitHub community profile and README rendering when possible.

## Visibility defaults

Use this gate before creating or changing visibility:

| Case | Default | Notes |
|---|---|---|
| Open-source library, public website starter, demo, portfolio, public docs | Public | Requires license, contribution expectations, security policy, polished README, topics, and leakage scan. |
| Client work, internal tool, proprietary business process, credential-adjacent code, database/admin tooling | Private | Requires explicit access plan, ownership, CODEOWNERS, and security settings. |
| Enterprise-wide reusable internal starter | Internal | Only if every enterprise member can safely read it. Otherwise private. |
| Unsure | Private | Visibility can be widened later after review. |

Before changing private to public, explicitly warn that code, Actions history/logs, activity, and forks/visibility side effects may become visible. Use the required `gh repo edit --accept-visibility-change-consequences` flag only when the user intentionally accepts that.

## Automation Surfaces

Use the narrowest reliable tool:

```bash
gh repo create OWNER/REPO --private --description "..." --homepage "..." --source=. --remote=origin --push
gh repo edit OWNER/REPO --description "..." --homepage "..." --enable-issues --delete-branch-on-merge
gh repo edit OWNER/REPO --add-topic "topic-one,topic-two"
gh api repos/OWNER/REPO --jq '{name,visibility,description,homepage,default_branch,has_issues,has_wiki,has_discussions}'
```

For settings beyond `gh repo edit`, use `gh api` against official GitHub endpoints. Common examples:

- Replace topics: `PUT /repos/{owner}/{repo}/topics`
- Create rulesets: `POST /repos/{owner}/{repo}/rulesets`
- Classic branch protection: `PUT /repos/{owner}/{repo}/branches/{branch}/protection`
- Actions permissions: repository Actions permissions endpoints
- Custom properties: repository/org custom properties endpoints
- Security analysis settings: repository update payload when supported by plan/licensing

Templates include API payloads under `templates/api/` as starting points for `gh api repos/OWNER/REPO/rulesets --input ...`. Edit branch names, bypass actors, and required status checks before applying.

## Release Mode

Use `release` mode only after repo readiness is good:

- Draft release: use `gh release create TAG --draft --generate-notes` for simple repos.
- Release Drafter: good default when PR labels should accumulate human-reviewed release notes.
- Release Please: good when version/changelog/release should be prepared in a PR.
- semantic-release: only for repos that intentionally use Conventional Commits and automated package publishing.

Read `references/release-workflows.md` before adding release automation.

## What To Read Next

Load only the needed reference:

- `references/repo-checklist.md` for the complete public/private creation checklist, fields, and verification commands.
- `references/profile-matrix.md` for mode/profile selection and hardening defaults.
- `references/readme-patterns.md` for README structures and copy requirements.
- `references/security-settings.md` for rulesets, branch protection, Actions, Dependabot, secret scanning, CODEOWNERS, and private repo safeguards.
- `references/release-workflows.md` for release automation selection.
- `references/gh-command-reference.md` for compact `gh` and `gh api` command patterns.
- `templates/` for reusable starter files and API payloads.
- `scripts/secret-preflight.sh` for a lightweight local leak check before publishing.
- `scripts/readme-completeness.py` for README completeness scoring.

## Output Standard

When invoked, return a concise publishing plan before destructive/remote actions unless the user explicitly asked to work autonomously. After completion, report:

- repo URL and visibility
- files created or updated
- settings applied
- protections/security features enabled or skipped with reasons
- verification commands/results
- any manual follow-up, especially social preview upload or plan/licensing limitations
