
from pathlib import Path
from typing import List

# Folders / files
DATA_DIR = Path("data/corpus")
OUTPUT_FILE = DATA_DIR / "combined_corpus.txt"

# File types we will read
VALID_EXTS = {".txt", ".md"}

def list_corpus_files() -> List[Path]:
    """Return all .txt/.md files under data/corpus/"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    for p in DATA_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in VALID_EXTS:
            files.append(p)
    return sorted(files)

def read_and_clean(path: Path) -> str:
    """Light cleanup: strip trailing spaces and collapse excess blank lines."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = [ln.rstrip() for ln in text.splitlines()]
    cleaned: List[str] = []
    prev_blank = False
    for ln in lines:
        if ln.strip() == "":
            if not prev_blank:
                cleaned.append("")  # keep a single blank line
            prev_blank = True
        else:
            cleaned.append(ln)
            prev_blank = False
    return "\n".join(cleaned).strip()

def build_corpus() -> str:
    """Concatenate all files with a header per source file."""
    files = list_corpus_files()
    if not files:
        return ""
    parts: List[str] = []
    for f in files:
        parts.append(f"# FILE: {f.name}\n{read_and_clean(f)}\n")
    return "\n\n".join(parts)

def save_corpus(text: str) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(f"[OK] Wrote combined corpus → {OUTPUT_FILE} ({len(text)} chars)")

if __name__ == "__main__":
    corpus = build_corpus()
    if not corpus.strip():
        print(f"[WARN] No .txt/.md files found in {DATA_DIR}. "
              "Add files and rerun: python src/ingest.py")
    else:
        save_corpus(corpus)

