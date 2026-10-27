"""House-wide deny patterns and scan regexes for publish exports."""

from __future__ import annotations

# Paths relative to private_root (glob-style suffixes matched as path segments).
HOUSE_DENY: list[str] = [
    "plan/",
    "PLAN.md",
    ".arbor/",
    ".grepai/",
    ".repowise/",
    ".llm-state/",
    ".venv/",
    ".mcp.json",
    ".pytest_cache/",
    ".ruff_cache/",
    ".claude/",
    ".codex/",
    ".vscode/",
    "__pycache__/",
    "*.pyc",
    "*.db",
    "*.pkl",
    "_tmp_*",
    "publish.manifest.yaml",  # house ops — not for strangers
    "*.public.md",  # overlay sources; exported under their dest names
    "*.public.yaml",
]

# Compiled against file contents (and path strings) in the public tree after export.
HOUSE_SCAN_FORBID_REGEX: list[str] = [
    r"<portfolio-root>",
    r"<portfolio-root>",
    r"<home>",
    r"<home>",
    # plan/token.txt is checked as a real file by doctor; docs may name it.
    # literal assigned secrets (quoted). Skip code that generates tokens.
    r"(?i)(api[_-]?key|auth[_-]?token|password)\s*=\s*['\"][A-Za-z0-9_\-./+=]{16,}['\"]",
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
]

# Substrings allowed even if they match a soft path check (docs placeholders).
SCAN_ALLOW_SUBSTRINGS: list[str] = [
    "~/projects/",
    "$HOME/",
    "%USERPROFILE%",
    "<project-root>",
    "<portfolio-root>",
    "<home>",
    "your-project",
    "myapp",
    "example.com",
]

# Applied to text files during export (private absolute paths → public placeholders).
# Order matters: longer / more-specific patterns first.
# Use non-raw "\\" escapes. Doubled-backslash forms first (Python/YAML examples).
HOUSE_PATH_REWRITES: list[tuple[str, str]] = [
    ("C:\\\\Users\\\\wwylo", "<home>"),
    ("<home>", "<home>"),
    ("<home>", "<home>"),
    ("D:\\\\antigravity", "<portfolio-root>"),
    ("<portfolio-root>", "<portfolio-root>"),
    ("<portfolio-root>", "<portfolio-root>"),
]

# Extensions treated as text for path rewriting (others copied byte-for-byte).
TEXT_REWRITE_SUFFIXES: frozenset[str] = frozenset(
    {
        ".md",
        ".txt",
        ".py",
        ".yaml",
        ".yml",
        ".toml",
        ".json",
        ".jsonl",
        ".ps1",
        ".sh",
        ".bat",
        ".cmd",
        ".css",
        ".js",
        ".mjs",
        ".ts",
        ".tsx",
        ".html",
        ".svg",
        ".rst",
        ".ini",
        ".cfg",
        ".toml",
        ".gitignore",
        ".gitattributes",
        ".editorconfig",
        ".example",
    }
)
