Closes #8.

Makes the repository itself usable by someone who lands on it from GitHub with no context: a license, a first screen that says who it is for, prerequisites, an install that needs only git and mise, a way to contribute, a contract addressed to anyone's agent, and a lineage note a stranger can read. Nothing under `templates/`, `examples/` or `.mise/tasks/{init,agent}` changes, and no test changes.

Five commits, one per file group, cut from `main` at `87fd50f`.

## Definition of done, line by line

| # | Line | What this PR does |
|---|---|---|
| 1 | `LICENSE` exists; the README names it | `LICENSE` is MIT, chosen from the maintainer's convention (every other public repo of theirs is MIT); the owner may swap it before merging. The README says it is MIT-licensed and that a house rendered from the templates belongs to whoever generated it and is not bound by the framework's license. **Holder note below.** |
| 2 | README says what and for whom before its first `##`; Prerequisites; an install with git and mise alone | New second paragraph: for anyone running a roster of agents against a repository, under any harness or none, not tied to the household that wrote it. New `## Prerequisites`: git, bash, mise; `mise install` brings bats. `## Install` now leads with `git clone` + `mise trust && mise install` + `mise run init example --at /path/to/example`, the form `.github/workflows/test.yml` uses; shiv is the optional second form. The `~/Work` path was already gone after #7; the example path is `/path/to/example`. |
| 3 | Every link in `README.md` and `notes/lineage.md` resolves logged-out or is marked private | Table below: every URL 200 anonymously. `olavostauros/ticket` is text, not a link, and reads "a private repository with no public link". |
| 4 | `CONTRIBUTING.md` exists; `AGENTS.md`'s first paragraph requires no house | `CONTRIBUTING.md`: open an issue first, `mise run test` and `git diff --check`, `examples --write` after a template change, conventional commits, no footers or tool attribution, read `AGENTS.md`. `AGENTS.md` opens as the contract for this repository for whoever's agent is here, under any harness or none; the lineage-in-commit rule is now "if you know, say so; if not, say it is new. Nobody is expected to know." |
| 5 | A tag and a release exist; the README says how to pin | **Owner step** (repo setting). The README already says how to pin, assuming `v0.1.0`: `git checkout v0.1.0` before either install form, since shiv installs from the working tree and reports the tag through `house --version`. |
| 6 | Topics non-empty; description free of the three lineage names | **Owner step** (repo setting); exact commands below. |
| 7 | `HOUSE_AGENTS_ROOT` named where `~/agents` first appears; `HOUSE_DEFINITIONS_DIR` where `~/.claude/agents` first appears | `HOUSE_AGENTS_ROOT` is now named at the README's first `~/agents` (the `examples/` paragraph under "Making it yours"). `HOUSE_DEFINITIONS_DIR` was already named at the first `~/.claude/agents` (the Harnesses section) as of #7; unchanged. |
| 8 | `notes/lineage.md` opens with a preface; no abbreviation before its expansion | Two-sentence preface (what the note is, who "the maintainer" and "the owner" are). `KKL` expanded on first use; `tits` expanded and linked; `fold` and `oikos` linked to their public repositories; "the owner" replaced by "the maintainer" where the note records a ruling about this repository. Where "the owner" is the house role a contract defines (files the queue, merges, asks for a preset) it is kept, and the preface says which is which. |
| 9 | Nothing under `templates/`, `examples/` or `.mise/tasks/{init,agent,doctor}`; #7's tests untouched | `templates/`, `examples/`, `init`, `agent` and every file under `test/` are untouched. **One line of `.mise/tasks/doctor` is changed** — the `vfox-shiv#36` citation is now a full URL — because the issue's "checked and not filed" paragraph names it and the assignment put it in scope. It is its own commit (`1fb9635`) so it can be dropped if item 9 is read strictly. `test/presets.bats:169` asserts only the `a range, not a release` prefix, so the change touches no test. |

## Holder note (item 1)

The assignment asked for `Copyright (c) 2026 Olavo Stauros`. Measured on this branch: that line fails `test/own_house.bats` test 1 ("ships no household or personal name outside notes/lineage.md and lib/lineage-names"), which greps every file but those two for `olavo` and `stauros` as whole words — output `LICENSE:3:Copyright (c) 2026 Olavo Stauros`. Item 9 says #7's tests stay untouched, so the holder here is `The house-framework Authors`, which passes. If the owner wants their name on it, the one-line change that permits it is adding `--exclude=LICENSE` to the `grep` on `test/own_house.bats:21`; that edit is the owner's call and is not in this PR.

## Gates

- `mise run test`: 70 bats ok, 0 not ok; template syntax pass; `examples/` matches a fresh render. Same counts as `main` at `87fd50f` before the change.
- `git diff --check`: clean.

## Link check

Every URL extracted from `README.md` and `notes/lineage.md`, fetched anonymously with `curl -sSLo /dev/null -w '%{http_code}'`; relative links checked as files in the tree.

| file | link | result |
|---|---|---|
| README.md | https://github.com/bats-core/bats-core | 200 |
| README.md | https://github.com/KnickKnackLabs/shiv | 200 |
| README.md | https://github.com/olavostauros/house-framework | 200 |
| README.md | https://git-scm.com | 200 |
| README.md | https://mise.jdx.dev | 200 |
| README.md | AGENTS.md (relative) | exists |
| README.md | CONTRIBUTING.md (relative) | exists |
| README.md | examples/ (relative) | exists |
| README.md | LICENSE (relative) | exists |
| README.md | notes/lineage.md (relative) | exists |
| notes/lineage.md | https://github.com/KnickKnackLabs | 200 |
| notes/lineage.md | https://github.com/KnickKnackLabs/tits | 200 |
| notes/lineage.md | https://github.com/olavostauros/oikos | 200 |
| notes/lineage.md | https://github.com/ricon-family/fold | 200 |
| notes/lineage.md | `olavostauros/ticket` (text, no link) | 404 anonymously; marked private in the text |

## Deliberately not done

- No tag, release, description or topics: repo settings, owner-only. Commands below.
- No test change to allow a personal name in `LICENSE` (holder note above).
- No issue or PR templates: the issue lists them in the community-profile finding but not in the definition of done, and `CONTRIBUTING.md` covers what they would say.

## Owner steps after merge

```bash
gh release create v0.1.0 --target main --title v0.1.0 --notes "First release: house init, agent add, rules add, doctor, export claude-code, and the notes and shimmer presets. MIT-licensed; a rendered house is its generator's."
gh repo edit --description "The starting point of a house of agents: scaffolds a household (contract, roster, queue, guard, housekeeper) and its agents, under any harness or none"
gh repo edit --add-topic agents --add-topic mise --add-topic bash --add-topic scaffolding --add-topic agents-md
```

Then `gh repo view --json licenseInfo,description,repositoryTopics` and `gh release list` close items 1, 5 and 6.
