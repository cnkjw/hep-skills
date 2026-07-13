# `hepdata-cli` interface reference

This reference reflects the official `HEPData/hepdata-cli` main branch inspected on 2026-07-13. Check installed `--help` output when behavior may have changed.

## Commands

```text
hepdata-cli [--verbose] find QUERY [-kw KEYWORD] [-i IDTYPE]
hepdata-cli [--verbose] download IDS... -f FORMAT -i IDTYPE [-t TABLE] [-d DIR]
hepdata-cli [--verbose] fetch-names IDS... -i IDTYPE
hepdata-cli [--verbose] upload ARCHIVE -e EMAIL [upload options]
```

`find` accepts advanced HEPData search syntax. With `-i/--ids`, it prints a space-separated identifier list suitable for shell use. Accepted search ID types are `arxiv`, `inspire`, and `hepdata`.

`download` and `fetch-names` accept only `inspire` and `hepdata`. For `download`, both `-f/--file-format` and `-i/--ids` are required by the CLI implementation. The default output directory is `./hepdata-downloads`.

## Download formats

Accepted values are:

- `csv`
- `root`
- `yaml`
- `yoda`
- `yoda1`
- `yoda.h5`
- `json`

For a whole record, non-JSON formats are delivered as an archive and unpacked by the client. JSON is downloaded as a JSON file. With `-t/--table-name`, only the named table is requested in the selected format.

## Safe patterns

Search for candidate records:

```bash
hepdata-cli --verbose find 'reactions:"P P --> TOP TOPBAR X"'
hepdata-cli find 'collaboration:CMS top quark' -i hepdata
```

List tables, then download one:

```bash
hepdata-cli fetch-names 1234567 -i inspire
hepdata-cli download 1234567 -i inspire -f yaml -t 'Table 2' -d ./hepdata-downloads
```

Download several reviewed records:

```bash
hepdata-cli download 111111 222222 -i hepdata -f csv -d ./hepdata-downloads
```

The upstream README demonstrates command substitution between `find` and `download`. Use it only after confirming the query is narrow and the returned IDs are appropriate; explicit reviewed IDs are safer and easier to audit.

## Python API

```python
from hepdata_cli.api import Client

client = Client(verbose=True)
ids = client.find('collaboration:ATLAS Higgs', ids='hepdata', format=list)
names = client.fetch_names(ids[:1], ids='hepdata')
files = client.download(ids[:1], file_format='yaml', ids='hepdata',
                        download_dir='./hepdata-downloads')
```

The API returns structured values: `find(..., format=list)` returns identifiers as a list, `fetch_names` returns table-name lists, and `download` returns a mapping from record ID to downloaded file paths.

## Failure handling

- An empty search is a valid result; refine the query rather than inventing an identifier.
- A service `/ping` request occurs when the API client is initialized or an ordinary subcommand starts, so searches and downloads require HEPData availability.
- Invalid formats or identifier types raise assertions in the inspected implementation.
- Downloads may create several files and nested record directories. Verify the whole output tree.
- Treat archive extraction or HTTP errors as failed downloads, even if a partial output directory exists.

Primary sources: [official repository](https://github.com/HEPData/hepdata-cli), [HEPData](https://www.hepdata.net/).
