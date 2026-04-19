# GitHub Guidelines

Load when work touches GitHub issues, pull requests, reviews, or branch publishing.

## Communication

All GitHub-facing text must be in English regardless of the user's chat language.

Applies to:

- issue titles and bodies
- PR titles and descriptions
- commit messages
- PR review replies
- inline PR comments
- follow-up comments

User-facing chat follows the user's language.

## Project Hygiene

- move an issue to `In Progress` when implementation begins
- no actively worked issue should remain in `Todo`
- if a PR is open, the issue must not remain in `Todo`

## Branch and PR Discipline

- one issue per branch unless the user wants combined scope
- do not merge branches or PRs unless the user explicitly asks
- before GitHub issue work, check open PR overlap to avoid duplication
- PRs opened by Codex should be ready for review by default, not draft
- open a draft PR only if the user explicitly asks for draft or incomplete publication
- before opening a PR, validation and review gates should be complete enough that the PR is reviewable
- if Codex opened a draft PR by mistake, convert it to ready for review once the branch is green
- branch names must use format `feat/[issue-id]-[short-description]`
- preserve tracker casing in `issue-id` when practical, for example `KIM-387`
- `short-description` must be short, lowercase, and hyphenated
- do not prepend username, org, personal namespace, or alternate prefix unless the user explicitly asks
