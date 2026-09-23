"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_sentences(text: str) -> list[str]:
    """Split on sentence endings while keeping the punctuation with the sentence."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _pack_units(units: list[str], chunk_size: int, overlap: int) -> list[str]:
    """
    Pack sentence/paragraph units into chunks under chunk_size.

    When the next unit would blow the limit, start a new chunk that begins with
    enough trailing text from the previous chunk to cover `overlap` characters
    (preferring whole units when they fit).
    """
    if not units:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    def flush() -> None:
        nonlocal current, current_len
        if current:
            chunks.append(" ".join(current).strip())
            current = []
            current_len = 0

    for unit in units:
        unit_len = len(unit)
        # Single unit longer than the window — hard-split with character overlap.
        if unit_len > chunk_size:
            flush()
            start = 0
            while start < unit_len:
                piece = unit[start : start + chunk_size].strip()
                if piece:
                    chunks.append(piece)
                if start + chunk_size >= unit_len:
                    break
                start += chunk_size - overlap
            continue

        separator = 1 if current else 0  # space between units
        if current and current_len + separator + unit_len > chunk_size:
            flush()
            # Seed the next chunk with trailing units for overlap.
            if chunks and overlap > 0:
                seed: list[str] = []
                seed_len = 0
                for prev in reversed(_split_sentences(chunks[-1])):
                    add = len(prev) + (1 if seed else 0)
                    if seed and seed_len + add > overlap:
                        break
                    seed.insert(0, prev)
                    seed_len += add
                current = seed
                current_len = seed_len

        if current:
            current_len += 1 + unit_len
        else:
            current_len = unit_len
        current.append(unit)

    flush()
    return [c for c in chunks if c]


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunker tuned for short campus_life posts.

    Most posts are under ~500 characters and already one complete thought, so
    we keep those whole. When a post has multiple paragraphs, we split on the
    blank line and pack sentences so a useful fact is not glued to an unrelated
    one. Long pieces fall back to sentence packing with overlap.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    min_keep_whole = min(chunk_size, 420)

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        text = doc.text.strip()
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

        pieces: list[str]
        if len(text) <= min_keep_whole and len(paragraphs) <= 2:
            # Short one-thought posts stay intact — the right call for campus_life.
            pieces = [text]
        else:
            units: list[str] = []
            for para in paragraphs:
                units.extend(_split_sentences(para.replace("\n", " ")))
            pieces = _pack_units(units, chunk_size, overlap)

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
