# Release Workflows

Only add release automation when the repo contract needs releases. Do not force package-release machinery onto internal apps.

## Decision Table

| Need | Default |
|---|---|
| Human-reviewed release notes from merged PRs | Release Drafter |
| Version/changelog/release prepared in a PR | Release Please |
| Fully automated package publishing from Conventional Commits | semantic-release |
| One-off initial release | `gh release create --draft --generate-notes` |
| Internal app with deployments but no public versions | Deployment notes in README, no release automation by default |

## Draft Release Flow

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 --draft --generate-notes --title "v0.1.0"
```

Before publishing:

- confirm tests/build passed
- confirm README and changelog are current
- inspect generated notes
- attach assets only if they are intentional deliverables

## Release Notes Quality

Borrowed from strong `gh-release` skills:

- find previous release/tag
- inspect commits since previous tag
- enrich with merged PR titles and labels when possible
- group notes by user-visible changes, fixes, docs, chores, and breaking changes
- include compare URL
- create draft first unless automation is explicitly approved

## Automation Templates

- `templates/.github/release-drafter.yml` for lightweight human-reviewed release notes.
- Consider Release Please for multi-language/package repos where version and changelog should be handled in PRs.
- Consider semantic-release only when Conventional Commits and package publishing are already part of the repo contract.

Sources:

- Release Drafter: https://github.com/release-drafter/release-drafter
- Release Please: https://github.com/googleapis/release-please
- semantic-release: https://github.com/semantic-release/semantic-release

