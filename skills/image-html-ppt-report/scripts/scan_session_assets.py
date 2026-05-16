import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


PAGE_RE = re.compile(
    r"^(?P<num>\d{2})-(?P<title>.+?)(?P<kind>-script-edge|-script)?(?P<ext>\.[^.]+)$"
)


def classify(path: Path) -> str:
    name = path.name
    if name.endswith("-script-edge.mp3"):
        return "audio"
    if name.endswith("-script.md"):
        return "script"
    if path.suffix.lower() == ".png":
        return "image"
    if path.suffix.lower() == ".md" and not name.endswith("-script.md"):
        return "prompt"
    return path.suffix.lower().lstrip(".") or "other"


def scan(folder: Path) -> dict:
    files = [p for p in folder.iterdir() if p.is_file()]
    extensions = defaultdict(lambda: {"count": 0, "bytes": 0})
    pages = defaultdict(dict)

    for path in files:
        ext = path.suffix.lower() or "(none)"
        extensions[ext]["count"] += 1
        extensions[ext]["bytes"] += path.stat().st_size

        match = PAGE_RE.match(path.name)
        if match:
            num = match.group("num")
            pages[num].setdefault("page", num)
            pages[num].setdefault("title", match.group("title"))
            pages[num][classify(path)] = path.name

    return {
        "folder": str(folder),
        "extensions": dict(sorted(extensions.items())),
        "pages": [pages[num] for num in sorted(pages)],
    }


def markdown(report: dict) -> str:
    lines = ["# Asset Scan", "", f"Folder: `{report['folder']}`", "", "## Extensions", ""]
    lines.append("| Extension | Count | Size MB |")
    lines.append("| --- | ---: | ---: |")
    for ext, data in report["extensions"].items():
        lines.append(f"| `{ext}` | {data['count']} | {data['bytes'] / 1024 / 1024:.2f} |")

    lines.extend(["", "## Pages", ""])
    lines.append("| Page | Title | Prompt | Image | Script | Audio |")
    lines.append("| ---: | --- | --- | --- | --- | --- |")
    for page in report["pages"]:
        lines.append(
            "| {page} | {title} | {prompt} | {image} | {script} | {audio} |".format(
                page=page.get("page", ""),
                title=page.get("title", ""),
                prompt=f"`{page['prompt']}`" if "prompt" in page else "",
                image=f"`{page['image']}`" if "image" in page else "",
                script=f"`{page['script']}`" if "script" in page else "",
                audio=f"`{page['audio']}`" if "audio" in page else "",
            )
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan image-HTML PPT report assets.")
    parser.add_argument("folder", nargs="?", default=".", help="Report/session folder to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    report = scan(folder)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
