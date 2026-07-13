---
name: hepdata-cli
description: Search HEPData and download experimental high-energy physics records or individual tables with the official hepdata-cli command-line tool. Use when Codex needs to find HEPData records by query, resolve HEPData or INSPIRE identifiers, list table names, download CSV, YAML, JSON, ROOT, YODA, YODA1, or YODA-HDF5 data, or verify downloaded HEPData artifacts.
---

# HEPData CLI

Use the official [`HEPData/hepdata-cli`](https://github.com/HEPData/hepdata-cli) package. Keep search/download work read-only with respect to HEPData.

## Prepare the tool

1. Check availability with `command -v hepdata-cli` and `hepdata-cli --version`.
2. If unavailable, ask before installing. Prefer an isolated virtual environment owned by the current project or a temporary directory; install with `python3 -m pip install hepdata-cli` inside it.
3. Run `hepdata-cli --help` after installation. Do not assume options from memory if installed help differs from this skill.
4. Treat service access and package installation as network operations subject to the current environment's approval rules.

Read [references/cli-reference.md](references/cli-reference.md) when exact options, identifier constraints, formats, API use, or failure handling matter.

## Search and download

1. Translate the request into a narrow HEPData search query. Preserve quoted advanced-search expressions as one shell argument.
2. Search interactively before downloading:

   ```bash
   hepdata-cli find 'reactions:"P P --> HIGGS X"'
   hepdata-cli find 'collaboration:ATLAS Higgs' -i hepdata
   ```

3. Confirm the intended record when a query returns multiple plausible matches. Record the identifier type explicitly.
4. List exact table names before a table-only download:

   ```bash
   hepdata-cli fetch-names 1234567 -i inspire
   ```

5. Download into a user-approved or task-local directory. Always pass both format and identifier type:

   ```bash
   hepdata-cli download 1234567 -i inspire -f yaml -d ./hepdata-downloads
   hepdata-cli download 987654 -i hepdata -f csv -t 'Table 1' -d ./hepdata-downloads
   ```

6. Inspect the resulting paths and verify them:

   ```bash
   python3 scripts/verify_download.py ./hepdata-downloads
   ```

7. Report the query, selected record and identifier type, requested format/table, output directory, and verification result. Do not claim physics interpretation from file presence alone.

## Choose formats

- Prefer `yaml` for HEPData-native structured content and uncertainty metadata.
- Prefer `csv` for simple tabular inspection, while checking all generated table files.
- Prefer `json` for programmatic record metadata.
- Use `root`, `yoda`, `yoda1`, or `yoda.h5` only when the downstream analysis requires that ecosystem.

## Guardrails

- Do not pass arXiv IDs directly to `download` or `fetch-names`; those commands accept only `hepdata` or `inspire` identifier types. Use arXiv IDs to search, then resolve an accepted identifier.
- Avoid unreviewed shell substitution for broad searches. Search first, inspect IDs, then pass an explicit ID list to `download`.
- Quote table names and queries. Keep downloaded data outside the skill directory unless the user explicitly requests fixtures.
- Do not invoke `upload` unless the user explicitly requests an upload and confirms the target. Never place a password or invitation cookie in source files, logs, command history, or the final response; allow the CLI to prompt for secrets.
- Surface HTTP, service, extraction, and empty-result failures. Do not silently fall back to scraped or fabricated data.

## Use the Python API only when needed

Use `hepdata_cli.api.Client` when a script needs structured return values or controlled iteration. Prefer CLI commands for ordinary search/download tasks. Pin or record the installed package version when reproducibility matters.
