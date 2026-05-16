import argparse
import asyncio
from pathlib import Path

import edge_tts


SCRIPT_SUFFIX = "-script.md"
AUDIO_SUFFIX = "-script-edge.mp3"


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text()


def script_to_tts_text(path: Path, paragraph_break: str) -> str:
    text = read_text(path)
    lines = [line.strip() for line in text.splitlines()]
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if not line:
            if current:
                paragraphs.append("".join(current))
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append("".join(current))
    text = paragraph_break.join(paragraphs)
    return text.strip()


async def generate_audio(text: str, output: Path, voice: str, rate: str, volume: str) -> None:
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
    )
    await communicate.save(str(output))


def default_output(markdown: Path) -> Path:
    if markdown.name.endswith(SCRIPT_SUFFIX):
        return markdown.with_name(f"{markdown.name[:-len(SCRIPT_SUFFIX)]}{AUDIO_SUFFIX}")
    return markdown.with_suffix(".mp3")


def iter_script_files(folder: Path) -> list[Path]:
    return sorted(
        [path for path in folder.iterdir() if path.is_file() and path.name.endswith(SCRIPT_SUFFIX)],
        key=lambda path: path.name,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate narration MP3 files from NN-topic-script.md files using edge-tts.")
    parser.add_argument("path", help="A script markdown file or a folder containing NN-topic-script.md files.")
    parser.add_argument("-o", "--output", help="Output MP3 path for single-file mode.")
    parser.add_argument("--voice", default="zh-CN-XiaoxiaoNeural", help="Edge TTS voice.")
    parser.add_argument("--rate", default="-5%", help="Speech rate, for example -10%%, -5%%, +0%%.")
    parser.add_argument("--volume", default="+0%", help="Speech volume, for example +0%%, -10%%, +10%%.")
    parser.add_argument("--paragraph-break", default="\n", help="Text inserted between paragraphs from blank lines.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip output files that already exist in folder mode.")
    return parser.parse_args()


async def run(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    if source.is_dir():
        scripts = iter_script_files(source)
        generated = 0
        for script in scripts:
            output = default_output(script)
            if args.skip_existing and output.exists():
                print(f"Skipping existing: {output.name}")
                continue
            text = script_to_tts_text(script, args.paragraph_break)
            if not text:
                print(f"Skipping empty script: {script.name}")
                continue
            await generate_audio(text, output, args.voice, args.rate, args.volume)
            print(f"Saved audio: {output}")
            generated += 1
        print(f"Generated {generated} audio file(s).")
        return 0

    if not source.is_file():
        raise FileNotFoundError(f"Script file or folder not found: {source}")

    output = Path(args.output).expanduser().resolve() if args.output else default_output(source)
    text = script_to_tts_text(source, args.paragraph_break)
    if not text:
        raise RuntimeError(f"Script is empty after cleanup: {source}")
    await generate_audio(text, output, args.voice, args.rate, args.volume)
    print(f"Saved audio: {output}")
    return 0


def main() -> int:
    args = parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
