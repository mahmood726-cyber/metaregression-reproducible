"""Rename prior runner outputs and scratch folders; never delete an attempt."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def preserve(root=ROOT):
    root = root.resolve()
    storage = root / ".validate-work/previous"
    sources = [root / "outputs", root / ".validate-work/recut", root / ".verify-pytest"]
    if not storage.resolve().is_relative_to(root):
        raise ValueError("Previous-attempt directory escapes archive")
    for source in sources:
        if not source.resolve().is_relative_to(root):
            raise ValueError("Attempt directory escapes archive: " + str(source))
        if source.exists() and not source.is_dir():
            raise ValueError("Expected an output directory: " + str(source))
    attempt = 1
    while any((storage / (source.name + ".prev-" + str(attempt))).exists() for source in sources):
        attempt += 1
    destinations = [storage / (source.name + ".prev-" + str(attempt)) for source in sources]
    for target in destinations:
        if not target.resolve().is_relative_to(root):
            raise ValueError("Rename destination escapes archive")
    storage.mkdir(parents=True, exist_ok=True)
    moved = []
    for source, target in zip(sources, destinations):
        if source.exists():
            source.rename(target)
            moved.append((source, target))
            print("Preserved " + source.relative_to(root).as_posix() + " -> " + target.relative_to(root).as_posix())
    return moved


if __name__ == "__main__":
    preserve()
