"""Ingest: read txt/md/pdf files and turn them into chunks."""
from __future__ import annotations

from pathlib import Path

from .chunking import Chunk, chunk_document

TEXT_EXTS = {".txt", ".md", ".markdown"}
SUPPORTED = TEXT_EXTS | {".pdf"}


class IngestError(Exception):
    pass


def read_pdf_pages(path: Path) -> list[str]:
    """Extract text per page. pypdf is an optional dependency."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise IngestError(
            f"Cannot read {path.name}: PDF support needs the optional 'pypdf' package. "
            "Install it with: pip install pypdf"
        ) from exc
    reader = PdfReader(str(path))
    return [(page.extract_text() or "") for page in reader.pages]


def load_file(path: Path, size: int = 500, overlap: int = 100) -> list[Chunk]:
    """Chunk one file. Unsupported types raise IngestError."""
    ext = path.suffix.lower()
    if ext in TEXT_EXTS:
        text = path.read_text(encoding="utf-8", errors="replace")
        return chunk_document(path.name, text, size, overlap)
    if ext == ".pdf":
        chunks: list[Chunk] = []
        for page_no, text in enumerate(read_pdf_pages(path), start=1):
            # Chunk each page separately so every chunk has a real page number.
            chunks += chunk_document(path.name, text, size, overlap,
                                     page=page_no, start_index=len(chunks))
        return chunks
    raise IngestError(f"Unsupported file type: {path.name} (supported: {', '.join(sorted(SUPPORTED))})")


def collect_files(paths: list[str]) -> list[Path]:
    """Expand files and directories (recursively) into supported files."""
    found: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            found += sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED)
        elif p.is_file():
            found.append(p)
        else:
            raise IngestError(f"Path not found: {p}")
    return found


def ingest(paths: list[str], size: int = 500, overlap: int = 100) -> list[Chunk]:
    """Chunk every file under `paths`. Duplicate file names get disambiguated."""
    files = collect_files(paths)
    if not files:
        raise IngestError("No supported files found (txt, md, pdf).")
    chunks: list[Chunk] = []
    seen: dict[str, int] = {}
    for f in files:
        file_chunks = load_file(f, size, overlap)
        name = f.name
        if name in seen:  # same basename from two folders: keep ids unique
            seen[name] += 1
            name = f"{f.stem}~{seen[name]}{f.suffix}"
            for c in file_chunks:
                c.doc, c.id = name, c.id.replace(f.name, name, 1)
        else:
            seen[name] = 0
        chunks += file_chunks
    return chunks
