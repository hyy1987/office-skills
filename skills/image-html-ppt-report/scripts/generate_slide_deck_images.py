import argparse
import subprocess
import sys
from pathlib import Path


PROMPT_EXTENSION = ".md"


def page_number(path: Path) -> str | None:
    name = path.name
    if len(name) >= 3 and name[:2].isdigit() and name[2] == "-":
        return name[:2]
    return None


def iter_prompt_files(folder: Path) -> list[Path]:
    files = [
        path
        for path in folder.iterdir()
        if path.is_file()
        and path.suffix.lower() == PROMPT_EXTENSION
        and not path.name.endswith("-script.md")
        and page_number(path)
    ]
    return sorted(files, key=lambda path: (page_number(path) or "", path.name))


def find_reference_image(output_dir: Path, previous_page: int) -> Path | None:
    matches = sorted(output_dir.glob(f"{previous_page:02d}-*.png"), key=lambda path: path.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def build_command(script_path: Path, prompt_path: Path, output_path: Path, args: argparse.Namespace, reference: Path | None) -> list[str]:
    command = [
        sys.executable,
        str(script_path),
        str(prompt_path),
        "-o",
        str(output_path),
        "--model",
        args.model,
        "--size",
        args.size,
        "--env-key",
        args.env_key,
    ]
    if args.base_url:
        command.extend(["--base-url", args.base_url])
    if args.quality:
        command.extend(["--quality", args.quality])
    if args.no_suffix:
        command.append("--no-suffix")
    if reference:
        command.extend(["--reference-image", str(reference)])
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate numbered slide images from NN-topic.md prompt files."
    )
    parser.add_argument("folder", nargs="?", default=".", help="Folder containing NN-topic.md prompt files.")
    parser.add_argument("--output-dir", help="Output directory. Defaults to the prompt folder.")
    parser.add_argument("--from-page", type=int, default=None, help="First page number to generate.")
    parser.add_argument("--to-page", type=int, default=None, help="Last page number to generate.")
    parser.add_argument("--reference-previous", action="store_true", help="Use the previous generated page as a reference image.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip output images that already exist.")
    parser.add_argument("--base-url", default=None, help="OpenAI-compatible base URL.")
    parser.add_argument("--env-key", default="OPENAI_API_KEY", help="API key environment variable.")
    parser.add_argument("--model", default="gpt-image-2", help="Image model.")
    parser.add_argument("--size", default="1536x1024", help="Image size.")
    parser.add_argument("--quality", default=None, help="Optional image quality value.")
    parser.add_argument("--no-suffix", action="store_true", help="Do not append the default PPT prompt suffix.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else folder
    output_dir.mkdir(parents=True, exist_ok=True)
    script_path = Path(__file__).resolve().with_name("generate_slide_image.py")

    prompts = iter_prompt_files(folder)
    generated = 0
    for prompt_path in prompts:
        number = int(page_number(prompt_path) or "0")
        if args.from_page is not None and number < args.from_page:
            continue
        if args.to_page is not None and number > args.to_page:
            continue

        output_path = output_dir / f"{prompt_path.stem}.png"
        if args.skip_existing and output_path.exists():
            print(f"Skipping existing: {output_path.name}")
            continue

        reference = find_reference_image(output_dir, number - 1) if args.reference_previous and number > 1 else None
        command = build_command(script_path, prompt_path, output_path, args, reference)
        print(f"Generating: {prompt_path.name} -> {output_path.name}")
        if reference:
            print(f"Reference: {reference.name}")
        result = subprocess.call(command)
        if result != 0:
            return result
        generated += 1

    print(f"Generated {generated} slide image(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
