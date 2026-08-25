#!/usr/bin/env python3
"""Build and query a lightweight, local codebase index."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


VERSION = 1
INDEX_REL = Path(".coco/codebase-index")
EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".coco", ".idea", ".vscode", ".vs",
    "node_modules", "vendor", "dist", "build", "coverage", "target",
    "bin", "obj", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".next", ".nuxt", ".venv", "venv",
}
SECRET_NAMES = {
    ".env", "id_rsa", "id_ed25519", "credentials", "credentials.json",
    "secrets.json", "service-account.json",
}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
TEXT_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx",
    ".java", ".kt", ".kts", ".go", ".rs", ".cs", ".cpp", ".cc",
    ".c", ".h", ".hpp", ".rb", ".php", ".swift", ".scala", ".vue",
    ".svelte", ".sql", ".graphql", ".gql", ".sh", ".ps1", ".yaml",
    ".yml", ".json", ".toml", ".xml", ".gradle", ".md",
}
CONFIG_NAMES = {
    "Dockerfile", "Makefile", "Procfile", "Gemfile", "Rakefile",
    "package.json", "pyproject.toml", "pom.xml", "build.gradle",
    "build.gradle.kts", "go.mod", "Cargo.toml",
}
ENTRY_NAMES = {
    "main.py", "app.py", "manage.py", "server.py", "index.js", "index.ts",
    "main.js", "main.ts", "server.js", "server.ts", "Program.cs",
    "main.go", "main.rs", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(path: Path) -> str:
    return path.as_posix()


def is_secret(path: Path) -> bool:
    name = path.name.lower()
    return (
        name in SECRET_NAMES
        or name.startswith(".env.")
        or path.suffix.lower() in SECRET_SUFFIXES
        or "secret" in name and path.suffix.lower() in {".json", ".yaml", ".yml"}
    )


def is_indexable(path: Path) -> bool:
    return not is_secret(path) and (
        path.suffix.lower() in TEXT_EXTENSIONS or path.name in CONFIG_NAMES
    )


def walk_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        base = Path(current)
        for name in sorted(files):
            path = base / name
            if is_indexable(path):
                yield path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    if path.stat().st_size > 2 * 1024 * 1024:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def language(path: Path) -> str:
    mapping = {
        ".py": "python", ".pyi": "python", ".js": "javascript",
        ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
        ".ts": "typescript", ".tsx": "typescript", ".java": "java",
        ".kt": "kotlin", ".kts": "kotlin", ".go": "go", ".rs": "rust",
        ".cs": "csharp", ".sql": "sql", ".vue": "vue", ".svelte": "svelte",
    }
    return mapping.get(path.suffix.lower(), path.suffix.lower().lstrip(".") or "config")


def extract_symbols(text: str, path: Path) -> list[dict]:
    ext = path.suffix.lower()
    patterns = []
    if ext in {".py", ".pyi"}:
        patterns = [("class", r"^\s*class\s+([A-Za-z_]\w*)"), ("function", r"^\s*(?:async\s+)?def\s+([A-Za-z_]\w*)")]
    elif ext in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte"}:
        patterns = [("class", r"^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)"), ("function", r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)"), ("symbol", r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)")]
    elif ext in {".java", ".kt", ".kts", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp", ".go", ".rs"}:
        patterns = [("type", r"^\s*(?:public\s+|private\s+|protected\s+|internal\s+|export\s+)?(?:class|interface|struct|enum|trait|type)\s+([A-Za-z_]\w*)"), ("function", r"^\s*(?:pub\s+|public\s+|private\s+|protected\s+|internal\s+|static\s+|async\s+)*(?:func|fn|fun)\s+([A-Za-z_]\w*)")]
    found = []
    for kind, pattern in patterns:
        regex = re.compile(pattern)
        for number, line in enumerate(text.splitlines(), 1):
            match = regex.search(line)
            if match:
                found.append({"name": match.group(1), "kind": kind, "line": number})
    return found


def extract_imports(text: str, path: Path) -> list[str]:
    ext = path.suffix.lower()
    found = []
    if ext in {".py", ".pyi"}:
        found += re.findall(r"^\s*from\s+([\.\w]+)\s+import\s+", text, re.MULTILINE)
        found += re.findall(r"^\s*import\s+([\w\.]+)", text, re.MULTILINE)
    elif ext in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte"}:
        found += re.findall(r"(?:from\s+|import\s*\(|require\s*\()\s*['\"]([^'\"]+)['\"]", text)
        found += re.findall(r"^\s*import\s+['\"]([^'\"]+)['\"]", text, re.MULTILINE)
    elif ext in {".java", ".kt", ".kts"}:
        found += re.findall(r"^\s*import\s+([\w\.]+)", text, re.MULTILINE)
    elif ext == ".go":
        found += re.findall(r"['\"]([^'\"]+)['\"]", text)
    elif ext == ".rs":
        found += re.findall(r"^\s*use\s+([\w:]+)", text, re.MULTILINE)
    return sorted(set(found))


def is_test_path(relative: str) -> bool:
    lower = relative.lower()
    name = Path(lower).name
    return (
        any(part in {"test", "tests", "spec", "specs", "__tests__", "e2e"} for part in Path(lower).parts)
        or name.startswith("test_") or ".test." in name or ".spec." in name or name.endswith("_test.go")
    )


def candidates_for_module(module: str, source: str) -> list[str]:
    source_path = Path(source)
    values = []
    if module.startswith("./") or module.startswith("../"):
        values.append(norm(Path(os.path.normpath(source_path.parent / module))))
    elif module.startswith("."):
        dots = len(module) - len(module.lstrip("."))
        base = source_path.parent
        for _ in range(max(0, dots - 1)):
            base = base.parent
        tail = module.lstrip(".").replace(".", "/")
        values.append(norm(base / tail))
    else:
        values.append(module.replace(".", "/"))
    return values


def resolve_import(module: str, source: str, known: set[str]) -> str | None:
    extensions = ["", ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".kt", ".go", ".rs", ".cs"]
    indexes = ["/__init__.py", "/index.js", "/index.ts", "/index.tsx"]
    for base in candidates_for_module(module, source):
        normalized = norm(Path(base))
        for suffix in extensions + indexes:
            candidate = normalized + suffix
            if candidate in known:
                return candidate
    return None


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def scan(root: Path, previous: dict | None = None) -> tuple[list[dict], int, int]:
    old = {item["path"]: item for item in (previous or {}).get("files", [])}
    records = []
    reused = changed = 0
    for path in walk_files(root):
        rel = norm(path.relative_to(root))
        stat = path.stat()
        prior = old.get(rel)
        if prior and prior.get("size") == stat.st_size and prior.get("mtime_ns") == stat.st_mtime_ns:
            records.append(prior)
            reused += 1
            continue
        digest = file_hash(path)
        if prior and prior.get("sha256") == digest:
            updated = dict(prior, size=stat.st_size, mtime_ns=stat.st_mtime_ns)
            records.append(updated)
            reused += 1
            continue
        text = read_text(path)
        records.append({
            "path": rel, "size": stat.st_size, "mtime_ns": stat.st_mtime_ns,
            "sha256": digest, "language": language(path), "is_test": is_test_path(rel),
            "symbols": extract_symbols(text, path), "imports": extract_imports(text, path),
        })
        changed += 1
    return sorted(records, key=lambda item: item["path"]), reused, changed


def build(root: Path, mode: str) -> int:
    index = root / INDEX_REL
    index.mkdir(parents=True, exist_ok=True)
    previous = load_json(index / "manifest.json", {}) if mode == "refresh" else {}
    files, reused, changed = scan(root, previous)
    known = {item["path"] for item in files}
    dependencies = []
    symbols = []
    entries = []
    for item in files:
        for symbol in item["symbols"]:
            symbols.append({"path": item["path"], **symbol})
        for module in item["imports"]:
            dependencies.append({"source": item["path"], "import": module, "target": resolve_import(module, item["path"], known)})
        if Path(item["path"]).name in ENTRY_NAMES:
            entries.append({"path": item["path"], "kind": "conventional-entrypoint"})
    test_map = [{"test": item["source"], "target": item["target"]} for item in dependencies if item["target"] and is_test_path(item["source"])]
    manifest = {"version": VERSION, "root": str(root), "generated_at": utc_now(), "files": files}
    write_json(index / "manifest.json", manifest)
    write_jsonl(index / "files.jsonl", [{k: v for k, v in item.items() if k not in {"symbols", "imports"}} for item in files])
    write_jsonl(index / "symbols.jsonl", symbols)
    write_jsonl(index / "dependencies.jsonl", dependencies)
    write_jsonl(index / "entrypoints.jsonl", entries)
    write_jsonl(index / "test-map.jsonl", test_map)
    languages = {}
    for item in files:
        languages[item["language"]] = languages.get(item["language"], 0) + 1
    summary = ["# Codebase Index", "", f"Generated: {manifest['generated_at']}", f"Files: {len(files)}", "", "## Languages", ""]
    summary += [f"- {name}: {count}" for name, count in sorted(languages.items(), key=lambda x: (-x[1], x[0]))]
    summary += ["", "## Entrypoints", ""] + ([f"- `{item['path']}`" for item in entries] or ["- None detected"])
    (index / "project-summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    write_json(index / "index-state.json", {"status": "current", "generated_at": manifest["generated_at"], "file_count": len(files), "reused": reused, "updated": changed})
    print(f"Index {mode} complete: {len(files)} files, {reused} reused, {changed} updated")
    return 0


def current_fingerprints(root: Path) -> dict[str, str]:
    return {norm(path.relative_to(root)): file_hash(path) for path in walk_files(root)}


def validate(root: Path) -> int:
    manifest = load_json(root / INDEX_REL / "manifest.json", None)
    if not manifest:
        print("Index missing")
        return 2
    indexed = {item["path"]: item["sha256"] for item in manifest.get("files", [])}
    current = current_fingerprints(root)
    added = sorted(current.keys() - indexed.keys())
    removed = sorted(indexed.keys() - current.keys())
    modified = sorted(path for path in current.keys() & indexed.keys() if current[path] != indexed[path])
    if added or removed or modified:
        print(json.dumps({"status": "stale", "added": added, "removed": removed, "modified": modified}, ensure_ascii=False, indent=2))
        return 2
    print("Index current")
    return 0


def read_jsonl(path: Path) -> list[dict]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, ValueError):
        return []


def query(root: Path, term: str) -> int:
    index = root / INDEX_REL
    needle = term.lower()
    rows = []
    for file in read_jsonl(index / "files.jsonl"):
        if needle in file["path"].lower():
            rows.append({"kind": "file", **file})
    for symbol in read_jsonl(index / "symbols.jsonl"):
        if needle in symbol["name"].lower():
            rows.append({"kind": "symbol", **symbol})
    for dep in read_jsonl(index / "dependencies.jsonl"):
        if needle in dep["import"].lower() or needle in (dep.get("target") or "").lower():
            rows.append({"kind": "dependency", **dep})
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    return 0 if rows else 1


def impact(root: Path, starts: list[str]) -> int:
    dependencies = read_jsonl(root / INDEX_REL / "dependencies.jsonl")
    reverse = {}
    for dep in dependencies:
        if dep.get("target"):
            reverse.setdefault(dep["target"], set()).add(dep["source"])
    roots = [norm(Path(item)) for item in starts]
    seen = set(roots)
    queue = [(item, 0) for item in roots]
    rows = []
    while queue:
        current, depth = queue.pop(0)
        for dependent in sorted(reverse.get(current, ())):
            if dependent in seen:
                continue
            seen.add(dependent)
            rows.append({"path": dependent, "depth": depth + 1, "is_test": is_test_path(dependent), "via": current})
            queue.append((dependent, depth + 1))
    result = {"roots": roots, "affected": rows, "test_candidates": [row["path"] for row in rows if row["is_test"]]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    for name in ("initialize", "refresh", "validate"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--root", default=".")
    query_cmd = sub.add_parser("query")
    query_cmd.add_argument("term")
    query_cmd.add_argument("--root", default=".")
    impact_cmd = sub.add_parser("impact")
    impact_cmd.add_argument("paths", nargs="+")
    impact_cmd.add_argument("--root", default=".")
    return result


def main() -> int:
    args = parser().parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Project root does not exist: {root}", file=sys.stderr)
        return 2
    if args.command in {"initialize", "refresh"}:
        return build(root, args.command)
    if args.command == "validate":
        return validate(root)
    if args.command == "query":
        return query(root, args.term)
    return impact(root, args.paths)


if __name__ == "__main__":
    raise SystemExit(main())
