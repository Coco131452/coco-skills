# Index schema

The index is a disposable local cache under `.codebase-index/`. Source code remains authoritative.

- `manifest.json`: version, root, generation time, and per-file fingerprints plus parsed imports/symbols.
- `files.jsonl`: searchable file metadata without source content.
- `symbols.jsonl`: symbol name, kind, path, and line.
- `dependencies.jsonl`: source, raw import, and resolved local target when available.
- `entrypoints.jsonl`: conventional runtime, build, and container entrypoints.
- `test-map.jsonl`: test files and the local files they import.
- `index-state.json`: refresh statistics.

The extractor intentionally omits source bodies and secret-like files. Results are approximate for dynamic languages and generated code.
