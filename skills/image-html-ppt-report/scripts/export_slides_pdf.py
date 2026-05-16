import argparse
import re
from pathlib import Path

from PIL import Image


PAGE_RE = re.compile(r"^(?P<num>\d{2})-(?P<title>.+?)\.(?P<ext>png|jpg|jpeg|webp)$", re.IGNORECASE)


def page_number(path: Path) -> str | None:
    match = PAGE_RE.match(path.name)
    return match.group("num") if match else None


def iter_slide_images(folder: Path) -> list[Path]:
    images = [path for path in folder.iterdir() if path.is_file() and page_number(path)]
    return sorted(images, key=lambda path: (page_number(path) or "", path.name))


def image_to_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    if image.mode == "RGB":
        return image.copy()
    background = Image.new("RGB", image.size, "white")
    if image.mode in {"RGBA", "LA"}:
        background.paste(image, mask=image.getchannel("A"))
    else:
        background.paste(image.convert("RGB"))
    return background


def export_pdf(images: list[Path], output: Path) -> None:
    if not images:
        raise RuntimeError("No numbered slide images found.")

    pages = [image_to_rgb(path) for path in images]
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        first, rest = pages[0], pages[1:]
        first.save(output, "PDF", save_all=True, append_images=rest, resolution=100.0)
    finally:
        for page in pages:
            page.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export numbered slide images to a multi-page PDF.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder containing NN-topic.png slide images.")
    parser.add_argument("-o", "--output", default="report.pdf", help="Output PDF path. Relative paths are resolved inside the folder.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = folder / output

    images = iter_slide_images(folder)
    export_pdf(images, output)
    print(f"Saved PDF: {output}")
    print(f"Pages: {len(images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
