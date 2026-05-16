import argparse
import json
import re
from pathlib import Path


NARRATION_AUDIO_SUFFIX = "-script-edge.mp3"
PAGE_RE = re.compile(
    r"^(?P<num>\d{2})-(?P<title>.+?)(?P<kind>-script-edge|-script)?(?P<ext>\.[^.]+)$"
)


def page_number(path: Path) -> str | None:
    match = PAGE_RE.match(path.name)
    return match.group("num") if match else None


def find_assets(folder: Path) -> tuple[list[str], list[str]]:
    images = sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and page_number(p)],
        key=lambda p: (page_number(p) or "", p.name),
    )
    audio_by_page = {}
    for audio in folder.iterdir():
        if not audio.is_file() or audio.suffix.lower() not in {".mp3", ".wav", ".m4a", ".ogg"}:
            continue
        number = page_number(audio)
        if number and audio.name.endswith(NARRATION_AUDIO_SUFFIX):
            audio_by_page.setdefault(number, audio.name)

    slides = [p.name for p in images]
    audios = [audio_by_page.get(page_number(p) or "", "") for p in images]
    return slides, audios


def render_template(template: str, title: str, slides: list[str], audios: list[str]) -> str:
    return (
        template.replace("__REPORT_TITLE__", title)
        .replace("__SLIDES_JSON__", json.dumps(slides, ensure_ascii=False, indent=6))
        .replace("__AUDIOS_JSON__", json.dumps(audios, ensure_ascii=False, indent=6))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build index.html from the bundled image-HTML PPT template.")
    parser.add_argument("folder", nargs="?", default=".", help="Report folder containing numbered slide images.")
    parser.add_argument("--title", default=None, help="Report title. Defaults to the folder name.")
    parser.add_argument("--output", default="index.html", help="Output HTML filename or path.")
    parser.add_argument("--template", default=None, help="Optional template path.")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    template_path = Path(args.template).expanduser().resolve() if args.template else skill_dir / "assets" / "index-template.html"
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = folder / output_path

    slides, audios = find_assets(folder)
    title = args.title or folder.name
    template = template_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_template(template, title, slides, audios), encoding="utf-8")
    print(f"Saved {output_path}")
    print(f"Slides: {len(slides)}")
    print(f"Audio files matched: {sum(1 for audio in audios if audio)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
