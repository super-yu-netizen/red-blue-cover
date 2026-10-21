#!/usr/bin/env python3
"""Build local photo contact sheets and inspect cover files. No network or source edits."""

import argparse
import fnmatch
import hashlib
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
PHOTO_CACHE = Path.home() / ".cache" / "red-blue-cover" / "photos"


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def photos(args):
    if args.library is None:
        raise ValueError("Set --library or RED_BLUE_COVER_PHOTOS to an authorized photo directory.")
    library = args.library.expanduser().resolve()
    if not library.is_dir():
        raise ValueError(f"Photo library unavailable: {library}")
    paths = sorted(
        p for p in library.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
        and not any(fnmatch.fnmatchcase(p.name, pattern) for pattern in args.exclude)
    )
    if not paths:
        raise ValueError("No supported photos remain after exclusions.")
    cache = args.cache_dir.expanduser().resolve()
    if cache == library:
        raise ValueError("Cache directory must differ from the photo library.")
    entries = [
        {"index": index, "path": str(path), "size_bytes": path.stat().st_size,
         "mtime_ns": path.stat().st_mtime_ns}
        for index, path in enumerate(paths, 1)
    ]
    signature = hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()
    sheet = cache / f"photos-{signature[:16]}.jpg"
    manifest = cache / f"photos-{signature[:16]}.json"
    if sheet.is_file() and manifest.is_file():
        emit({"cached": True, "count": len(paths), "sheet": str(sheet), "manifest": str(manifest)})
        return 0
    columns = min(4, len(paths))
    cell_width, cell_height = 240, 320
    canvas = Image.new("RGB", (columns * cell_width, math.ceil(len(paths) / columns) * cell_height), "#eef0f3")
    draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(paths):
        with Image.open(path) as original:
            preview = ImageOps.exif_transpose(original).convert("RGB")
            preview.thumbnail((cell_width - 16, cell_height - 36))
            x, y = index % columns * cell_width, index // columns * cell_height
            canvas.paste(preview, (x + (cell_width - preview.width) // 2, y + 6))
        draw.text((x + 12, y + cell_height - 24), f"Photo {index + 1:02d}", fill="#111111")
    cache.mkdir(parents=True, exist_ok=True)
    canvas.save(sheet, quality=90)
    manifest.write_text(
        json.dumps({"signature": signature, "library": str(library), "photos": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    emit({"cached": False, "count": len(paths), "sheet": str(sheet), "manifest": str(manifest)})
    return 0


def check(args):
    source = args.image.expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"Cover unavailable: {source}")
    try:
        width_part, height_part = map(int, args.aspect.split(":"))
        if width_part <= 0 or height_part <= 0:
            raise ValueError
    except ValueError as error:
        raise ValueError("Aspect must be two positive integers, e.g.4:3.") from error
    with Image.open(source) as original:
        original.verify()
    with Image.open(source) as original:
        stored_size = original.size
        oriented = ImageOps.exif_transpose(original)
        width, height = oriented.size
        report = {
            "file": str(source), "readable": True, "format": original.format,
            "stored_size": list(stored_size), "display_size": [width, height],
            "expected_aspect": args.aspect,
            "aspect_ok": width * height_part == height * width_part,
            "visual_review_required": ["exact text", "identity", "hands", "brand marks", "composition"],
        }
        if args.review_dir:
            review = args.review_dir.expanduser().resolve()
            review.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            preview = oriented.convert("RGB")
            preview.thumbnail((480, 480))
            preview_path = review / f"{source.stem}-{digest[:12]}-preview.jpg"
            report_path = review / f"{source.stem}-{digest[:12]}-file-check.json"
            preview.save(preview_path, quality=92)
            report.update(sha256=digest, preview=str(preview_path), report=str(report_path))
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    emit(report)
    return 0 if report["aspect_ok"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    photo_parser = actions.add_parser("photos", help="Create or reuse a local-only photo contact sheet.")
    default_library = os.environ.get("RED_BLUE_COVER_PHOTOS")
    photo_parser.add_argument("--library", type=Path, default=Path(default_library) if default_library else None)
    photo_parser.add_argument("--cache-dir", type=Path, default=PHOTO_CACHE)
    photo_parser.add_argument("--exclude", action="append", default=[], metavar="FILENAME_PATTERN")
    photo_parser.set_defaults(run=photos)
    check_parser = actions.add_parser("check", help="Inspect readability and exact aspect; do not modify the source.")
    check_parser.add_argument("image", type=Path)
    check_parser.add_argument("--aspect", default="4:3")
    check_parser.add_argument("--review-dir", type=Path)
    check_parser.set_defaults(run=check)
    args = parser.parse_args()
    try:
        return args.run(args)
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        emit({"error": str(error), "action": args.action})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

