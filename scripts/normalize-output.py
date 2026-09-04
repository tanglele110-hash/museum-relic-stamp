#!/usr/bin/env python3
"""Validate and normalize museum-relic stamp images for delivery."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:  # pragma: no cover - exercised only without the dependency
    requirements = Path(__file__).resolve().parent.parent / "requirements.txt"
    print(
        "Pillow is required. Install it with: "
        f"python3 -m pip install -r {requirements}",
        file=sys.stderr,
    )
    raise SystemExit(2)


ALLOWED_SIZES = {(768, 1024), (1536, 2048)}
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class NormalizationError(Exception):
    """An expected validation or output error."""


def parse_size(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*[xX×]\s*(\d+)\s*", value)
    if not match:
        raise argparse.ArgumentTypeError("size must look like 768x1024")
    size = (int(match.group(1)), int(match.group(2)))
    if size not in ALLOWED_SIZES:
        allowed = ", ".join(f"{width}x{height}" for width, height in sorted(ALLOWED_SIZES))
        raise argparse.ArgumentTypeError(f"size must be one of: {allowed}")
    return size


def safe_stem(value: str) -> str:
    stem = value.strip()
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", stem)
    stem = re.sub(r"\s+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip(" .-_")
    if not stem:
        stem = "museum-relic-stamp"
    if stem.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
        stem = f"museum-{stem}"
    return stem[:120].rstrip(" .") or "museum-relic-stamp"


def reserve_output(output_dir: Path, stem: str):
    version = 1
    while True:
        suffix = "" if version == 1 else f"-v{version}"
        candidate = output_dir / f"{stem}{suffix}.png"
        try:
            return candidate, version, candidate.open("xb")
        except FileExistsError:
            version += 1


def dimensions(width: int, height: int) -> dict[str, int]:
    return {"width": width, "height": height}


def normalize(args: argparse.Namespace) -> dict[str, object]:
    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise NormalizationError(f"input image does not exist: {source}")

    target_width, target_height = args.size
    try:
        with Image.open(source) as opened:
            opened.load()
            original_width, original_height = opened.size
            image = ImageOps.exif_transpose(opened)
            source_width, source_height = image.size
            source_info = dict(opened.info)
    except (OSError, UnidentifiedImageError) as error:
        raise NormalizationError(f"cannot read input image: {error}") from error

    if source_width * target_height != source_height * target_width:
        raise NormalizationError(
            f"input is {source_width}x{source_height}; strict 3:4 is required and cropping is disabled"
        )
    if source_width < target_width or source_height < target_height:
        raise NormalizationError(
            f"input is {source_width}x{source_height}, smaller than target "
            f"{target_width}x{target_height}; upscaling is disabled"
        )

    action = "validated" if image.size == args.size else "downscaled"
    report: dict[str, object] = {
        "status": "ok",
        "input": str(source),
        "input_pixels": dimensions(original_width, original_height),
        "oriented_pixels": dimensions(source_width, source_height),
        "target_pixels": dimensions(target_width, target_height),
        "aspect": "3:4",
        "action": action,
        "resample": None if action == "validated" else "Lanczos",
        "upscaled": False,
        "cropped": False,
        "overwritten": False,
    }

    if args.check_only:
        report["action"] = "valid" if action == "validated" else "would_downscale"
        report["output"] = None
        report["version"] = None
        return report

    has_alpha = "A" in image.getbands() or "transparency" in source_info
    image = image.convert("RGBA" if has_alpha else "RGB")
    if action == "downscaled":
        image = image.resize(args.size, Image.Resampling.LANCZOS)

    output_dir = args.output_dir.expanduser().resolve()
    stem = safe_stem(args.name or source.stem)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        destination, version, output_handle = reserve_output(output_dir, stem)
    except OSError as error:
        raise NormalizationError(f"cannot prepare output directory: {error}") from error

    save_options: dict[str, object] = {"format": "PNG", "optimize": True}
    if source_info.get("icc_profile"):
        save_options["icc_profile"] = source_info["icc_profile"]
    if source_info.get("dpi"):
        save_options["dpi"] = source_info["dpi"]

    try:
        with output_handle:
            image.save(output_handle, **save_options)
        with Image.open(destination) as completed:
            if completed.size != args.size:
                raise NormalizationError(
                    f"written image is {completed.width}x{completed.height}, expected "
                    f"{target_width}x{target_height}"
                )
            completed.verify()
    except Exception as error:
        destination.unlink(missing_ok=True)
        if isinstance(error, NormalizationError):
            raise
        raise NormalizationError(f"cannot write output image: {error}") from error

    report["output"] = str(destination)
    report["version"] = version
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a strict 3:4 museum-relic stamp, downscale it without cropping, "
            "and save it with non-destructive version naming."
        )
    )
    parser.add_argument("input", type=Path, help="source PNG, JPEG, or other Pillow-readable image")
    parser.add_argument(
        "--size",
        type=parse_size,
        default=(768, 1024),
        metavar="WIDTHxHEIGHT",
        help="delivery size: 768x1024 (default) or 1536x2048",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "output" / "museum-relic-stamp",
        help="destination directory (default: ./output/museum-relic-stamp)",
    )
    parser.add_argument(
        "--name",
        help="base filename without extension; unsafe cross-platform characters are replaced",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate and report the required action without writing a file",
    )
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    return parser


def print_report(report: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    source = report["oriented_pixels"]
    target = report["target_pixels"]
    assert isinstance(source, dict) and isinstance(target, dict)
    print(
        f"OK: {source['width']}x{source['height']} -> "
        f"{target['width']}x{target['height']} ({report['action']})"
    )
    if report["output"]:
        print(f"Output: {report['output']}")
        print(f"Version: {report['version']}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        report = normalize(args)
    except NormalizationError as error:
        if args.json:
            print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print_report(report, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
