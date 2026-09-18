Adds one line to `sources.json`:

```json
"house": "olavostauros/house-framework",
```

[house-framework](https://github.com/olavostauros/house-framework) is a public, MIT-licensed tool that scaffolds and checks a house of agents (`house init`, `house doctor`, `house agent add`). It is a shiv package in the ordinary shape — a `mise.toml` and executables under `.mise/tasks/` — and has a semver tag (`v0.1.0`), so a bare `shiv install house` resolves once the name is in the index. The README's "add an entry to `sources.json` in this repo" route is what this follows.

Until this merges, house-framework's README carries the source-file fallback (`~/.config/shiv/sources/house.json`). The plan that led here is [olavostauros/house-framework#13](https://github.com/olavostauros/house-framework/issues/13).

Checked: `jq empty sources.json` passes; the entry is in alphabetical position and the file has 50 entries.
