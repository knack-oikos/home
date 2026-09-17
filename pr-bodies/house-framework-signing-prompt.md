Closes #1. Opened into `refactor/harness-agnostic-housekeeper` (#2), not `main`, as asked; the owner merges this into that branch and then merges #2.

## What the user sees

- `house init` prints, before its bootstrap commit and only when the git config signs: `sign: the bootstrap commit is signed (openpgp, key <id>); a passphrase prompt that appears now is for it. --no-commit leaves the files for the owner to commit instead`. With no `user.signingkey` it names the committer identity gpg picks by.
- `mise run welcome` gains `== signing ==`: `commits here: signed (<format>, key <id>)` or `commits here: unsigned`, and when signed, that `agent-env` sets the author only, so an agent's commit carries this same key and verifies as its holder, and that a stalled prompt is reported, never worked around.
- The house README gains a *Signing* section: the prompt is for that key and names no terminal; an agent's commit is signed with the owner's key, and per-agent keys are the backlog entry; why it repeats (gpg-agent's 10-minute and 2-hour defaults) and that a longer cache or a keyring-backed pinentry is machine setup; how the owner turns signing off per repository.
- The three home briefs and the three Claude Code definitions carry one sentence each: if the machine signs, the agent's commit carries the owner's key, and a commit that stalls on the passphrase prompt is reported, never worked around — no turning signing off, no `<HOUSE>_OWNER_COMMIT`.

## Ideas from #1: taken and left

Taken, all four: `init` says so before the commit and names `--no-commit`; `welcome` reports the signing state with the key and that an activated agent still signs as the owner; the README section; the home briefs and the exported definitions say stop and report.

Left: `doctor` says nothing about signing (not asked, and not a health check); the contract template is untouched (authority-only, and "Know when to abort" already covers a missing credential); no gpg-agent configuration is written or suggested beyond the README sentence; nothing changes which key signs.

## Harness-agnostic

`init`, `welcome`, `lib/house.sh`, the README template and the home briefs mention git and gpg only. The sentence in the definitions lives under `templates/harness/claude-code/`.

## Reproduction and tests

Under a global git config with `commit.gpgsign=true`, `user.signingkey=0123456789ABCDEF` and a fake `gpg.program` that logs its arguments, `house init` on the base invoked gpg (`--status-fd=2 -bsau 0123456789ABCDEF`) and printed nothing about it; `welcome` had no line about signing. The new test helper `signing_env` does the same through `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_*`, so the suite's `GIT_CONFIG_GLOBAL=/dev/null` stays and no real gpg or key is touched.

`mise run test`: 41 → 46, all passing; `bash -n` over the executable templates ok; `git diff --check` clean. Seven touched tests fail by name on pristine `444d41b` with the test files copied in (init names the key; init names the committer identity; welcome; README and housekeeper home; builder home; judge home; export definitions). The eighth, `init says nothing about signing when commits are unsigned or --no-commit`, passes on both trees and is a control.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
